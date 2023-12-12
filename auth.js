function authenticateUser() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Replace with your actual authentication credentials
    if (username === 'IoT NSCC' && password === 'Leeds@ 70367') {
        document.getElementById('loginForm').style.display = 'none';
        document.getElementById('fileUploader').style.display = 'block';
        document.getElementById('accessLogSection').style.display = 'block';
        connectToMQTT(); // Proceed to connect to MQTT after successful authentication
    } else {
        alert('Invalid username or password. Please try again.');
    }
}
