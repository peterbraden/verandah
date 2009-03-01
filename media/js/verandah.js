verandah = {}

/**
* Hint:
* A Jquery Plugin to allow 'hints' to be added to an input
*/
$.fn.hint = function (text) {
	return this.each(function () {
    	var input = $(this);
    	var form = $(this.form);
		
		function remove() {
			if (input.val() === text && input.hasClass('blur')) {
				input.val('').removeClass('blur');
      			}
			}

		input.blur(function () {
			if (this.value === '') {
				input.val(text).addClass('blur');
        	}
		}).focus(remove).blur();
		form.submit(remove);
      	$(window).unload(remove); // handles Firefox's autocomplete
    });
};


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
		
		// Extract header
		var title = form.find('h2').text()
		form.find('h2').remove();
		
		// Switch Labels into input hints 
		form.find('input, textarea').each(function(){
			var label = form.find('label[for=' + $(this).attr('id') + ']');
			$(this).hint(label.text());
			label.remove();
		});
		
		// Make datefields datepickers
		//form.find('input.datetime').removeClass('hasDatepicker').datepicker();
		//$("#ui-datepicker-div").css("z-index", 3000);
		
		/* On submit do ajax */
		//form.submit(function(){
		//	console.log(form)
		//	return false;
		//});
		
		form.show().dialog({
			'title' : title, 
			'modal' : true, 
			'resizable': false,
			'width' : '20em',
			});
			
		return false;
	});
	
	


});
		
		