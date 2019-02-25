#! /usr/bin/env python3
import ev3dev.ev3 as ev3
import logging
from time import sleep


class DetectMarking:

    # Constructor
    def __init__(self):
        self.btn = ev3.Button()
        self.shut_down = False

