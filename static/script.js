var socket = io.connect('http://' + document.domain + ':' + location.port);

function setPumpTrigger() {
  var pumpTriggerValue = document.getElementById('pump_trigger').value;
  socket.emit('set_pump_trigger', { 'pump_trigger': pumpTriggerValue });
}

socket.on('sensor_update', function(data) {
  document.getElementById('temperature').innerHTML = 'Temperature: ' + data.temperature + '°C';
  document.getElementById('humidity').innerHTML = 'Humidity: ' + data.humidity + '%';
  document.getElementById('moisture').innerHTML = 'Moisture: ' + data.moisture + '%';
});

socket.on('pump_status', function(data) {
  var pumpStatusElement = document.getElementById('pump_status');
  pumpStatusElement.innerHTML = 'Pump Status: ' + (data.pump_status ? 'ON' : 'OFF');
  pumpStatusElement.style.color = data.pump_status ? 'green' : 'red';
});

socket.on('moisture_history', function(data) {
  var moistureHistory = data.moisture_history;
  var ctx = document.getElementById('moisture_chart').getContext('2d');

  // Check if a chart already exists
  if (typeof chart !== "undefined") {
    chart.data.labels.push(moistureHistory.length); // Update labels (assuming timestamps or sample numbers are received)
    chart.data.datasets[0].data.push(moistureHistory[moistureHistory.length-1]); // Update data with latest value
    chart.update(); // Update the chart
  } else {
    // If no chart exists, create a new one with initial data
    chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: Array.from({ length: moistureHistory.length }, (_, i) => i + 1),
        datasets: [{
          label: 'Moisture Level',
          data: moistureHistory,
          borderColor: 'blue',
          borderWidth: 1,
          fill: false,
        }]
      },
      options: {
        scales: {
          x: {
            type: 'linear',
            beginAtZero: true
          },
          y: {
            type: 'linear',
            beginAtZero: true
          }
        }
      }
    });
  }
});
