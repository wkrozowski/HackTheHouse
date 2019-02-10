  function updateDashboard(data) {

    $('#TemperatureIn').text(data['TemperatureIn']);
    $('#TemperatureOut').text(data['TemperatureOut']);
    $('#humidity').text(data['Humidity']);

  }


jQuery(document).ready(function() {
  
  if (typeof google === 'object' && typeof google.maps === 'object') {
    markers['robot'].setVisible(true);
    fitMap();
  }
});
  