var map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

var startMarker = L.marker([0, 0], { draggable: true, opacity: 0 }).addTo(map);
var destinationMarker = L.marker([0, 0], { draggable: true, opacity: 0 }).addTo(map);
var routeLayer = L.layerGroup().addTo(map);

var timerId;  // متغير لتخزين معرف setTimeout الحالي

function calculateDistance() {
  // إلغاء التوقيت القديم إذا كان معرف setTimeout معرفًا
  if (timerId) {
    clearTimeout(timerId);
    timerId = null; // تحديث قيمة timerId إلى فارغة
  }

  var startLocation = document.getElementById('startLocation').value;
  var destination = document.getElementById('destination').value;

  if (startLocation.trim() === '' || destination.trim() === '') {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Please enter pick-up point and destination.',
    });
    return;
  }

  getCoordinatesNominatim(startLocation, function (startCoords) {
    getCoordinatesNominatim(destination, function (destCoords) {
      startMarker.setLatLng(startCoords).setOpacity(1);
      destinationMarker.setLatLng(destCoords).setOpacity(1);

      var distance = startMarker.getLatLng().distanceTo(destinationMarker.getLatLng()) / 1000;
      var price = calculatePrice(distance);

      document.getElementById('distanceResult').innerHTML = 'Distance: <br>' + distance.toFixed(3) + ' kilometers';
      document.getElementById('priceResult').innerHTML = 'Price: <br>' + price.toFixed(3) + ' Syrian Pounds';

      startTimer(distance);

      drawRoute(startCoords, destCoords);
      fitMapBounds(startCoords, destCoords);
    });
  });
}

function calculatePrice(distance) {
  var pricePerKilometer = 4000;
  var kilometersPerPriceUnit = 1;

  var totalPrice = (Math.ceil(distance / kilometersPerPriceUnit) * pricePerKilometer);
  return totalPrice;
}

function startTimer(distance) {
  var timerElement = document.getElementById('timer');

  // Assuming 3 minutes per kilometer
  var speedInSecondsPerKilometer = 60; // 3 minutes = 180 seconds
  var durationInSeconds = Math.ceil(distance * speedInSecondsPerKilometer);

  function updateTimer() {
    var hours = Math.floor(durationInSeconds / 3600);
    var minutes = Math.floor((durationInSeconds % 3600) / 60);
    var seconds = durationInSeconds % 60;

    timerElement.innerHTML = 'Time: <br>' + hours + ' hours ' + minutes + ' minutes ' + seconds + ' seconds';

    if (--durationInSeconds >= 0) {
      timerId = setTimeout(updateTimer, 1000);
    } else {
      timerElement.innerHTML = 'Time: <br>Arrived';
    }
  }

  updateTimer();
}

function getCoordinatesNominatim(address, callback) {
  fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`)
    .then(response => response.json())
    .then(data => {
      if (data && data.length > 0) {
        var coords = [parseFloat(data[0].lat), parseFloat(data[0].lon)];
        callback(coords);
      } else {
        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Address not found.',
        });
      }
    })
    .catch(error => console.error('Error connecting to Nominatim service', error));
}

function drawRoute(startCoords, destCoords) {
  var route = L.polyline([startCoords, destCoords], { color: 'blue', weight: 5, opacity: 0.7 });
  routeLayer.clearLayers();
  routeLayer.addLayer(route);
}

function fitMapBounds(startCoords, destCoords) {
  var bounds = L.latLngBounds([startCoords, destCoords]);
  map.fitBounds(bounds);
}

function getCurrentLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function(position) {
        var currentCoords = [position.coords.latitude, position.coords.longitude];
        document.getElementById('startLocation').value = currentCoords.join(', ');

        Swal.fire({
          icon: 'success',
          title: 'Success',
          text: 'Current location set as Start Location.',
        });
      },
      function(error) {
        console.error('Error getting current location:', error);

        Swal.fire({
          icon: 'error',
          title: 'Error',
          text: 'Failed to get current location.',
        });
      }
    );
  } else {
    Swal.fire({
      icon: 'error',
      title: 'Error',
      text: 'Geolocation is not supported by your browser.',
    });
  }
}
