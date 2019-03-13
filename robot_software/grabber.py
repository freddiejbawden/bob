import time


class Grabber():
    RETRACT_ANGLE = 180
    PREPARE_ANGLE = 42
    GRAB_ANGLE = 180

    MC_SPEED = 100  # speed for the outward and inward scoop
    OUTWARD_SCOOP_TIME = 0.28  # time in seconds for the motor to move towards the shelf
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

    def grab(self):
        print('grabbing')
        self.mc.setMotor(self.mc_id, self.MC_SPEED)
        time.sleep(self.OUTWARD_SCOOP_TIME)
        self.mc.stopMotors()
        time.sleep(1)

        self.sc.setPosition(self.GRAB_ANGLE)

        time.sleep(self.SERVO_TIME)
        self.mc.setMotor(self.mc_id, -self.MC_SPEED)
        time.sleep(self.OUTWARD_SCOOP_TIME+0.07)
        self.mc.stopMotors()

        self.sc.disengage()
