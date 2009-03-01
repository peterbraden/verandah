verandah = {}


$(document).ready(function(){
	
	
	/* Add lightbox Day event to day */
	$(".day-header").click(function(){
		$(this).parent().dialog();
	}).css('cursor', 'pointer');
	
	
	/* Event Click Show lightbox Form */
	$(".event").click(function(){
		$(this).dialog();
	}).css('cursor', 'pointer');

	/* Add Event form lightbox */
	$("#add_event").click(function(){
		$("#event_form").show().dialog();
		return false;
	});
	
	
	/* Jquery ui datetimepicker */
	$("input.datetime").datepicker();

});
		
		