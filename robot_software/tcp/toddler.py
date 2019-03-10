import time
import numpy
import cv2
import sys
import socket
from threading import Thread
from rasppi_coordinator import RobotJobListener
from iotools import IOTools

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

class Toddler:

	def __init__(self, onRobot):
		IO = IOTools()
		print('Grabber initialised')
		self.camera = IO.camera.initCamera('pi', 'low')
		self.getInputs = IO.interface_kit.getInputs
		self.getSensors = IO.interface_kit.getSensors
		self.mc = IO.motor_control
		self.sc = IO.servo_control

	def listen(self):
		PORT = 65432 # Port to listen on (non-privileged ports are > 1023)

		s =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		HOST  = socket.gethostbyname(socket.gethostname())
		s.bind((HOST, PORT))
		print("Socket listening on {}:{}".format(HOST,PORT))
		s.listen(1)
		conn, addr = s.accept()
		with conn:
			print('Connected by', addr)
			while True:
				data = conn.recv(1024)
				print('Socket data' + data)
				if data:
					self.grabber()
					conn.sendall(b'done')
	
	def control(self):
		try:
			thread = Thread(target = self.listen)
			thread.start()

		# start pinging the server
		# server, rasppi, ev3
		
			rjl = RobotJobListener(['192.168.105.38',9000],['192.168.105.139',65432],['192.168.105.94',65432])
			rjl.listen_to_server('robot')
		except KeyboardInterrupt:
			return

	def grabber(self):
		print('{}\t{}'.format(self.getSensors(), self.getInputs()))
		self.mc.setMotor(0, 100)
		self.sc.engage()
		self.sc.setPosition(0)
		time.sleep(2)
		self.sc.setPosition(90)
		time.sleep(2)
		self.sc.setPosition(180)
		time.sleep(2)

	def vision(self):
	   # image = self.camera.getFrame()
	   # self.camera.imshow('Camera', image)
		time.sleep(0.05)
		return

if __name__ == '__main__':
	onRobot = bool(sys.argv.count('-rss'))
    sys.stdout = Logger(onRobot)
    sys.stderr = sys.stdout
    t = Toddler(onRobot)
