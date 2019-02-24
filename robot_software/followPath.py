#! /usr/bin/env python3
import ev3dev.ev3 as ev3
from followLine import FollowLine
from threading import Thread


class FollowPath:
    # Follow a path given by the server

    # Constructor
    def __init__(self):
        self.shut_down = False
        self.runner = None

    def go(self, path):
        line_follower = FollowLine()
        for direction, distance in path:
            print(direction, distance)
            # direction move in forwards axis or side axis
            if direction == 'X':
                # start currently only deals with forwards and backwards motion
                line_follower.run_x(distance)
            elif direction == 'Y':
                line_follower.run_y(distance)
            elif direction == 'G':
                ev3.Sound.speak("Grab").wait()
        line_follower.stop()

    # TODO: possibly move start and stop to FollowPath or move correct trajectory to a separate file instead
    def start(self, path):
        self.shut_down = False
        if len(path) == 0:
            ev3.Sound.speak("No instructions given").wait()
        else:
            self.runner = Thread(target=self.go, args=(path,), name='go')
            self.runner.start()


# Main function
if __name__ == "__main__":
    path_follower = FollowPath()
    # X = forwards
    # Y = sideways
    # G = grab
    current_path = [('X', 2), ('X', -2), ('X', 2), ('X', -2), ('X', 2)]
    #current_path = [('Y', 1), ('X', 2), ('G', 0), ('X', -1), ('G', 0), ('X', 3), ('Y', 1), ('G', 0), ('X', -4),
    #                ('Y', -1)]
    path_follower.start(current_path)
