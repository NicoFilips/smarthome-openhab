import java.io.File 

// #############################################################
//                      Global EPG Settings
// #############################################################
//
// ----------------------- PREREQUISITES -----------------------
// 'Exec' Binding - Check
// 'MAP' Transformation (including 'epg.map') - Check
// 'xmltv' installed ('sudo apt-get install xmltv') - Check
// 'epg_parser.py' in OH script-directory
// 
// 'JS' Transformation (for easier duration-calculation) [OPTIONAL] - Check 
// -------------------------------------------------------------
//
// ---------------------- Übersicht der Regeln -----------------
//
// EPG -> 0 - erstellen erneuern von epgsource.xml
// EPG -> 1 - minimiert epgsource.xml und erstellt/erneuert epgsource_bynow.xml
// EPG -> 2
// EPG -> 3
// EPG -> 4
//
// -------------------------------------------------------------
//
val xml_grabber = "tv_grab_eu_egon" 
val xml_path = "/etc/openhab2/html/epg/"
val script_path = "/etc/openhab2/scripts/"
//
// #############################################################

// -------------------------------------------------------------> START
//
//                      EPG Rule #1
//
// Die Regel holt sich alle XMLTV Daten der Channel
// von der Auswahl der xmltv-config.
//
// Braucht Internetverbindung zum Ausführen!
//
//
// -------------------------------------------------------------
rule "EPG - 2-Tagesvorschau Update XMLTV-file"
when
    System started or 
    Time cron "0 3 0 * * ?" or // ... Jede Nacht um 3
    Item EPG_Update received update 0 // ... Falls eine Regel '0' an 'EPG_Update' sendet.
then
    val epgConfig = new File(xml_path + "conf/epg_eu.conf")
    val epgSource = new File(xml_path + "data/epgsource.xml")

    // Abbrechen falls xmltv-config fehlt
    if (epgConfig.isFile() == false || epgConfig.canRead() == false) {
        logError("EPG","EPG Error: Update/Initialisierung fehlerhaft ('epg_eu.conf' fehlt oder kann nicht geöffnet werden)")
        return
    }

    // Checken ob epgsource.xml verfügbar ist...
    if (epgSource.isFile() && epgSource.canRead()) {
        val newdate = new DateTime(now().minusHours(12))
        val filedate = new DateTime(epgSource.lastModified())

        // Erneuern von epgsource.xml falles es zuletzt vor ÜBER 12 Stunden geupdated wurde
        if(filedate.isBefore(newdate)) {
            logInfo("EPG","EPG: 'epgsource.xml' ist vorhanden, jedoch älter als 12 Stunden - Starting update... ")
            executeCommandLine("sudo /usr/bin/" + xml_grabber + " --config-file " + xml_path + "conf/epg_eu.conf --days 2 --quiet --output " + xml_path + "data/epgsource.xml",5000)
            sendCommand(EPG_Update, 1) // Weiter zur nächsten Regel #2
            return
        } else { return }
    } else {
        // Ausführen falls epgsource.xml nicht auffind- oder bearbeitbar ist.
        logInfo("EPG","EPG: 'epgsource.xml ' ist nicht verfügbar oder bearbeitbar - holen von EPG-data...")
        executeCommandLine("sudo /usr/bin/" + xml_grabber + " --config-file " + xml_path + "conf/epg_eu.conf --days 2 --quiet --output " + xml_path + "data/epgsource.xml",5000)
        sendCommand(EPG_Update, 1) // continue with rule step #2
    }
end // -------------------------------------------------------------> END

// -------------------------------------------------------------> START
//
//                          EPG Rule #2
//
// minimiert 'epgsource.xml' stündlich, mit Erstellung
// einer anderen Datei für alle Show die jetzt laufen.
// 
// -------------------------------------------------------------
rule "EPG - Minimiert XMLTV-Datei jede Stunde"
when
    Time cron "0 0 * * * ?" or // Ausführung in jeder Stunde...
    Item EPG_Update received update 1 // ... und falls Regel #1 einen Trigger sendet
then
    // Checkt verfügbarkeit von 'epgsource.xml'
    val epgSource = new File(xml_path + "data/epgsource.xml") 
    if(epgSource.isFile() && epgSource.canRead()) { 

        // Extrahiert alle Shows die jetzt laufen, hängt von der lokalen Zeit ab
        executeCommandLine("sudo /usr/bin/tv_grep --on-after now --output " + xml_path + "data/epgsource_bynow.xml " + xml_path + "data/epgsource.xml",5000)
        sendCommand(EPG_Update, 2) // weitermachen mit regel #3 
        logInfo("EPG","EPG: 'epgsource.xml' successfully minimized.")
    } else {
        sendCommand(EPG_Update, 0) // falls 'epgsource' nicht gefunden wurde - Zurück zu Regel #1...
        return
    }
end // -------------------------------------------------------------> END

// -------------------------------------------------------------> START
//
//                          EPG Rule #3
//
// Extract the current and next tv-shows for all selected
// channels from 'epgsource_bynow.xml'.
//
// -------------------------------------------------------------
rule "EPG - Holen der aktuellen TV Show und der nächsten, der minimierten epgsource_bynow.xml"
when
    Item EPG_Update received update 2 // Ausführen bei Update '2'
then
    // Verfügbarkeit checken von 'epgsource_bynow.xml'
    val epgFiltered = new File(xml_path + "data/epgsource_bynow.xml")
    if(epgFiltered.isFile() && epgFiltered.canRead()) {
        // Splitten der minimierten xmltv-Datei in eins für jeden Channel
        executeCommandLine("sudo /usr/bin/tv_split --output " + xml_path + "data/%channel_bynow.xml " + xml_path + "data/epgsource_bynow.xml",5000) 

        gTVChannel.members.filter[ i | i.state != NULL ].forEach[ i |
            // Extrahieren&Transformieren von channelID vom Item
            val chan = i.name.split("_").get(2).toString
            val channelId = transform("MAP", "map/epg.map", chan)

            // Query für jetztige und nächste TV-Show
            val stop = executeCommandLine("sudo python " + script_path + "epg_parser.py -t " + xml_path + "data/" + channelId + "_bynow.xml -c get_stopextra",5000)
            executeCommandLine("sudo /usr/bin/tv_grep --on-after now --on-before now --output " + xml_path + "data/" + channelId + "_now.xml " + xml_path + "data/" + channelId + "_bynow.xml",5000)
            executeCommandLine("sudo /usr/bin/tv_grep --on-after " + stop + " --on-before " + stop + " --output " + xml_path + "data/" + channelId + "_next.xml " + xml_path + "data/" + channelId + "_bynow.xml",5000)
        ]

        // Weiter zu Regel #4
        sendCommand(EPG_Update, 3) 
        return

    } else {
        logError("EPG", "EPG Error: Update fehlgeschlagen ('epgsource_bynow.xml' ist nicht vorhanden oder kann nicht bearbeitet werden)" )
        sendCommand(EPG_Update, 1) // zurück zu Regel #2
        return
    }
end // -------------------------------------------------------------> END

// -------------------------------------------------------------> START
// 
//                          EPG Rule #4
//
// Extrahieren aller Werte in den *.xml-dateien und senden 
// an ihre openHAB-items.
//
// -------------------------------------------------------------
rule "EPG - Updateinfos an openHAB-items senden"
when
    Item EPG_Update received update 3 // Ausführen bei Update #3
then
    gTVChannel.members.forEach[ i |
        val room = i.name.split("_").get(0).toString
        val type = i.name.split("_").get(1).toString
        val chan = i.name.split("_").get(2).toString
        // Setzen von Variablen namen & transform Werten
        val currentShowTitleItem = room + "_" + type + "_" + chan + "_CurrentShow"
        val nextShowTitleItem = room + "_" + type + "_" + chan + "_NextShow"
        val currentShowStartTimeItem = room + "_" + type + "_" + chan + "_CurrentShowStartTime"
        val nextShowStartTimeItem = room + "_" + type + "_" + chan + "_NextShowStartTime"
        val currentShowStopTimeItem = room + "_" + type + "_" + chan + "_CurrentShowStopTime"
        val nextShowStopTimeItem = room + "_" + type + "_" + chan + "_NextShowStopTime"
        // val currentShowStartStopItem = room + "_" + type + "_" + chan + "_CurrentShowStartStop"
        val nextShowStartStopItem = room + "_" + type + "_" + chan + "_NextShowStartStop"
        // val logoURLItem = room + "_" + type + "_" + chan + "_LogoURL"
        val channelId = transform("MAP", "map/epg.map", chan)

        // Ausführen des python-scripts epg_parser.py
        val channelName = executeCommandLine("sudo python " + script_path + "epg_parser.py -t " + xml_path + "data/" + channelId + "_now.xml -c get_channelname",5000)
        val currentShowTitle = executeCommandLine("sudo python " + script_path + "epg_parser.py -t " + xml_path + "data/" + channelId + "_now.xml -c get_title",5000)
        val nextShowTitle = executeCommandLine("sudo python " + script_path + "epg_parser.py -t " + xml_path + "data/" + channelId + "_next.xml -c get_title",5000)
        val currentShowStartTime = executeCommandLine("sudo python " + script_path + "epg_parser.py -t " + xml_path + "data/" + channelId + "_now.xml -c get_starttime",5000)
        val nextShowStartTime = executeCommandLine("sudo python " + script_path + "epg_parser.py -t " + xml_path + "data/" + channelId + "_next.xml -c get_starttime",5000)
        val currentShowStopTime = executeCommandLine("sudo python " + script_path + "epg_parser.py -t " + xml_path + "data/" + channelId + "_now.xml -c get_stoptime",5000)
        val nextShowStopTime = executeCommandLine("sudo python " + script_path + "epg_parser.py -t " + xml_path + "data/" + channelId + "_next.xml -c get_stoptime",5000)
        // val currentShowStartStop = executeCommandLine("sudo python " + script_path + "epg_parser.py -t " + xml_path + "data/" + channelId + "_now.xml -c get_startstop",5000)
        val nextShowStartStop = executeCommandLine("sudo python " + script_path + "epg_parser.py -t " + xml_path + "data/" + channelId + "_next.xml -c get_startstop",5000)
        // val logoURL = executeCommandLine("sudo python " + script_path + "epg_parser.py -t " + xml_path + "data/" + channelId + "_now.xml -c get_logourl",5000)

        // Werte an OpenHAB items senden
        sendCommand(i.name, channelName)
        sendCommand(currentShowTitleItem, currentShowTitle)
        sendCommand(nextShowTitleItem, nextShowTitle)
        if (currentShowStartTime != "" || currentShowStartTime != NULL) { sendCommand(currentShowStartTimeItem, currentShowStartTime.toString) }
        sendCommand(nextShowStartTimeItem, nextShowStartTime.toString)
        if (currentShowStopTime.toString != "" || currentShowStopTime.toString != NULL) { sendCommand(currentShowStopTimeItem, currentShowStopTime.toString) }
        sendCommand(nextShowStopTimeItem, nextShowStopTime.toString)
        // sendCommand(currentShowStartStopItem, currentShowStartStop.toString)
        sendCommand(nextShowStartStopItem, nextShowStartStop.toString)
        // sendCommand(logoURLItem, logoURL)
    ]

    // Kalkulieren der Laufzeit von momentan laufenden Shows
    gTVStopTime.members.forEach[ i |
        val currentShowDuration = i.name.split("_").get(0).toString+"_"+i.name.split("_").get(1).toString+"_"+i.name.split("_").get(2).toString+"_CurrentShowDuration"
        val oldDate = new DateTime((i.state as DateTimeType).calendar.timeInMillis).millis
        val newDate = new DateTime(now()).millis
        val duration = (((oldDate-newDate) / 1000) / 60)
        sendCommand(currentShowDuration, duration.toString)
    ]

    sendCommand(EPG_Update, 4) // wenn das senden von Werten an OH Items erfolgreich war
    logInfo("EPG","EPG: openHAB-items erfolgreich geupdated! \u2713")
end // -------------------------------------------------------------> END

// -------------------------------------------------------------> START
//
//                          EPG Rule #5  
//
// Die Regel ist wichtig um Systemrufe auf ein minimum
// zu reduzieren - es checkt, ob die stop-zeit von jeder der laufenden 
//  tv-shows erreicht wurde.
//
// -------------------------------------------------------------
rule "EPG - Check if an EPG update is needed"
when
    Time cron "0 0/1 * * * ?" //Jede Minute
then
    // Checken von 'epgsource_bynow.xml'
    val epgByNow = new File(xml_path + "data/epgsource_bynow.xml")
    if(epgByNow.isFile() && epgByNow.canRead()) { 

        // Kalkulieren der verbleibenden Zeit der aktuellen Show
        gTVStopTime.members.forEach[ i |
            val currentShowDuration = i.name.split("_").get(0).toString+"_"+i.name.split("_").get(1).toString+"_"+i.name.split("_").get(2).toString+"_CurrentShowDuration"
            logInfo("filename"," "+ currentShowDuration.toString() +" "+ i.state.toString())
            val oldDate = new DateTime((i.state as DateTimeType).calendar.timeInMillis).millis
            val newDate = new DateTime(now()).millis
            val duration = (((oldDate-newDate) / 1000) / 60)
            sendCommand(currentShowDuration, duration.toString)
        ]

        // Timestamp für die Show mit dem frühesten Ende
        val stopTime = executeCommandLine("sudo python " + script_path + "epg_parser.py -t " + xml_path + "data/epgsource_bynow.xml -c get_stopextra",5000) 
        val DateTimeType timestamp = DateTimeType.valueOf(stopTime) // Convert human readable time stamp to DateTimeType

        // Compare current time with earliest stopDate of the current running shows
        if (now.isAfter(new DateTime(timestamp.zonedDateTime.toInstant.toEpochMilli)) ) { 
            executeCommandLine("sudo /usr/bin/tv_grep --on-after now --output " + xml_path + "data/epgsource_bynow.xml " + xml_path + "data/epgsource.xml",5000) // Update 'epgsource_bynow.xml'
            sendCommand(EPG_Update, 2) // execute rule #2
            logInfo("EPG", "EPG: Eine TV-Show wurde beendet. Update starten...")
        } else { return }
    } else {
        logError("EPG", "EPG Error: Update fehlgeschlagen ('epgsource_bynow.xml' fehlt oder kann nicht bearbeitet werden.)" )
        sendCommand(EPG_Update, 1) // return to rule #2
        return
    }
end 
// -------------------------------------------------------------> END