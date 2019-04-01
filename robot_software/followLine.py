#! /usr/bin/env python3
import ev3dev.ev3 as ev3
from time import sleep, time
import control


class FollowLine:
    # From https://gist.github.com/CS2098/ecb3a078ed502c6a7d6e8d17dc095b48
    MOTOR_SPEED = 1000
    DT = 50  # milliseconds  -  represents change in time since last sensor reading/


    MARKING_NUMBER = 2  # number of consecutive colour readings to detect marking
    MARKING_INTERVAL = 1.3  # time between marking checks in seconds
    reverse = False

    BLACK = 1  # black reading from colour sensor in COL-COLOR mode
    BLUE = 2  # blue reading from colour sensor in COL-COLOR mode
    GREEN = 3  # green reading from colour sensor in COL-COLOR mode

    CORRECTION_TIME = 100  # time in millisecond Bob moves away from blue line to correct sideways movement
    SIDEWAYS_SPEED = 1000   # how fast Bob moves when moving sideways

    # Constructor
    def __init__(self):
        self.btn = ev3.Button()
        self.shut_down = False

        # colour sensors
        self.csfl = ev3.ColorSensor('in1')  # colour sensor front left
        self.csfr = ev3.ColorSensor('in2')  # colour sensor front right
        self.csbl = ev3.ColorSensor('in3')  # colour sensor back left
        self.csbr = ev3.ColorSensor('in4')  # colour sensor back right
        assert self.csfl.connected
        assert self.csfr.connected
        assert self.csbl.connected
        assert self.csbr.connected

        # motors
        self.lm = ev3.LargeMotor('outA')  # left motor
        self.rm = ev3.LargeMotor('outC')  # right motor
        self.cm = ev3.LargeMotor('outD')  # centre motor
        assert self.lm.connected
        assert self.rm.connected
        assert self.cm.connected

        self.consecutive_colours = 0  # counter for consecutive colour readings
        self.ignore_blue = False  # when switching from sideways to forwards
        self.ignore_green = False  # when switching from forwards to sideways
        # self.number_of_markers = 0  # at which marker it should stop

        self.start_time = 0  # when robot starts doing a command
        self.marker_counter = 0  # how many markers have been passed in current command

        self.reverse = -1  # -1 if Bob is reversing, 1 if not
        self.moving_out_over_black_count = 0
    def detect_marking(self, colour_left, colour_right, desired_colour):
        # print(colour_left, colour_right)
        if colour_right == desired_colour and colour_left == desired_colour:
            self.consecutive_colours += 1
            print("CONSECUTIVE COLOURS: ", self.consecutive_colours)
            if self.consecutive_colours >= self.MARKING_NUMBER:
                self.consecutive_colours = 0
                return True
        else:
            self.consecutive_colours = 0
        return False

    # limit motor speed to safe values: [-1000, 1000] deg/sec
    @staticmethod
    def limit_speed(speed):
        if speed > 1000:
            return 1000
        if speed < -1000:
            return -1000
        return speed

    # adjust modes of colour sensors depending on the direction of Bob
    # COL-REFLECT: measure light intensity
    # COL-COLOR: measure colour
    def set_cs_modes(self, direction):
        if direction == 'forward':
            self.csfl.mode = 'COL-REFLECT'
            self.csfr.mode = 'COL-REFLECT'
            self.csbl.mode = 'COL-COLOR'
            self.csbr.mode = 'COL-COLOR'
        elif direction == 'backward':
            self.csfl.mode = 'COL-COLOR'
            self.csfr.mode = 'COL-COLOR'
            self.csbl.mode = 'COL-REFLECT'
            self.csbr.mode = 'COL-REFLECT'
        elif direction == 'left' or direction == 'right':
            self.csfl.mode = 'COL-COLOR'
            self.csfr.mode = 'COL-COLOR'
            self.csbl.mode = 'COL-COLOR'
            self.csbr.mode = 'COL-COLOR'
        else:
            return False  # wrong direction command sent
        return True

    # increase marker counter when seeing desired colour
    def count_markings(self, cs_left, cs_right, desired_colour):
        # Wait before checking for colour again
        if time() - self.start_time > self.MARKING_INTERVAL:
            # marking of desired colour detected
            if self.detect_marking(cs_left.value(), cs_right.value(), desired_colour):
                self.marker_counter += 1
                ev3.Sound.beep()
                self.start_time = time()
        return

    # follows a line and corrects trajectory continually
    # uses light sensors to follow line and colour sensors to detect markings
    def correct_trajectory(self, light_left, light_right, motor_left, motor_right, pid_controller):
        # most likely off line, may need to recalibrate numbers later
        # time_off_line = self.get_back_on_line(light_left, light_right, time_off_line)

        # Calculate torque using PID control
        torque = pid_controller.calculate_torque(light_left.value(), light_right.value())
        # Set the speed of the motors
        speed_left = self.limit_speed(self.MOTOR_SPEED + torque)
        speed_right = self.limit_speed(self.MOTOR_SPEED - torque)
        print('Speed left:', speed_left)
        print('Speed right:', speed_right)

        # run motors
        motor_left.run_timed(time_sp=self.DT, speed_sp=speed_left * self.reverse)
        motor_right.run_timed(time_sp=self.DT, speed_sp=speed_right * self.reverse)
        sleep(self.DT / 1000)

        return

    # move forward
    def run_forward(self, distance, desired_colour):
        self.reverse = 1
        self.start_time = time()
        self.marker_counter = 0
        pid_controller = control.Control(self.DT)

        while not self.shut_down:
            self.correct_trajectory(self.csfl, self.csfr, self.lm, self.rm, pid_controller)
            self.count_markings(self.csbl, self.csbr, desired_colour)
            if self.marker_counter >= distance:
                return

    # move backward
    def run_backward(self, distance, desired_colour):
        self.reverse = -1
        self.start_time = time()
        self.marker_counter = 0
        pid_controller = control.Control(self.DT)

        while not self.shut_down:
            self.correct_trajectory(self.csbr, self.csbl, self.rm, self.lm, pid_controller)
            self.count_markings(self.csfr, self.csfl, desired_colour)
            if self.marker_counter >= distance:
                return

    # move sideways between two blue lines
    def run_sideways(self, distance, direction, last_direction):
        self.start_time = time()
        self.marker_counter = 0

        while not self.shut_down:
            # if a colour sensor is on a blue line, correct position to be between them again
            if direction == 'left':
                right_speed = self.SIDEWAYS_SPEED/2.0
                left_speed = self.SIDEWAYS_SPEED
            else:
                right_speed = self.SIDEWAYS_SPEED
                left_speed = self.SIDEWAYS_SPEED / 2.0
            if self.detect_marking(self.csbl.value(), self.csbr.value(), self.BLUE):
                # back sensors on blue line, so move forward for some time
                self.lm.run_timed(time_sp=self.CORRECTION_TIME, speed_sp=left_speed)
                self.rm.run_timed(time_sp=self.CORRECTION_TIME, speed_sp=right_speed)
                sleep(self.CORRECTION_TIME / 1000)
            if self.detect_marking(self.csfl.value(), self.csfr.value(), self.BLUE):
                # front sensors on blue line, so move backward for some time

                self.lm.run_timed(time_sp=self.CORRECTION_TIME, speed_sp=-left_speed)
                self.rm.run_timed(time_sp=self.CORRECTION_TIME, speed_sp=-right_speed)
                sleep(self.CORRECTION_TIME / 1000)

            # colour sensor for marking detection needs to be at front or back dependng on the last direction
            if last_direction == 'forward':
                cs_left = self.csbr
                cs_right = self.csbl
            else:
                # if last direction is backward, left, or right
                cs_left = self.csfr
                cs_right = self.csfl

            # move sideways for a bit while counting black markings
            if direction == 'left':
                self.cm.run_timed(time_sp=self.DT, speed_sp=self.SIDEWAYS_SPEED)
                sleep(self.DT / 1000)
                self.count_markings(cs_left, cs_left, self.BLACK)
            if direction == 'right':
                self.cm.run_timed(time_sp=self.DT, speed_sp=-self.SIDEWAYS_SPEED)
                sleep(self.DT / 1000)
                self.count_markings(cs_right, cs_right, self.BLACK)

            if self.marker_counter >= distance:
                return

    # when line is lost oscillate side to side until it is found
    def get_back_on_line(self, lval, rval, time_off_line):
        if lval > 90 and rval > 70:
            if time_off_line == 0:
                time_off_line = time()
            # if off line for more than a second move side-to-side until line is found
            # print(time() - time_off_line)
            if time() - time_off_line > 0.5:
                correction_speed = 200
                correction_time = 100
                # can change thresholds
                while lval > 70 and rval > 50:
                    self.cm.run_timed(time_sp=correction_time, speed_sp=correction_speed)
                    correction_speed *= -1
                    # increase the time to move in one direction to increased the search radius
                    correction_time += 100
                    sleep(correction_time / 1000)  # milliseconds to seconds
                    lval = self.csfl.value()
                    rval = self.csfr.value()
                time_off_line = 0
        else:
            time_off_line = 0
        return time_off_line

    def move_toward_shelf(self):
        self.cm.run_timed(time_sp=self.DT*50, speed_sp=-self.SIDEWAYS_SPEED)
        sleep(self.DT*50.0/1000.0)
        return

    def move_away_from_shelf(self):
        # move out until black is seen
        print('moving back')
        
        self.cm.run_timed(time_sp=300, speed_sp=self.SIDEWAYS_SPEED)
        sleep(0.3)
        if self.detect_marking(self.csbr, self.csbr, self.BLACK):
            print("BLACK!")
            return

    def stop_shelf_movement(self):
        self.cm.stop(stop_action='brake')

    def stop(self):
        self.shut_down = True
        self.rm.stop()
        self.lm.stop()
        #ev3.Sound.speak("whack").wait()
