var apiKey = 'fad4cac23d331198eba7852ff9ebabf9';

var weatherIcons = {
  //format is api_icon:[weather-icon-font,bg-color-key,font-color]
  'clear-day': ['wi-day-sunny', '#ffff33','#000000'],
  'clear-night': ['wi-night-clear', '#2d2d86','#ffffff'],
  'rain': ['wi-rain', '#003399', '#ffffff'],
  'snow': ['wi-snow','#ccffff', '#000000'],
  'sleet': ['wi-sleet', '#ccffff', '#000000'],
  'wind': ['wi-strong-wind', '#80bfff', '#ffffff'],
  'fog': ['wi-fog', '#248f8f','#000000'],
  'cloudy': ['wi-cloudy', '#8b8b8d','#000000'],
  'partly-cloudy-day': ['wi-day-cloudy', '#ffffcc','#000000'],
  'partly-cloudy-night': ['wi-night-alt-cloudy', '#2d2d86','#ffffff'],
  'hail': ['wi-hail', '#ccffff', '#000000'],
  'thunderstorm': ['wi-storm-showers', '#4b4f4c','#ffffff'],
  'tornado': ['wi-tornado','#ff6600','#000000']
};

function getLocation() {
    if (navigator.geolocation) {
        return navigator.geolocation.getCurrentPosition(function (position) {
          var loc = [position.coords.latitude, position.coords.longitude];

          var LATITUDE = loc[0];
          var LONGITUDE = loc[1];
          var url = 'https://api.forecast.io/forecast/' + apiKey + '/' + LATITUDE + ',' + LONGITUDE;
          console.log(url);
          data = $.ajax({
            type: "GET",
            url: url,
            dataType: 'jsonp',
            success: function(data){
              //console.log(data);
              var icon = data.currently.icon;
              temperature = data.currently.apparentTemperature;
              c_temperature = (temperature-32)*5/9
              var summary = data.currently.summary;
              var icon_to_display = weatherIcons[icon]
              //change background, font and button
              $("body").css('color',icon_to_display[2])
              $("body").css('background-color',icon_to_display[1])
              $("#tempswitch").css('background-color',icon_to_display[1])
              $("#tempswitch").css('border-color',icon_to_display[2])
              $("#icon").removeClass().addClass('wi '+ icon_to_display[0])
              $("#summary").html(summary)
              $('#temperature').html(temperature)
              $('#bottom_text').css('color', icon_to_display[2])
              $('a').css('color', icon_to_display[2])
              $('hr').css('border-color', icon_to_display[2])
            }
          });
        });
    } else {
        console.log("Geolocation is not supported by this browser.");
    }
}

$(document).ready(function() {
  getLocation();
  $('#tempswitch').on('click', function() {
    if ($('#deg').hasClass('wi-fahrenheit')) {
      temp = c_temperature
    } else {
      temp = temperature
    }
    temp = temp.toFixed(2);
    $('#temperature').html(temp);
    $('#deg').toggleClass('wi-fahrenheit wi-celsius')
  })


});
