# Tello Remote Control Environment with Tello-Video and MQTT

This repository gives you an example to control Tello remotely through the Internet with using video and gamepad.

## MQTT Broker
This repository uses test.mosquitto.org for MQTT broker.
Users have to download mosquitto.org.crt(PEM format) from the site.

## Requirements
- Mac
- Python3 environment (Recommend Anaconda)
- Pillow, opencv, paho-mqtt, pygame
- H.264 decoder, shared object .so, for Tello-Video
  https://github.com/f41ardu/Tello-Python
- Logicool Wireless Gamepad F710
