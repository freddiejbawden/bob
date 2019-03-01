#! /usr/bin/env python3
import ev3dev.ev3 as ev3
import logging

KP = 10
KD = 0.5  # derivative gain   medium
KI = 0  # integral gain       lowest


def calculate_torque(lval, rval, DT, integral, previous_error):
    error = lval - rval - 10
    logging.info("PID error: ", error)
    integral += (error * DT)
    derivative = (error - previous_error) / DT

    # u zero:     on target,  drive forward
    # u positive: too bright, turn right
    # u negative: too dark,   turn left
    # u is torque (See IVR lecture on Control)
    u = (KP * error) + (KI * integral) + (KD * derivative)
    print("u:", u)
    logging.info("PID torque: ", u)
    return u, integral, error