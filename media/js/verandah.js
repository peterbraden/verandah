verandah = {}


$(document).ready(function(){
	
	
	/* Add lightbox Day event to day */
	$(".day-header").click(function(){
		$(this).parent().dialog();
	}).css('cursor', 'pointer');
	
	
	/* Event Click Show lightbox Form */
	$(".event").click(function(){
		$(this).clone().dialog({'title' : 'Modify Event', 'modal' : true});
	}).css('cursor', 'pointer');

	/* Add Event form lightbox */
	$("#add_event").click(function(){
		var form = $("#event_form").clone();
		
		var title = form.find('h2').text()
		form.find('h2').remove();
		form.show().dialog({'title' : title, 'modal' : true, 'resizable': false});
		return false;
	});
	
	
	/* Jquery ui datetimepicker */
	$("input.datetime").datepicker();

});
		
		