#! /usr/bin/env python3
import ev3dev.ev3 as ev3
import logging


class Control:
    KP = 10
    KD = 0.5  # derivative gain   medium
    KI = 0  # integral gain       lowest

    # Constructor
    def __init__(self, dt):
        self.dt = dt
        self.integral = 0
        self.previous_error = 0

    def calculate_torque(self, lval, rval):
        error = lval - rval
        #print('lval', lval)
        #print('rval', rval)
        #print("PID error: ", error)
        self.integral += (error * self.dt)
        derivative = (error - self.previous_error) / self.dt
        self.previous_error = error

        # u zero:     on target,  drive forward
        # u positive: too bright, turn right
        # u negative: too dark,   turn left
        # u is torque (See IVR lecture on Control)
        u = (self.KP * error) + (self.KI * self.integral) + (self.KD * derivative)
        #print("PID torque: ", u)
        return u
