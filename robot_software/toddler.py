import time
import numpy
import cv2
import sys
import os
import socket
from threading import Thread
from iotools import IOTools
from grabber import Grabber
from lift import Lift
from rasppi_coordinator import RobotJobListener
from rasppi_listener import listen


class Logger(object):
    def __init__(self, onRobot):
        self.useTerminal = not onRobot
        self.terminal = sys.stdout
        self.log = 0
        if os.path.isdir('/tmp/sandbox'):
            self.log = open('/tmp/sandbox/log.txt', 'a+')

    def write(self, message):
        if self.useTerminal:
            self.terminal.write(message)
        if self.log:
            self.log.write(message)
            self.log.flush()

    def flush(self):
        pass


halt = {'stop': False}


class Toddler:
    MOTOR_PORT = 1
    BUMP_SENSOR_SHELF_1 = 0
    BUMP_SENSOR_SHELF_2 = 1
    BUMP_SENSOR_GRABBER_FRONT = 2
    BUMP_SENSOR_GRABBER_BACK = 3

    def __init__(self, onRobot):
        IO = IOTools(onRobot)
        print('Grabber initialised')
        self.camera = IO.camera.initCamera('pi', 'low')
        self.getInputs = IO.interface_kit.getInputs
        self.getSensors = IO.interface_kit.getSensors
        self.mc = IO.motor_control
        self.mc.stopMotors()
        self.sc = IO.servo_control
        self.sc.engage()
        self.grabber = Grabber(self.mc, self.MOTOR_PORT, self.sc)
        #self.grabber.prepare_grabber()
        self.lift = Lift(onRobot, self.mc)
       
        
        
        self.lift_pos = 0
        self.s = None
        # self.mc.setMotor(self.MOTOR_PORT, 100)
        # time.sleep(3)
        # self.mc.stopMotors()

    def kill_socket(self):
        s.close()

    def listen(self):
        global halt
        try:
            PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # HOST = socket.gethostbyname(socket.gethostname())
            HOST = '192.168.105.139'
            self.s.bind(('192.168.105.139', PORT))
            print("Listening on {}:{}".format(HOST, PORT))

            self.s.listen(1)
            conn, addr = self.s.accept()
            while not (halt['stop']):

                data = conn.recv(1024)
                data = data.decode('utf-8')
                data = data.split(' ')
                print("Listen: " + data[0])
                if data[0] == 'grab':
                    self.grabber.grab(self)
                elif data[0] == 'upper_grab':
                    self.grabber.upper_grab(self)
                elif data[0] == 'prepare':
                    self.grabber.prepare_grabber()
                elif data[0] == 'retract':
                    self.grabber.retract_grabber()
                elif data[0] == 'wait_for_bump':
                    inp = self.getInputs()
                    while inp[self.BUMP_SENSOR_SHELF_1] == 0 or inp[self.BUMP_SENSOR_SHELF_2] == 0:
                        print(inp)
                    print("bump")
                elif data[0] == 'lift':
                    if int(data[1]) < self.lift_pos:
                        print('down')
                        self.lift.lift('down')
                    elif int(data[1]) > self.lift_pos:
                        print('up')
                        self.lift.lift('up')
                    self.lift_pos = int(data[1])
                    time.sleep(0.5)
                elif data[0] == 'drop':
                    self.grabber.prepare_grabber()
                    while inp[self.BUMP_SENSOR_GRABBER_BACK] == 0:
                        print('Waiting for collection')
                    self.grabber.retract_grabber()
                print("Listen done")
                conn.sendall(b'done')
            conn.close()
        except KeyboardInterrupt:
            conn.close()
            return

    def control(self):
        global halt

        try:
            thread = Thread(target=self.listen)
            thread.daemon = True
            thread.start()
            print("here")
            rjr = RobotJobListener(('192.168.105.38', 9000), ('192.168.105.139', 65432), ('192.168.105.94', 65433))
            rjr.start_reliable_listener('robot')
            # start pinging the server
            # server, rasppi, ev3
        except KeyboardInterrupt:
            halt['stop'] = True
            self.sc.disengage()
            return

    def vision(self):
        # image = self.camera.getFrame()
        # self.camera.imshow('Camera', image)
        time.sleep(0.05)
        return


if __name__ == '__main__':
    onRobot = bool(sys.argv.count('-rss'))
    sys.stdout = Logger(onRobot)
    sys.stderr = sys.stdout
    try:
        t = Toddler(onRobot)
        t.control()
    except KeyboardInterrupt:

        t.kill_socket()
