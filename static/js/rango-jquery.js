$(document).ready( function(){
	$("#add-text-btn").click( function(event){
		msgstr = $("#example1").html();
		msgstr = msgstr + "...and the button was clicked!";
		$("#example1").html(msgstr);
	})
});

$(document).ready( function(){
	$("#clean-text-btn").click( function(event){
		msgstr = $("#example1").html();
		msgstr = "";
		$("#example1").html(msgstr);
	})
});

$(document).ready(function(){
	$("a").hover(function(){
		$(this).css('color', 'green');
	},
	function(){
		$(this).css('color', '');
	})
});

