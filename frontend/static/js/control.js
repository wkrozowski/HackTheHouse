jQuery(document).ready(function() {

  $('.middle').click(function() {
      $('.toggle-inactive, .toggle-active').toggle();
  });

	$('.sort-list li').click(function() {

		var cl = $(this).attr('class');

		var attr = $('.to-hide');

  		if( cl == 'hide'){
  			attr.css('visibility','hidden');
  		} else {
  			attr.css('visibility','visible');
  		}
 	});

  $(document).on('mouseup', '.arrow', function(e) {
    releaseArrow($(this).attr('id'));
  })

  $(document).on('mousedown', '.arrow', function(e) {
    clickArrow($(this).attr('id'));
  });

  $(document).keydown(function(e) {


    if(checkButton(e)) clickArrow(arrows[e.keyCode]);
    e.preventDefault();
    e.stopPropagation();
  });

  $(document).keyup(function(e) {

    if(checkButton(e)) releaseArrow(arrows[e.keyCode]);

  })

  data = JSON.parse(data);
  markers['robot'].setVisible(true);
  changePosition('robot', getLatLong(data.actual_position));


  function updateLog(data) {
    var element = $('<div/>', {
        'class':'box-top',
    });

    $('<span/>', {'class': 'box-type-sm2', 'text': data[0]}).appendTo(element);
    $('#logs').prepend(element);
  }

  if(data.status == 'running') {
    markers['finish'].setVisible(true);
    markers['start'].setVisible(true);

    var repeatFuntion = function() { sendPost({'id': data.route}, 'get_log', function(data){updateLog(data);})};

    refreshing(repeatFuntion, 1000);

  }

  map.addListener('click', function(event) {

    if($('#status').text() == 'running') return;
    changePosition('finish', event.latLng);
    markers['finish'].setVisible(true);

    $('#finishLatLong .input-filter').eq(0).val(event.latLng.lat)
    $('#finishLatLong .input-filter').eq(1).val(event.latLng.lng)

    if($('.toggle-active').is(":visible")) {
      calcRoute([markers['robot'].getPosition().lat(), markers['robot'].getPosition().lng()], [markers['finish'].getPosition().lat(), markers['finish'].getPosition().lng()]);
    } else {
      var first = getLatLong([markers['robot'].getPosition().lat(), markers['robot'].getPosition().lng()]);
      var second = getLatLong([markers['finish'].getPosition().lat(), markers['finish'].getPosition().lng()]);
      drawPath([first, second], '#FFF000', true)
    }
  });

  $(document).on('input change', '#formControlRange', function() {
    $('#speed').html($(this).val());   
  });

  $('#formControlRange').change(function () {

    var data = {speed: $(this).val()};
    sendPost(data, 'set_control');
  })

  $('#button-stop').on('click', function() {

    sendPost({'move': 1}, 'set_control');
  });

});

function sendButton(value, mode) {

  var data = {
    direction: [value, mode]
  };

  sendPost(data, 'set_control');
}

var arrows = {
  37: 'L',
  38: 'F',
  39: 'R',
  40: 'B'
};

var buttonPressed = false;

function clickArrow(direction) {
  if(!buttonPressed) {
    $('#' + direction).css('color', 'green');
    sendButton(direction, 'press');
    buttonPressed = true;
  }
}

function releaseArrow(direction) {
  $('#' + direction).css('color', '#343a40');
  sendButton(direction, 'release');
  buttonPressed = false;
}

function checkButton(e) {
  var buttonCode = e.keyCode;

  return (buttonCode > 36 && buttonCode < 41);
}

