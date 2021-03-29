# Copyright (c) 2021 Takenoshin
# Released under the MIT license
# https://opensource.org/licenses/mit-license.php

import time
from decimal import Decimal
import pygame

def tello_joy():
    pygame.init()
    joy = pygame.joystick.Joystick(0)
    joy.init()
    try:
        n_btn = joy.get_numbuttons()
        n_axe = joy.get_numaxes()
        n_hat = joy.get_numhats()
        print("Joystick Name: " + joy.get_name())
        print("Number of Button : " + str(n_btn))
        print("Number of Axis : " + str(n_axe))
        print("Number of Hats : " + str(n_hat))

        pygame.event.get()
        sent_com = 0
        while True:
            if joy.get_button(1):
                sent_com = 1
                print("Land");
            elif joy.get_button(3):
                sent_com = 1
                print("Take off");
            elif joy.get_button(4):
                sent_com = 1
                print("Rotate counterclockwise");
            elif joy.get_button(5):
                sent_com = 1
                print("Rotate clockwise");

            hat = joy.get_hat(0);
            lr = hat[0];
            if lr < -0.5:
                sent_com = 1
                print("Left");
            elif lr > 0.5:
                sent_com = 1
                print("Right");

            fb = hat[1];
            if fb < -0.5:
                sent_com = 1
                print("Back");
            elif fb > 0.5:
                sent_com = 1
                print("Forward");

            if sent_com:
                sent_com = 0
                time.sleep(0.3)
            else:
                time.sleep(0.01)

            pygame.event.get()
    except( KeyboardInterrupt, SystemExit): # Exit with Ctrl-C
        print("Exit")

if __name__ == "__main__":
    tello_joy()
