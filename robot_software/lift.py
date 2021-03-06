#! /usr/bin/env python3
import time
from iotools import IOTools
import sys

class Lift:
    MC_SPEED = 100
    # use ports 2 and 3
    mc_id_a = 2
    mc_id_b = 3

    def __init__(self,onRobot, mc):
        self.mc = mc
        self.mc.stopMotors()

    def lift(self, direction):
        print('lifting {}'.format(direction))
        try:
            if direction == 'up':
                self.mc.setMotor(self.mc_id_a, -self.MC_SPEED)
                self.mc.setMotor(self.mc_id_b, -self.MC_SPEED)
                raw_input()
                #time.sleep(10)
                self.mc.stopMotor(self.mc_id_a)
                self.mc.stopMotor(self.mc_id_b)
                time.sleep(1)
            elif direction == 'down':
                self.mc.setMotor(self.mc_id_a, self.MC_SPEED)
                self.mc.setMotor(self.mc_id_b, self.MC_SPEED)
                raw_input()
                #time.sleep(8)
                self.mc.stopMotor(self.mc_id_a)
                self.mc.stopMotor(self.mc_id_b)
                time.sleep(1)
        except KeyboardInterrupt:
                self.mc.stopMotor(self.mc_id_a)
                self.mc.stopMotor(self.mc_id_b)


if __name__ == "__main__":
    onRobot = bool(sys.argv.count('-rss'))
    lifter = Lift(onRobot)
    lifter.lift('up')
    time.sleep(lifter.LIFT_TIME+1)
    lifter.lift('down')


