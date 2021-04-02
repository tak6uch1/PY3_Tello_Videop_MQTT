# coding=utf8
import paho.mqtt.client as mqtt
import cv2
import base64
import numpy as np
from pygame.locals import *
import pygame
import time
import sys
import termios

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
try:
    joy = pygame.joystick.Joystick(0)
    joy.init()
except:
    joy = None;

pygame.event.get()
WAIT = 0.3
input_flg = True
start_time = 0.0

def send_command(msg):
    print(msg);
    client.publish("Tello-Control/command", msg, 0, True)

while True:
    cv2.imshow("Stream", frame)

    if joy != None:
        if input_flg:
            if joy.get_button(8):
                input_flg = False
                start_time = time.time()
                send_command("Land")
            elif joy.get_button(9):
                input_flg = False
                start_time = time.time()
                send_command("Take off")
            elif joy.get_button(4):
                input_flg = False
                start_time = time.time()
                send_command("Rotate counterclockwise")
            elif joy.get_button(5):
                input_flg = False
                start_time = time.time()
                send_command("Rotate clockwise")
            elif joy.get_button(1):
                input_flg = False
                start_time = time.time()
                send_command("Down")
            elif joy.get_button(3):
                input_flg = False
                start_time = time.time()
                send_command("Up")
            elif joy.get_button(0):
                input_flg = False
                start_time = time.time()
                send_command("Flip left")
            elif joy.get_button(2):
                input_flg = False
                start_time = time.time()
                send_command("Flip right")
            elif joy.get_button(7):
                input_flg = False
                start_time = time.time()
                send_command("Flip forward")
            elif joy.get_button(6):
                input_flg = False
                start_time = time.time()
                send_command("Flip back")
        
            hat = joy.get_hat(0);
            lr = hat[0];
            if lr < -0.5:
                input_flg = False
                start_time = time.time()
                send_command("Left")
            elif lr > 0.5:
                input_flg = False
                start_time = time.time()
                send_command("Right")
        
            fb = hat[1];
            if fb < -0.5:
                input_flg = False
                start_time = time.time()
                send_command("Back")
            elif fb > 0.5:
                input_flg = False
                start_time = time.time()
                send_command("Forward")
        elif time.time() - start_time > WAIT:
            input_flg = True

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_UP:
                send_command("Forward")
            elif event.key == K_DOWN:
                send_command("Back")
            elif event.key == K_LEFT:
                send_command("Left")
            elif event.key == K_RIGHT:
                send_command("Right")
            elif event.key == K_w:
                send_command("Up")
            elif event.key == K_s:
                send_command("Down")
            elif event.key == K_a:
                send_command("Rotate counterclockwise")
            elif event.key == K_d:
                send_command("Rotate clockwise")
            elif event.key == K_t:
                send_command("Take off")
            elif event.key == K_l:
                send_command("Land")
            elif event.key == K_z:
                send_command("Flip left")
            elif event.key == K_x:
                send_command("Flip forward")
            elif event.key == K_c:
                send_command("Flip back")
            elif event.key == K_v:
                send_command("Flip right")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client.loop_stop()

