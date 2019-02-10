  function updateDashboard(data) {

    $('#TemperatureIn').text(data['TemperatureIn']);
    $('#TemperatureOut').text(data['TemperatureOut']);
    $('#humidity').text(data['Humidity']);

    if('fingerprint' in data) {

      if(data['fingerprint'][1] == 1) {
        $.notify(data['fingerprint'][0] + ' enter the building!', 'success');
      }
    }
  }


jQuery(document).ready(function() {
  
  if (typeof google === 'object' && typeof google.maps === 'object') {
    markers['robot'].setVisible(true);
    fitMap();
  }
});
  