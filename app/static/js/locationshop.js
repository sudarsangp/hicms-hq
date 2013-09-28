
$(document).ready(function(){
	$('.tohide').hide();
	
	$('#citycountry').change(function(){

		var cityVal = $('#city option:selected').text();
		var countryVal = $('#country option:selected').text();
		if(cityVal == "None" || countryVal == "None"){
			$('.tohide').show();
			$("label[for=emformlocation-csrf_token]").hide();
		}
		else{
			$('.tohide').hide();
		}
	});
	
});