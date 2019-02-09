  


  function sendPost(data, url, success_function = function(){}, error_function = function() {}) {
   
    $.ajax({
      url: url,
      data: data,
      dataType: 'json',
      type: 'POST',
      error: function() {
        error_function();
      },
      success: function(data) {
        success_function(data);
      },

    });

  }

  function refreshing(repeatFunction, time) {
    setInterval(function(){repeatFunction();}, time);
  }