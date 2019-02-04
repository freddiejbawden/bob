#! /usr/bin/env python3
import ev3dev.ev3 as ev3
import logging
from time import sleep


class FollowLine:
    # From https://gist.github.com/CS2098/ecb3a078ed502c6a7d6e8d17dc095b48
    MOTOR_SPEED = 700
    KP = 20
    KD = 0.1  # derivative gain   medium
    KI = 0  # integral gain       lowest

    DT = 50  # milliseconds  -  represents change in time since last sensor reading/movement

    # Constructor
    def __init__(self):
        self.btn = ev3.Button()
        self.shut_down = False

    def onLine(self, sensor_value, position):
        if position == 'left':
            return sensor_value < 30
        if position == 'right':
            return sensor_value < 40
        logging.error("onLine: wrong position value for sensor")
        return False

    def correctTrajectory(self, csfl, csfr, lm, rm):
        integral = 0
        previous_error = 0

        while not self.shut_down:
            lval = csfl.value()
            rval = csfr.value()
            error = lval - rval - 10
            logging.info("PID error: ", error)
            integral += (error * self.DT)
            derivative = (error - previous_error) / self.DT

            # u zero:     on target,  drive forward
            # u positive: too bright, turn right
            # u negative: too dark,   turn left
            # u is torque (See IVR lecture on Control)
            u = (self.KP * error) + (self.KI * integral) + (self.KD* derivative)

            # limit u to safe values: [-1000, 1000] deg/sec
            if self.MOTOR_SPEED + abs(u) > 1000:  # reduce u if speed and torque are too high
                if u >= 0:
                    u = 1000 - self.MOTOR_SPEED
                else:
                    u = self.MOTOR_SPEED - 1000

            # run motors
            lm.run_timed(time_sp=self.DT, speed_sp=-(self.MOTOR_SPEED + u))
            rm.run_timed(time_sp=self.DT, speed_sp=-(self.MOTOR_SPEED - u))
            sleep(self.DT / 1000)


            print("u {}".format(u))
            print("lm {}\n".format(lm.speed_sp))
            print("rm {}".format(rm.speed_sp))
            print("PID:", lval, rval)

            previous_error = error

    def run(self):

        # colour sensors
        csfl = ev3.ColorSensor('in1')  # colour sensor front left
        csfr = ev3.ColorSensor('in2')  # colour sensor front right
        assert csfl.connected
        assert csfr.connected
        csfl.mode = 'COL-REFLECT'  # measure light intensity
        csfr.mode = 'COL-REFLECT'  # measure light intensity

        # motors
        lm = ev3.LargeMotor('outA')  # left motor
        rm = ev3.LargeMotor('outC')  # right motor
        assert lm.connected
        assert rm.connected
        self.correctTrajectory(csfl, csfr, lm, rm)

        """
        lm.run_forever(speed_sp=-self.MOTOR_SPEED)
        rm.run_forever(speed_sp=-self.MOTOR_SPEED)
        while not self.shut_down:
            print(csfl.value(), csfr.value())
            if self.onLine(csfl.value(), 'left') or self.onLine(csfr.value(), 'right'):   # left sensor is on the line
                lm.stop()
                rm.stop()
                self.correctTrajectory(csfl, csfr, lm, rm)
        """
        rm.stop()
        lm.stop()


# Main function
if __name__ == "__main__":
    robot = FollowLine()
    robot.run()
