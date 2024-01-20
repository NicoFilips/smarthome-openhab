'''
PURPOSE:
Das Skript parst die Alexa Stimmenkommandos, und falls sie mit dem Text in der Regel uebereinstimmen, wird ein Kommando an ein Item
verlinkt zu den Echo TTS Kanaelen. Zum Beispiel, Kann man sagen "Sind die Lichter an?", und das Geraet, dass ich gefragt habe
wird antworten mit "Alle Lichter sind aus" oder eine liste der Lichter die an sind. Zusaetzliche Fragen koennen implementiert werden.
'''
from core import org.joda.time

from core.triggers import when
from core.rules import rule
from core.log import logging, LOG_PREFIX
from random import *
from time import sleep

logVC = logging.getLogger("org.eclipse.smarthome.model.script.Rules.Alexa.py")

#-----------------------------------------------
# TODO: trimmen der inputs 
#-----------------------------------------------

def getLightStates():
    return "Die Lichter sind aus" if items["gLights"] == OnOffType.OFF else "Folgende Lichter sind an, \n{}".format("\n".join(map(lambda unlockedLock: unlockedLock.label, filter(lambda lock: lock.state == OnOffType.OFF, list(ir.getItem("gLights").getAllMembers())))))

def getWindowStates():
    return "Die Lichter sind aus" if items["gLights"] == OnOffType.OFF else "Folgende Lichter sind an, \n{}".format("\n".join(map(lambda unlockedLock: unlockedLock.label, filter(lambda lock: lock.state == OnOffType.OFF, list(ir.getItem("gLights").getAllMembers())))))

	
@rule("Alert: Voice command alert")
@when("Member of AlexaAZ_LVC received update")
def lastVoiceCommandAlert(event):
    logVC.info("Jython: Alexa hat folgendes erkannt: ['{}']".format(event.itemState))
    logVC.info(""+event.itemState.toString().lower())
    #fensterstatus
    if event.itemState.toString().lower() == "fensterstatus":
        events.sendCommand(event.itemName.replace("AlexaWZ_lastVoiceCMD", "TTS"), getWindowStates())
        logVC.info("Alexa Output:")
    #lichterstatus
    elif event.itemState.toString().lower() == "lichter status" or event.itemState.toString().lower() == "lichterstatus":
        events.sendCommand(event.itemName.replace("lastVoiceCMD","TTS"), "Momentan sind "+str(items["gTextLights"])+" Lichter in deiner Bude angeschalten")
        logVC.info("Jython: Lichter status")
    # elif event.itemState.toString().lower() == "echo":
    #     events.sendCommand(event.itemName.replace("lastVoiceCMD","TTS"), "Ja, was denn?")
    #     logVC.info("Jython: echo")
    #Alle lichter anschalten
    elif event.itemState.toString().lower() == "alle lichter an" or event.itemState.toString().lower() == "alle lichter anschalten" or event.itemState.toString().lower() == "alle lichter einschalten" or event.itemState.toString().lower() == "alle lichter ein":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Lichter angeschalten")
        events.sendCommand("gLights", "ON")
    #Nur lokale lichter an
    elif event.itemState.toString().lower() == "licht an" or event.itemState.toString().lower() == "licht ein" or event.itemState.toString().lower() == "lichter ein" or event.itemState.toString().lower() == "lichter an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        if "WZ" in event.itemName:
            logVC.info("Jython: WZ Lichter angeschalten")
            events.sendCommand("gWohnzimmer", "ON")
            events.sendCommand("gHeizungskeller","ON")
        else:
            logVC.info("Jython: SZ Lichter angeschalten")
            events.sendCommand("gBedYeelight","ON")
    elif event.itemState.toString().lower() == "lichter aus" or event.itemState.toString().lower() == "licht aus":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        if "WZ" in event.itemName:
            logVC.info("Jython: WZ Lichter angeschalten")
            events.sendCommand("gWohnzimmer", "OFF")
            events.sendCommand("gHeizungskeller","OFF")
        else:
            logVC.info("Jython: SZ Lichter angeschalten")
            events.sendCommand("gBedYeelight","OFF")
    #licht ausschalten
    elif event.itemState.toString().lower() == "alle lichter ausmachen" or event.itemState.toString().lower() == "alle lichter abschalten" or event.itemState.toString().lower() == "alle lichter ausschalten" or event.itemState.toString().lower() == "alle lichter aus":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Lichter ausgeschalten")
        events.sendCommand("gLights","OFF")
    #licht rotschalten
    elif event.itemState.toString().lower() == "licht rot" or event.itemState.toString().lower() == "licht eins":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Lichter rot")
        events.sendCommand("farbWahl","1")
    #licht grün schalten
    elif event.itemState == "licht grün" or event.itemState.toString().lower() == "licht zwei":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Lichter grün")
        events.sendCommand("farbWahl","2")
    #licht blau schalten
    elif event.itemState.toString().lower() == "licht blau" or event.itemState.toString().lower() == "licht drei":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Lichter blau")
        events.sendCommand("farbWahl","3")
    #licht gelb schalten
    elif event.itemState.toString().lower() == "licht gelb" or event.itemState.toString().lower() == "licht vier":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Lichter gelb")
        events.sendCommand("farbWahl","4")
    #licht türkis schalten
    elif event.itemState.toString().lower() == "licht türkis" or event.itemState.toString().lower() == "licht fünf":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Lichter türkis")
        events.sendCommand("farbWahl","5")
    #licht violett schalten
    elif event.itemState.toString().lower() == "licht violett" or event.itemState.toString().lower() == "licht sechs":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Lichter violett")
        events.sendCommand("farbWahl","6")
    #licht weiß schalten
    elif event.itemState.toString() == "licht weiß" or event.itemState.toString().lower() == "licht weiss" or event.itemState.toString().lower() == "licht hell" or event.itemState.toString().lower() == "licht sieben":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Lichter weiß")
        events.sendCommand("farbWahl","7")
    #strobolicht anschalten
    elif event.itemState.toString() == "city club an" or event.itemState.toString().lower() == "strobolicht an" or event.itemState.toString().lower() == "strobo an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Lichter strobo")
        events.sendCommand("AlexaWZ_MusicProviderId","SPOTIFY")
        events.sendCommand("AlexaWZ_Player","PLAY")
        events.sendCommand("farbWahl","8")
    #alle strobolicht anschalten
    elif event.itemState.toString() == "kompletter city club an" or event.itemState.toString().lower() == "alle strobolicht an" or event.itemState.toString().lower() == "alle strobo an" or event.itemState.toString().lower() == "alle lichter strobo":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Lichter strobo")
        events.sendCommand("AlexaWZ_MusicProviderId","SPOTIFY")
        events.sendCommand("AlexaWZ_Player","PLAY")
        events.sendCommand("farbWahl","13")
    #licht bunt schalten
    elif event.itemState.toString().lower() == "licht bunt":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Lichter bunterfade")
        events.sendCommand("farbWahl","9")
    elif event.itemState.toString().lower() == "alle lichter bunt":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Alle Lichter bunterfade")
        events.sendCommand("farbWahl","10")
    #fernseher anschalten
    elif event.itemState.toString().lower() == "fernseher an" or event.itemState.toString().lower() == "tv an" or event.itemState.toString().lower() == "t.v. an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Fehrnseher angeschalten")
        events.sendCommand("wol_fernseher","ON")
    #pc anschalten
    elif event.itemState.toString().lower() == "pc an" or event.itemState.toString().lower() == "p. c. an" or event.itemState.toString().lower() == "rechner an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: PC angeschalten")
        events.sendCommand("wol_rechner","ON")
    #drucker anschalten
    elif event.itemState.toString().lower() == "drucker an" or event.itemState.toString().lower() == "epsondrucker an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Drucker angeschalten")
        events.sendCommand("wol_drucker","ON")
    #staubsauger an
    elif event.itemState.toString().lower() == "staubsauger an" or event.itemState.toString().lower() == "staubsaugerroboter an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Staubsauger angeschalten")
        events.sendCommand("actionControl","vacuum")
    #staubsauger leise
    elif event.itemState.toString().lower() == "staubsauger leise" or event.itemState.toString().lower() == "staubsaugerroboter leiser":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Staubsauger auf leise geschalten")
        events.sendCommand("actionFan","38")
    #staubsauger laut
    elif event.itemState.toString().lower() == "staubsauger laut" or event.itemState.toString().lower() == "staubsaugerroboter laut":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Staubsauger auf laut geschalten")
        events.sendCommand("actionFan","90")
    #staubsauger ausschalten
    elif event.itemState.toString().lower() == "staubsauger aus" or event.itemState.toString().lower() == "staubsaugerroboter aus":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Staubsauger angeschalten")
        events.sendCommand("actionControl","dock")
    #wohnzimmerthermostat ausschalten
    elif event.itemState.toString().lower() == "wohnzimmer thermostat aus":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Wohnzimmerthermostat aus")
        events.sendCommand("SollTempDect2","18")
    #wohnzimmerthermostat anschalten
    elif event.itemState.toString().lower() == "wohnzimmer thermostat an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Wohnzimmerthermostat an")
    #thermostate anschalten
    elif event.itemState.toString().lower() == "thermostate an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: beide Thermostate an")
        events.sendCommand("SollTempDect2","26")
        events.sendCommand("SollTempDect1","26")
    #schlafzimmerthermostat ausschalten
    elif event.itemState.toString().lower() == "schlafzimmer thermostat an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Schlafzimmerthermostat an")
        events.postUpdate("SollTempDect1","26")
    #wohnzimmerthermostat ausschalten
    elif event.itemState.toString().lower() == "schlafzimmer thermostat aus":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Wohnzimmerthermostat aus")
        events.sendCommand("SollTempDect1","18")
    #licht zufallsfarbe
    elif event.itemState.toString().lower() == "licht zufall" or event.itemState.toString().lower() == "lichter zufallsfarbe" or event.itemState.toString().lower() == "zufallsfarbe":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        x = randint(1,8)
        logVC.info("Jython: Lichter Zufalls farbe: " + str(x))
        events.sendCommand("farbWahl", str(x))
    #NUR schlafzimmerlicht an
    elif event.itemState.toString().lower() == "nur schlafzimmer licht an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Schlafzimmerlicht eingeschalten")
        events.sendCommand("zimmerWahl", "2")
    #NUR wohnzimmerlicht an
    elif event.itemState.toString().lower() == "nur wohnzimmer licht an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Wohnzimmerlicht eingeschalten")
        events.sendCommand("zimmerWahl", "1")
    #NUR heizungskellerlicht an
    elif event.itemState.toString().lower() == "nur heizungskeller licht an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Heizungskellerlicht eingeschalten")
        events.sendCommand("zimmerWahl", "4")
    #NUR flurlicht an
    elif event.itemState.toString().lower() == "nur flur licht an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Flurlicht eingeschalten")
        events.sendCommand("zimmerWahl", "3")
    #schlafzimmerlicht an
    elif event.itemState.toString().lower() == "schlafzimmer licht an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Schlafzimmerlicht eingeschalten")
        events.sendCommand("gBedYeelight", "ON")
    #wohnzimmerlicht an
    elif event.itemState.toString().lower() == "wohnzimmer licht an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Wohnzimmerlicht eingeschalten")
        events.sendCommand("gWohnzimmer", "ON")
    #heizungskellerlicht an
    elif event.itemState.toString().lower() == "heizungskeller licht an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Heizungskellerlicht eingeschalten")
        events.sendCommand("gHeizungskeller", "ON")
    #flurlicht an
    elif event.itemState.toString().lower() == "flur licht an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Flurlicht eingeschalten")
        events.sendCommand("gFlurlicht", "ON")
    #06:00 Wecker an
    elif event.itemState.toString().lower() == "frühes aufstehen an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"ok")
        logVC.info("Jython: Wecker auf 06:00 Uhr gestellt")
        events.sendCommand("PERSON1_WECKER_PRESETS","1")
    #07:00 Wecker an
    elif event.itemState.toString().lower() == "normales aufstehen an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"ok")
        logVC.info("Jython: Wecker auf 07:00 Uhr gestellt")
        events.sendCommand("PERSON1_WECKER_PRESETS","2")
    #08:00 Wecker an
    elif event.itemState.toString().lower() == "spätes aufstehen an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"ok")
        logVC.info("Jython: Wecker auf 08:00 Uhr gestellt")
        events.sendCommand("PERSON1_WECKER_PRESETS","3")
    #06:30 Wecker an
    elif event.itemState.toString().lower() == "schulwecker an" or event.itemState.toString().lower() == "berufsschul aufstehen an" or event.itemState.toString().lower() == "berufsschule aufstehen an" or event.itemState.toString().lower() == "berufsschul wecker an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: Wecker auf 06:30 Uhr gestellt")
        events.sendCommand("PERSON1_WECKER_PRESETS","4")
    #Ender 3D Druckerstatus (Düse/Betttemperatur)    
    elif event.itemState.toString().lower() == "3d drucker status" or event.itemState.toString().lower() == "drei d. drucker status" or event.itemState.toString().lower() == "ender drucker status":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"), "Das Druckbett hat"+items["OctoprintPrinterBedTemp"].toString()+" und die Nozzle hat"+items["OctoprintPrinterHotEndTemp"].toString()+" Grad")
        logVC.info("Jython: 3D Drucker Status abgefragt")
    #Ender motoren an    
    elif event.itemState.toString().lower() == "ender motoren an" or event.itemState.toString().lower() == "stepper motoren an" or event.itemState.toString().lower() == "ender stepper an":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        events.sendCommand("OctoprintPrinterCommand","M17")
        logVC.info("Jython: Stepper Motoren ausgeschalten")
    #Ender motoren an
    elif event.itemState.toString().lower() == "ender motoren aus" or event.itemState.toString().lower() == "stepper motoren aus" or event.itemState.toString().lower() == "ender stepper aus" or event.itemState.toString().lower() == "stecker motoren aus"  or event.itemState.toString().lower() == "Motoren aus" or event.itemState.toString().lower() == "Endermotoren aus"  or event.itemState.toString().lower() == "Ender 3 motoren aus" :
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        events.sendCommand("OctoprintPrinterCommand","M18")
        logVC.info("Jython: Stepper Motoren eingeschalten")
    #Ender lüfter aus
    elif event.itemState.toString().lower() == "lüfter aus":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        events.sendCommand("OctoprintPrinterCommand","M106")
        logVC.info("Jython: Lüfter ausgeschalten")
    #Ender lüfter an
    elif event.itemState.toString().lower() == "lüfter an" or event.itemState.toString().lower() == "ender lüfter an" or event.itemState.toString().lower() == "ender lüfter":
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        events.sendCommand("OctoprintPrinterCommand","M107") 
        logVC.info("Jython: Lüfter angeschalten")
    #Ender autohomen
    elif event.itemState.toString().lower() == "bett level an" or event.itemState.toString().lower() == "ender leveln" or event.itemState.toString().lower() == "ABL an":
        events.sendCommand("OctoprintPrinterCommand","mesh_bed_level")
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: AutoHome angeschalten")
    #Ender autohomen
    elif event.itemState.toString().lower() == "auto home an" or event.itemState.toString().lower() == "ender nach hause" or event.itemState.toString().lower() == "ender auto home":
        events.sendCommand("OctoprintPrinterCommand","G28")
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        logVC.info("Jython: AutoHome angeschalten")
    #Helligkeit schalten
    elif event.itemState.toString().lower().startswith("helligkeit auf"):
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        i = parseValue(event.itemState.toString().lower())
        events.sendCommand("gBrightness",str(i))
    #wohnzimmerthermostat schalten
    elif event.itemState.toString().lower().startswith("wohnzimmerthermostat auf") or event.itemState.toString().lower().startswith("wohnzimmer thermostat auf") :
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        i = parseDegree(event.itemState.toString().lower())
        events.sendCommand("SollTempDect2",str(i))
    #schlafzimmerthermostat schalten
    elif event.itemState.toString().lower().startswith("schlafzimmerthermostat auf") or event.itemState.toString().lower().startswith("schlafzimmer thermostat auf"):
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        i = parseDegree(event.itemState.toString().lower())
        events.sendCommand("SollTempDect1",str(i))
    #Thermostate schalten
    elif event.itemState.toString().lower().startswith("thermostate auf"):
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht chef")
        i = parseDegree(event.itemState.toString().lower())
        events.sendCommand("SollTempDect2",str(i))
        events.sendCommand("SollTempDect1",str(i))
    elif event.itemState.toString().lower() == "wecker aus" or event.itemState.toString().lower() == "webserverwecker aus":
        events.sendCommand("gBedYeelight","OFF")
        events.sendCommand("AlexaSZ_Player","PAUSE")
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Webserver wecker wurde ausgeschalten. Bitte stehe auf, Chef")
    elif event.itemState.toString().lower() == "lautsprecher aus" or event.itemState.toString().lower() == "lautsprecher an":
        events.sendCommand("Mi_trust_Power","ON")
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht Chef")
    elif event.itemState.toString().lower() == "lautsprecher stumm" or event.itemState.toString().lower() == "lautsprecher laut":
        events.sendCommand("Mi_trust_Mute","ON")
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht Chef")
    elif event.itemState.toString().lower() == "lautsprecher licht aus" or event.itemState.toString().lower() == "lautsprecher licht an":
        events.sendCommand("Mi_trust_LED","ON")
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht Chef")
    elif event.itemState.toString().lower() == "netflix an" or event.itemState.toString().lower() == "netflix und chill" or event.itemState.toString().lower() == "netflix and chill":
        events.sendCommand("Mi_TCL_Netflix","ON")
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht Chef")
    elif event.itemState.toString().lower() == "wii an" or event.itemState.toString().lower() == "nintendo wii an" or event.itemState.toString().lower() == "nintendo an":
        events.sendCommand("Mi_TCL_Zeug","4")
        events.sendCommand("Mi_TCL_back","ON")
        events.sendCommand("Mi_TCL_ok","ON")
        events.sendCommand(event.itemName.replace("lastVoiceCMD", "TTS"),"Wird gemacht Chef")
    
def parseValue(stringVal):
    if "zehn" in stringVal:
        return 10
    elif "zwanzig" in stringVal:
        return 20
    elif "dreißig" in stringVal:
        return 30
    elif "vierzig" in stringVal:
        return 40
    elif "fünfzig" in stringVal:
        return 50
    elif "sechzig" in stringVal:
        return 60
    elif "siebzig" in stringVal:
        return 70
    elif "achtzig" in stringVal:
        return 80
    elif "neunzig" in stringVal:
        return 90
    elif "hundert" in stringVal:
        return 100

def parseDegree(stringVal):
    if "sechzehn" in stringVal:
        return 16
    elif "siebzehn" in stringVal:
        return 17
    elif "achtzehn" in stringVal:
        return 18   
    elif "neunzehn" in stringVal:
        return 19
    elif "zwanzig" in stringVal:
        return 20
    elif "einundzwanzig" in stringVal:
        return 21
    elif "zweiundzwanzig" in stringVal:
        return 22
    elif "dreiundzwanzig" in stringVal:
        return 23
    elif "vierundzwanzig" in stringVal:
        return 24
    elif "fünfundzwanzig" in stringVal:
        return 25
    elif "sechsundzwanzig" in stringVal:
        return 26
    elif "siebenundzwanzig" in stringVal:
        return 27
    elif "achtundzwanzig" in stringVal:
        return 28
    elif "neunundzwanzig" in stringVal:
        return 29
    elif "dreißig" in stringVal:
        return 30

@rule("Lass Alexa sprechen")
@when("Item AlexaTTS received command")
def lassAlexaSprechen(event):
    sleep(0.5)
    strTTSstring = ""
    strTTSstring = items["AlexaTTS"].toString()
    #strTTSstring = event.itemState.toString()
    logVC.info("Jython: AlexaTTS - "+strTTSstring)
    if items["AlexaEchoChoose"].toString != UnDefType.NULL or items["AlexaEchoChoose"].toString() == "2":
         events.sendCommand("AlexaSZ_TTS",strTTSstring)
         events.sendCommand("AlexaWZ_TTS",strTTSstring)
    elif items["AlexaEchoChoose"].toString() == "1":
        events.sendCommand("AlexaSZ_TTS",strTTSstring)
    elif items["AlexaEchoChoose"].toString() == "0": 
        events.sendCommand("AlexaWZ_TTS",strTTSstring)
