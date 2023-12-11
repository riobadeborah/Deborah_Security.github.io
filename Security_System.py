import RPi.GPIO as GPIO
import time
import logging
import paho.mqtt.client as mqtt
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306

# MQTT Broker Details
mqtt_broker = "83e374a4d4df41b5926fac056d1f5340.s1.eu.hivemq.cloud"
mqtt_port = 8883
client_id = "Deborah_Security_System"
mqtt_username = "security_system"
mqtt_password = "Security_system67"
mqtt_topic = "access_input"

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a file handler and set the formatter
handler = logging.FileHandler('access_log.txt')
handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

# Add the handler to the logger
logger.addHandler(handler)

# Row and column pin numbers definition
row_pins = [18, 23, 24, 25]  # GPIO pin numbers for rows
col_pins = [12, 16, 20, 21]  # GPIO pin numbers for columns
trigger_pin = 17  # GPIO pin number for the trigger
green_bulb = 22  # GPIO pin number for the green bulb
red_bulb = 27  # GPIO pin number for the red bulb

# Define the keypad layout
keypad = [['1', '2', '3', 'A'],
          ['4', '5', '6', 'B'],
          ['7', '8', '9', 'C'],
          ['*', '0', '#', 'D']]

# Set up GPIO
GPIO.setmode(GPIO.BCM)  # set the pin numbering mode to BCM

for pin in row_pins:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for pin in col_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

GPIO.setup(trigger_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(green_bulb, GPIO.OUT)
GPIO.setup(red_bulb, GPIO.OUT)

# Initialize the OLED display
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=32, rotate=0)

# MQTT on_connect callback
def on_connect(client, userdata, flags, rc, properties=None):
    logger.info("Connected to MQTT Broker with result code: %s", rc)

# MQTT on_disconnect callback
def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.warning("Unexpected disconnection from MQTT Broker")

# Initialize MQTT client
mqtt_client = mqtt.Client(client_id=client_id, protocol=mqtt.MQTTv5)
mqtt_client.username_pw_set(mqtt_username, mqtt_password)
mqtt_client.tls_set()  # Use TLS for a secure connection
mqtt_client.connect(mqtt_broker, mqtt_port, keepalive=60)
mqtt_client.on_connect = on_connect
mqtt_client.on_disconnect = on_disconnect

# Function to detect the key pressed
def detect_key():
    pin = ''
    pin_length = 4

    # Loop to collect 4-digit PIN
    while len(pin) < pin_length:
        # Loop over columns
        for j in range(4):
            GPIO.output(col_pins[j], GPIO.LOW)

            # Loop over rows
            for i in range(4):
                if not GPIO.input(row_pins[i]):
                    key = keypad[i][j]
                    pin += key
                    while not GPIO.input(row_pins[i]):  # Wait for button release
                        pass
                    with canvas(device) as draw:
                        draw.text((0, 0), "Please Enter PIN: {}".format("*" * len(pin)), fill="white")  # Show "*" for each entered digit

            GPIO.output(col_pins[j], GPIO.HIGH)

        time.sleep(0.3)  # Delay to debounce the button

    return pin

# Loop to display text on the OLED display
try:
    mqtt_client.loop_start()

    while True:
        if not GPIO.input(trigger_pin):
            with canvas(device) as draw:
                draw.text((0, 0), "Please Enter PIN", fill="white")

            pin = detect_key()

            with canvas(device) as draw:
                draw.text((0, 0), "PIN Entered: {}".format(pin), fill="white")

            # Log the time and PIN entered using the logger
            logger.info('PIN Entered: %s', pin)

            # Publish the PIN and timestamp to the MQTT topic
            payload = f'{time.strftime("%Y-%m-%d %H:%M:%S")} - PIN: {pin}'
            mqtt_client.publish(mqtt_topic, payload, qos=1, retain=False)

            if pin == '3340':
                with canvas(device) as draw:
                    draw.text((0, 20), "Access Granted", fill="white")
                GPIO.output(green_bulb, GPIO.HIGH)  # Turn on the green bulb
                GPIO.output(red_bulb, GPIO.LOW)  # Turn off the red bulb
                time.sleep(5)  # Display the "Access Granted" message for 5 seconds
                GPIO.output(green_bulb, GPIO.LOW)  # Turn off the green bulb after granting access
                GPIO.output(red_bulb, GPIO.LOW)  # Turn off the red bulb after granting access
            else:
                with canvas(device) as draw:
                    draw.text((0, 20), "Access Denied", fill="white")
                GPIO.output(red_bulb, GPIO.HIGH)  # Turn on the red bulb
                GPIO.output(green_bulb, GPIO.LOW)  # Turn off the green bulb
                time.sleep(5)  # Display the "Access Denied" message for 5 seconds
                GPIO.output(green_bulb, GPIO.LOW)  # Turn off the green bulb after denying access
                GPIO.output(red_bulb, GPIO.LOW)  # Turn off the red bulb after denying access

            time.sleep(3)  # Small delay before accepting the next PIN

finally:
    GPIO.cleanup()  # Clean up GPIO pins
    device.clear()  # Clear the OLED display
    mqtt_client.disconnect()
    mqtt_client.loop_stop()
