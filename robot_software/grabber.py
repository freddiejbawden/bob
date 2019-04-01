import time


class Grabber():
    RETRACT_ANGLE = 180
    PREPARE_ANGLE = 35
    UPPER_GRAB_ANGLE = 110
    GRAB_ANGLE = 180

    MC_SPEED = -100  # speed for the outward and inward scoop
    OUTWARD_SCOOP_TIME = 1.5  # time in seconds for the motor to move towards the shelf
    SERVO_TIME = 1  # time in seconds for the servo to move into position

    def __init__(self, mc, mc_id, sc):
        self.mc_id = mc_id
        self.mc = mc
        self.sc = sc
        self.sc.engage()
        self.sc.setPosition(self.PREPARE_ANGLE)
        time.sleep(self.SERVO_TIME)

    def prepare_grabber(self):
        print("preparing")
        self.sc.setPosition(self.PREPARE_ANGLE)
        time.sleep(self.SERVO_TIME)

    def cycle_grabber(self):
        self.sc.setPosition(30)
        self.sc.setPosition(180)

    def retract_grabber(self):
        print("retracting")
        self.sc.setPosition(self.RETRACT_ANGLE)
        time.sleep(self.SERVO_TIME)

    def grab(self, inputer):
        print('grabbing')
        inp = inputer.getInputs()
        print(inp)
        while inp[3] == 0:
            print(inp)
            inp = inputer.getInputs()
            self.mc.setMotor(self.mc_id, self.MC_SPEED)
        self.mc.stopMotors()
        time.sleep(1)

        self.sc.setPosition(self.GRAB_ANGLE)

        time.sleep(self.SERVO_TIME)
        while inp[2] == 0:
            print(inp)
            inp = inputer.getInputs()
            self.mc.setMotor(self.mc_id, -self.MC_SPEED)
        self.mc.stopMotors()

    def upper_grab(self, inputer):
        print('grabbing but higher')
        inp = inputer.getInputs()
        print(inp)
        while inp[3] == 0:
            print(inp)
            inp = inputer.getInputs()
            self.mc.setMotor(self.mc_id, self.MC_SPEED)
        self.mc.stopMotors()
        time.sleep(1)

        self.sc.setPosition(self.UPPER_GRAB_ANGLE)

        time.sleep(self.SERVO_TIME)
        while inp[2] == 0:
            print(inp)
            inp = inputer.getInputs()
            self.mc.setMotor(self.mc_id, -self.MC_SPEED)
        self.mc.stopMotors()

        # self.sc.disengage()
