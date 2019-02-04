#!/usr/bin/env python

import time
from lineFollower import LineFollower

class Toddler:

    MOTOR_SIDE = 1
    MOTOR_FRONT_LEFT = 2
    MOTOR_FRONT_RIGHT = 3

    def __init__(self, IO):
        print('[Toddler] I am toddler playing in a sandbox')
        self.camera = IO.camera.initCamera('pi', 'low')
        self.getInputs = IO.interface_kit.getInputs
        self.getSensors = IO.interface_kit.getSensors
        self.mc = IO.motor_control
        self.sc = IO.servo_control
        self.follower = LineFollower(IO)

    def control(self):
        print('{}\t{}'.format(self.getSensors(), self.getInputs()))
        # self.mc.setMotor(self.MOTOR_FRONT_LEFT, 1)
        # self.mc.setMotor(self.MOTOR_FRONT_RIGHT, 1)
        self.follower.motor_speed()
        time.sleep(0.5)

    def vision(self):
        image = self.camera.getFrame()
        self.camera.imshow('Camera', image)
        time.sleep(0.05)