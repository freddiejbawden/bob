#! /usr/bin/env python3
import ev3dev.ev3 as ev3

def get_rgb(sensor):
    assert sensor.mode == 'RGB-RAW'
    red = sensor.value(0)
    green = sensor.value(1)
    blue = sensor.value(2)
    print(red, green, blue)
    return red, green, blue

