
class Grabber():
	RETRACT_ANGLE = 180
	PREPARE_ANGLE = 0
	GRAB_ANGLE = 180

	MC_SPEED = 90  # speed for the outward and inward scoop
	OUTWARD_SCOOP_TIME = 1  # time in seconds for the motor to move towards the shelf


	def __init__(self, mc, mc_id, sc):
		self.mc_id = mc_id
		self.mc = mc
		self.sc.setPosition(self.RETRACT_ANGLE)

	def prepare_grabber(self):
		self.sc.setPosition(self.PREPARE_ANGLE)

	def grab(self):
		self.mc.setMotor(self.mc_id, self.MC_SPEED)
		time.sleep(self.OUTWARD_SCOOP_TIME)
        self.sc.setPosition(self.GRAB_ANGLE)


	print('{}\t{}'.format(self.getSensors(), self.getInputs()))
		self.mc.setMotor(0, 100)
		self.sc.engage()
		self.sc.setPosition(0)
		time.sleep(2)
		self.sc.setPosition(90)
		time.sleep(2)
		self.sc.setPosition(180)
		time.sleep(2)
