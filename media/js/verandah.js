verandah = {}



verandah.addBox = Object();
verandah.addBox.visible = false;
verandah.addBox.width = 400;
verandah.addBox.height = 400;

verandah.addBox.position  = function(){
  var de = document.documentElement;
  var w = self.innerWidth || (de&&de.clientWidth) || document.body.clientWidth;
  $("#addBox").css({
  	width:verandah.addBox.width+"px",
  	height:verandah.addBox.height+"px",
    left: ((w - verandah.addBox.width)/2)+"px" 
    });
  $("#addBox").css("height",verandah.addBox.height - 32 +"px");
}


verandah.addBox.show = function(content){
	if (! $("#addBox").length > 0){
		$(document.body).append("<div id='addBox_overlay' ></div><div id='addBox'></div>");
		
		$("#addBox_overlay").click(verandah.hide_dialogs);
		$(window).resize(verandah.addBox.position);
	 }

	$("#addBox").html(content);
	$("#addBox_overlay").show();
  	verandah.addBox.position();

	verandah.addBox.visible = true;
    $("#addBox").slideDown("fast");


}

verandah.hide_dialogs = function(){
  $("#addBox,#addBox_overlay").hide();
}


$(document).ready(function(){
	
	$(".day").click(function(){
		verandah.addBox.show($(this).clone());
	}).css('cursor', 'pointer');
	
	
	
});
		
		