  function updateDashboard(data) {

    $('#TemperatureIn').text(data['TemperatureIn']);
    $('#TemperatureOut').text(data['PPM']);
    $('#humidity').text(data['Humidity']);

    if(parseFloat(data['Distance']) > 200) {
      $('#car').text('Away');
    } else {
      $('#car').text('Present');
    }
    if('fingerprint' in data) {

      if(data['fingerprint'][1] == 1) {
        $.notify(data['fingerprint'][0] + ' enter the building!', 'success');
      }
    }
  }
