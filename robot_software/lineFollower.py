#!/usr/bin/env python

import time

class LineFollower:

    MOTOR_FRONT_LEFT = 2
    MOTOR_FRONT_RIGHT = 3

    def __init__(self, IO): # can change this to pass in the individual sensors and motors instead of entire IO
        # get the sensors from the phidget board
        self.getSensors = IO.interface_kit.getSensors
        self.left_sensor = self.getSensors()[0]
        self.right_sensor = self.getSensors()[1]
        self.mc = IO.motor_control

    def motor_speed(self):
        while True:
            # Stage 1
            if self.left_sensor == 0 and self.right_sensor == 0:  # change ranges to match sensor values
                # continue straight
                self.mc.setMotor(self.MOTOR_FRONT_LEFT, 1)
                self.mc.setMotor(self.MOTOR_FRONT_RIGHT, 1)
            # Stage 2
            if self.left_sensor == 0 and self.right_sensor == 1:
                # adjust
                self.mc.setMotor(self.MOTOR_FRONT_RIGHT, -1)
            if self.left_sensor == 1 and self.right_sensor == 0:
                self.mc.setMotor(self.MOTOR_FRONT_LEFT, -1)
            #print(r, l)
