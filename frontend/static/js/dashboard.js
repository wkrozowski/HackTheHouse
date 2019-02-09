  function updateDashboard(data) {

    var pathPercentage = parseInt(data['status'][1]) + '%';

    $('#status .info-box-number').text(data['status'][0]);
    $('#status .progress-bar').css('width', pathPercentage);
    $('#status .progress-description').text(pathPercentage.toString() + ' of path done');

    var batteryPercentage = parseInt(data['battery'][0]) + '%';
    $('#battery .info-box-number').text(batteryPercentage);
    $('#battery .progress-bar').css('width', batteryPercentage);
    $('#battery .progress-description').text('estimated time: ' + data['battery'][1].toString() + ' minutes');

    $('#something .info-box-number').text(data['something'][0].toFixed(2));

    $(".motors .info-box-content").each(function( index ) {
      
      $(this).find('.info-box-number').text(data['motors'][index][1].toFixed(2));
      $(this).find('.progress-description').text(data['motors'][index][0]);
    });

    changePosition('robot', getLatLong(data.actual_position));
  }


jQuery(document).ready(function() {
  
  if (typeof google === 'object' && typeof google.maps === 'object') {
    markers['robot'].setVisible(true);
    fitMap();
  }
});
  