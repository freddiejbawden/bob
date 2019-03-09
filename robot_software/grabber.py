import time
import numpy
import cv2

class Toddler:

    def __init__(self, IO):
        print('Grabber initialised')
        self.camera = IO.camera.initCamera('pi', 'low')
        self.getInputs = IO.interface_kit.getInputs
        self.getSensors = IO.interface_kit.getSensors
        self.mc = IO.motor_control
        self.sc = IO.servo_control

    def control(self):
        print('{}\t{}'.format(self.getSensors(), self.getInputs()))
        #self.mc.setMotor(0, 100)
        retract_angle = 0
        prepare_angle = 90
        grab_angle = 180

        self.sc.engage()
        self.sc.setPosition(retract_angle)
        time.sleep(5)
        self.sc.setPosition(prepare_angle)
        time.sleep(5)

    def vision(self):
        image = self.camera.getFrame()
        self.camera.imshow('Camera', image)
        time.sleep(0.05)

