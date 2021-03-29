# coding=utf8
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set("mosquitto.org.crt")
client.connect("test.mosquitto.org", 8883)

while client.loop() == 0:
    msg = "TIME: "+time.ctime()
    client.publish("Tello-Control/command", msg, 0, True)
    print(msg)
    time.sleep(1.5)
    pass
