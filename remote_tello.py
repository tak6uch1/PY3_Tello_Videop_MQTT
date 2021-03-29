# coding=utf8
import paho.mqtt.client as mqtt
import cv2
import base64
import numpy as np
import pygame
import time

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
    tmp_frame = cv2.imdecode(npimg, 3)
    # Convert RBG to BGR for opencv image
    frame = cv2.cvtColor(tmp_frame, cv2.COLOR_RGB2BGR)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.tls_set("mosquitto.org.crt")
client.connect("test.mosquitto.org", 8883)

client.loop_start()

# Initialize joystick
pygame.init()
joy = pygame.joystick.Joystick(0)
joy.init()

pygame.event.get()
WAIT = 0.3
input_flg = True
start_time = 0.0
while True:
    cv2.imshow("Stream", frame)

    if input_flg:
        if joy.get_button(8):
            input_flg = False
            start_time = time.time()
            msg = "Land"
            print(msg);
            client.publish("Tello-Control/command", msg, 0, True)
        elif joy.get_button(9):
            input_flg = False
            start_time = time.time()
            msg = "Take off"
            print(msg);
            client.publish("Tello-Control/command", msg, 0, True)
        elif joy.get_button(4):
            input_flg = False
            start_time = time.time()
            msg = "Rotate counterclockwise"
            print(msg);
            client.publish("Tello-Control/command", msg, 0, True)
        elif joy.get_button(5):
            input_flg = False
            start_time = time.time()
            msg = "Rotate clockwise"
            print(msg);
            client.publish("Tello-Control/command", msg, 0, True)
        elif joy.get_button(1):
            input_flg = False
            start_time = time.time()
            msg = "Down"
            print(msg);
            client.publish("Tello-Control/command", msg, 0, True)
        elif joy.get_button(3):
            input_flg = False
            start_time = time.time()
            msg = "Up"
            print(msg);
            client.publish("Tello-Control/command", msg, 0, True)
        elif joy.get_button(0):
            input_flg = False
            start_time = time.time()
            msg = "Flip left"
            print(msg);
            client.publish("Tello-Control/command", msg, 0, True)
        elif joy.get_button(2):
            input_flg = False
            start_time = time.time()
            msg = "Flip right"
            print(msg);
            client.publish("Tello-Control/command", msg, 0, True)
        elif joy.get_button(7):
            input_flg = False
            start_time = time.time()
            msg = "Flip forward"
            print(msg);
            client.publish("Tello-Control/command", msg, 0, True)
        elif joy.get_button(6):
            input_flg = False
            start_time = time.time()
            msg = "Flip back"
            print(msg);
            client.publish("Tello-Control/command", msg, 0, True)
    
        hat = joy.get_hat(0);
        lr = hat[0];
        if lr < -0.5:
            input_flg = False
            start_time = time.time()
            msg = "Left"
            print(msg);
            client.publish("Tello-Control/command", msg, 0, True)
        elif lr > 0.5:
            input_flg = False
            start_time = time.time()
            msg = "Right"
            print(msg);
            client.publish("Tello-Control/command", msg, 0, True)
    
        fb = hat[1];
        if fb < -0.5:
            input_flg = False
            start_time = time.time()
            msg = "Back"
            print(msg);
            client.publish("Tello-Control/command", msg, 0, True)
        elif fb > 0.5:
            input_flg = False
            start_time = time.time()
            msg = "Forward"
            print(msg);
            client.publish("Tello-Control/command", msg, 0, True)
    elif time.time() - start_time > WAIT:
        input_flg = True

    pygame.event.get()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client.loop_stop()

