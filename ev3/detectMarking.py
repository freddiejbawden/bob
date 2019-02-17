#! /usr/bin/env python3
import ev3dev.ev3 as ev3
import logging
from time import sleep


def get_rgb(sensor):
    assert sensor.mode == 'RGB-RAW'
    red = sensor.value(0)
    green = sensor.value(1)
    blue = sensor.value(2)
    print(red, green, blue)
    return red, green, blue


def on_line(sensor_value, position):
    if position == 'left':
        return sensor_value < 30
    if position == 'right':
        return sensor_value < 40
    logging.error("onLine: wrong position value for sensor")
    return False