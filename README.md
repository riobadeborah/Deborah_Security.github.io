# Deborah_Security.github.io
# Deborah Security System

## Description

This project implements a security system on a Raspberry Pi using a keypad, an OLED display, and MQTT communication. The system logs access events and publishes PIN entries to an MQTT broker, providing visual feedback using LEDs and an OLED display.

## Prerequisites

- Raspberry Pi with GPIO pins
- Python 3 installed
- Paho MQTT library installed (`pip install paho-mqtt`)
- luma-oled library installed (`pip install luma-oled`)

## Installation

1. Clone this repository to your Raspberry Pi:

    ```bash
    https://github.com/riobadeborah/Deborah_Security.github.io.git
    ```

2. Navigate to the project directory:

    ```bash
    cd security-system
    ```

3. Run the Python script:

    ```bash
    python3 security_system.py
    ```

## Configuration

Make sure to update the following configurations in the `security_system.py` script:

- MQTT broker details (`mqtt_broker`, `mqtt_port`, `mqtt_username`, `mqtt_password`, `mqtt_topic`).
- Adjust GPIO pin numbers if necessary.
- Update OLED display initialization parameters.

## Usage

- Run the script manually using:

    ```bash
    python3 security_system.py
    ```

- To run the script at startup, follow the instructions in the [How to Run at Startup](#how-to-run-at-startup) section.


## Contributing

If you'd like to contribute, please fork the repository and create a new branch. Pull requests are welcome!
