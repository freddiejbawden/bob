#! /usr/bin/env python3
import ev3dev.ev3 as ev3
from followLine import FollowLine
from threading import Thread


class FollowPath:
    # Follow a path given by the server
    BLACK = 1  # black reading from colour sensor in COL-COLOR mode
    BLUE = 2  # blue reading from colour sensor in COL-COLOR mode
    GREEN = 3  # green reading from colour sensor in COL-COLOR mode

    # Constructor
    def __init__(self):
        self.shut_down = False
        self.runner = None
        self.last_direction = '' # saves previous direction Bob moved in

    def go(self, path):
        print(path)
        line_follower = FollowLine()
        for p in path:
            if isinstance(p,tuple):
                direction, distance = p
                if line_follower.set_cs_modes(direction):

                    # modes set successfully
                    # direction move in forwards axis or side axis
                    if direction == 'forward':
                        line_follower.run_forward(distance, self.GREEN)
                    elif direction == 'backward':
                        line_follower.run_backward(distance, self.GREEN)
                    elif direction == 'left' or direction == 'right':
                        if self.last_direction == 'forward':  # Bob has to move forward to blue line
                            print('SIDEWAYS: moved forward')
                            line_follower.set_cs_modes('forward')
                            line_follower.run_forward(1, self.BLUE)
                        if self.last_direction == 'backward':  # Bob has to move backward to blue line
                            line_follower.set_cs_modes('backward')
                            print('SIDEWAYS: moved backward')
                            line_follower.run_backward(1, self.BLUE)
                        else:
                            print(self.last_direction == 'backward')
                        print('LAST DIRECTION:', self.last_direction)
                        line_follower.set_cs_modes(direction)
                        line_follower.run_sideways(distance, direction, self.last_direction)
                        self.last_direction = direction
                    else:
                        print("invalid direction")
                self.last_direction = direction
            else:
                print(p)
                # not a valid direction for colour sensors
                if p == 'in':
                    #ev3.Sound.speak("Scoopdidoop").wait()
                    line_follower.move_toward_shelf()
                elif p == 'out':
                    line_follower.set_cs_modes('left')
                    line_follower.move_away_from_shelf()
                elif p == 'move_out_upper':
                    line_follower.move_away_from_shelf_upper()
                elif p == 'stop':
                    line_follower.stop_shelf_movement()
                elif p == 'prep_for_upper':
                    line_follower.prep_for_upper()
                elif p == 'move_back_a_little':
                    line_follower.move_backward_for_a_little_bit()
                elif p == 'move_forward_a_little':
                    line_follower.move_forward_for_a_little_bit()
                elif p == 'reset':
                    line_follower.reset_from_move()
                else:
                    print("Wrong command given. What does", p, "mean?")
        line_follower.stop()


    # TODO: possibly move start and stop to FollowPath or move correct trajectory to a separate file instead
    def start(self, path):
        self.shut_down = False
        print(path)
        if len(path) == 0:
            print('no instructions!')
            #ev3.Sound.speak("No instructions given").wait()
        else:
            self.go(path)
if  __name__ == "__main__":
    pf = FollowPath()
    pf.go([('backward',1),('right',1)])
