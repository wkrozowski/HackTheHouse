jQuery(document).ready(function() {

	var i = 0;

	$.each(JSON.parse(routes), function (key, element) {

		var path = [];
		$.each(element['coords'], function(index, coords) {
			path.push(new google.maps.LatLng(coords[0], coords[1]));
		});


		var colour = colours[i];
		drawPath(path, colour);

		$('.box-list .rating').eq(i++).css('color', colour);
	});

});