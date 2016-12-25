$(document).ready( function(){
	$('#likes').click( function(){
		var catid;
		catid = $(this).attr("data-catid");
		$.get('/rango/like/', {'category_id': catid}, function(data){
			$('#like_count').html(data);
			$('#likes').hide();
		})
	})
})

$(document).ready(function(){
	$('#suggestion').keyup(function(){
		var query;
		query = $(this).val();

		$.get('/rango/suggest/', {'suggestion':query}, function(data){
			$('#cats').html(data);
		})
	})
})


$(document).ready(function(){
	$('.rango-add').click(function(){
		
		var bt = $(this);
		var dict = {};
		var catid = bt.attr("data-catid");
		var page_title = bt.attr("data-page-title");
		var page_url = bt.attr("data-page-url");
		dict['catid'] = catid;
		dict['page_url'] = page_url;
		dict['page_title'] = page_title;

	
		$.get('/rango/add_page/',
				dict, function(data){

			bt.hide();
			$("#pages").html(data);

		});
	
	
})
})
