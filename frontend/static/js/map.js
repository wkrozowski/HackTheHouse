
var map;

var markers;

var bounds; 

var directionsService

var directionsDisplay

var colours = ['#e6194b', '#3cb44b', '#ffe119', '#0082c8', '#f58231', '#911eb4'];

function initMap (startPosition={lat: 50.939618, lng: -1.397233}) {

	directionsService = new google.maps.DirectionsService;
  	directionsDisplay = new google.maps.DirectionsRenderer({suppressMarkers: true});

	map = new google.maps.Map(document.getElementById('map-control'), {
		zoom: 15,
		center: startPosition,
		keyboardShortcuts: false,
	});

	directionsDisplay.setMap(map);


	markers = {

		'robot': new google.maps.Marker({
			position: startPosition,	
			map: map,
			icon: '/static/images/robot-marker.png',
			visible: false
		}),

		'start': new google.maps.Marker({
			position: startPosition,	
			map: map,
			icon: '/static/images/start-marker.png',
			visible: false
		}),

		'finish': new google.maps.Marker({
			position: startPosition,	
			map: map,
			icon: '/static/images/finish-marker.png',
			visible: false
		})
	}
}



function changePosition(marker, position, fit=false) {

	markers[marker].setPosition(position); 

	if(fit) fitMap();
}


function fitMap () {
	var bounds = new google.maps.LatLngBounds();
	
	map.setCenter(markers['robot'].getPosition());	

	$.each(markers, function(index, value) {
	 	
	 	if(value.visible) {

	 		bounds.extend(value.getPosition());
 		}

	});

	map.fitBounds(bounds);
}

var path;
function drawPath(coords, colour='#FFF000', clear=false) {
    if (path != null && clear) {
    	path.setMap(null);
 	}
    path = new google.maps.Polyline({
		path: coords,
		geodesic: true,
		strokeColor: colour,
		strokeOpacity: 1.0,
		strokeWeight: 2
    });

    path.setMap(map);
	
	var bounds = new google.maps.LatLngBounds();
    path.getPath().forEach(function(e) {
		bounds.extend(e);
  	});

    map.fitBounds(bounds);
}

function getLatLong(coords) {
	return {lat: coords[0], lng: coords[1]};
}

function calcRoute(start, end) {
if (path != null ) path.setMap(null);
	var start = getLatLong(start);
	var end = getLatLong(end);

	var request = {
		origin: start,
		destination: end,
		travelMode: 'WALKING'
	};
	directionsService.route(request, function(result, status) {
	if (status == 'OK') {
	  directionsDisplay.setDirections(result);
	}
	});
}