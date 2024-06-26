// main.js
var client; // Declare client globally
var accessLog = []; // Array to store access log locally

// Connect to the MQTT broker and subscribe to the topic
function connectToMQTT() {
  client = mqtt.connect('wss://83e374a4d4df41b5926fac056d1f5340.s1.eu.hivemq.cloud:8883');

  client.on('connect', function () {
    console.log('Connected to MQTT broker');
    client.subscribe('access_input');
  });

  client.on('message', function (topic, message) {
    console.log('Received message:', message.toString());
    
    // Handle the received message as needed
    document.getElementById('fileContent').textContent = message.toString();
    
    // Add the message to the list
    var messageList = document.getElementById('messageList');
    var listItem = document.createElement('li');
    listItem.appendChild(document.createTextNode(message.toString()));
    messageList.appendChild(listItem);

    // Update the local access log array
    accessLog.push(message.toString());

    // Update the displayed access log
    updateAccessLogDisplay();
  });
}

// Call the connectToMQTT function when the page loads
window.onload = function () {
  // Load access log from local storage
  var storedLog = localStorage.getItem('accessLog');
  if (storedLog) {
    accessLog = JSON.parse(storedLog);
    updateAccessLogDisplay();
  }
};
