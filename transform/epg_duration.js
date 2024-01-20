// computes nicely formatted duration from given minutes
(function(i){ 

	var d = Math.floor(i / (24 * 60));
	var h = Math.floor((i / 60) - (24 * d));
	var m = Math.round(i - 60 * (24 * d + h));
	var result = '';

	// Tage
	if (d > 0) { 
		result = result + d;
		if (d == 1) {
			result = d + " Tag";
		} else {
			result = d + " Tage";
		}
	}

	// Stunden
	if (h > 0) {
		if (result != '') {
			result = result + ', ';
		}
		result = result + h;
		if (h == 1) {
			result = result + ' Stunde';
		} else {
			result = result + ' Stunden';
		}
	}
	
	// Minuten
	if (m > 0) {
		if (result != '') {
			result = result + ', ';
		}
		result = result + m;
		if (m == 1) {
			result = result + ' Minute';
		} else {
			result = result + ' Minuten';
		}
	}

	if (d == 0 && h == 0 && m == 0) {
		return 'Jetzt vorbei' + result;
	}

	return 'noch ' + result;
})(input)