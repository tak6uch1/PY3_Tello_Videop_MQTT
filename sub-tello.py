# coding=utf8
import paho.mqtt.client as mqtt
import cv2
import base64
import numpy as np

#frame = np.zeros((720, 960, 3), np.uint8)
#frame = np.zeros((240, 320, 3), np.uint8)
frame = np.zeros((120, 160, 3), np.uint8)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("Tello-Video/jpg-image")

def on_message(client, userdata, msg):
    global frame
    # Decoding the message
    img = base64.b64decode(msg.payload)
    # converting into numpy array from buffer
    npimg = np.frombuffer(img, dtype=np.uint8)
    # Resize
    #npimg = cv2.resize(npimg, dsize=(960, 720))
    # Decode to Original Frame
    frame = cv2.imdecode(npimg, 3)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set("mosquitto.org.crt")
client.connect("test.mosquitto.org", 8883)

#client.loop_forever()
client.loop_start()

while True:
    cv2.imshow("Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client.loop_stop()

