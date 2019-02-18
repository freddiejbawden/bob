#! /usr/bin/env python3
import ev3dev.ev3 as ev3
from followLineServer import FollowLine


class FollowPath:
    # Follow a path given by the server

    def go(self, path):
        line_follower = FollowLine()
        for direction, distance in path:
            print((direction,distance))
            # direction move in forwards axis or side axis
            if direction == 'F':
                # start currently only deals with forwards and backwards motion
                line_follower.start(distance)
            elif direction == 'S':
                if distance < 0:
                    ev3.Sound.speak("Slide to the left").wait()
                else:
                    ev3.Sound.speak("Slide to the right").wait()
            elif direction == 'G':
                ev3.Sound.speak("yoink").wait()



# Main function
if __name__ == "__main__":
    path_follower = FollowPath()
    # F = forwards
    # S = sideways    could change to X and Y once standard has been agreed
    # G = grab
    path = [('F', 2), ('G', 0), ('F', -2), ('G', 0), ('F', 1), ('S', 1), ('F', -2), ('G', 0), ('F', 1), ('S', 1),
            ('F', 1), ('G', 0), ('F', -1), ('S', -2)]
    path_follower.go(path)
