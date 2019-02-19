#! /usr/bin/env python3
import ev3dev.ev3 as ev3
from followLineServer import FollowLine


class FollowPath:
    # Follow a path given by the server

    # Constructor
    #def __init__(self):


    def go(self, path):
        line_follower = FollowLine()
        for direction, distance in path:
            # direction move in forwards axis or side axis
            if direction == 'Y':
                # start currently only deals with forwards and backwards motion
                line_follower.run_y(distance)
            elif direction == 'X':
                if distance < 0:
                    ev3.Sound.speak("Slide to the left").wait()
                else:
                    ev3.Sound.speak("Slide to the right").wait()
            elif direction == 'G':
                ev3.Sound.speak("Criss cross").wait()
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
    # Y = forwards
    # X = sideways
    # G = grab
    path = [('Y', 2), ('G', 0), ('Y', -2), ('G', 0), ('Y', 1), ('X', 1), ('Y', -2), ('G', 0), ('Y', 1), ('X', 1),
            ('Y', 1), ('G', 0), ('Y', -1), ('X', -2)]
    path_follower.go(path)
