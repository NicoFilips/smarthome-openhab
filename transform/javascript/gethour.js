//transforms Minutes into Hours
(function(i){ 

	var result = ((parseInt(i) / 60).toFixed(0) + " Std");
    // if (parseInt(result) > 24){
    //     result = (result / 24 )
    // } 
    return result;
    
})(input)