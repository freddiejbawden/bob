#! /usr/bin/env python3
import sys
import socket

from followPath import FollowPath
from bobTranslation import extract
from followLine import FollowLine
import ev3dev.ev3 as ev3
import time
import json
 # Get local machine name
class EV3Listener:
    def __init__(self):
        self.path_follower = FollowPath()
    def get_instructions(self):
        PORT = 65433 # Port to listen on (non-privileged ports are > 1023)

        s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST  = socket.gethostbyname(socket.gethostname())
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        print("Listening on {}:{}".format(HOST,PORT))
        #ev3.Sound.tone([(1000, 250, 0),(1500, 250, 0),(2000, 250, 0)]).wait()
        s.listen(2)
        conn, addr = s.accept()
        print('Connected by', addr)
        try:
            while True:
                data = conn.recv(1024)
                if data:
                    str_instruction = data.decode('utf-8')
                    str_instruction = str_instruction.replace('\'', '\"')
                    str_instruction = str_instruction.replace('u\"', '\"')
                    print(str_instruction)
                    if str_instruction == 'FIN':
                        return
                    elif str_instruction == 'move_in' or str_instruction == 'in':
                        self.path_follower.go(['in'])
                    elif str_instruction == 'move_out'or str_instruction == 'in':
                        self.path_follower.go(['out'])
                    elif str_instruction == 'stop_shelf':
                        self.path_follower.go(['stop'])
                    else:
                        movement = json.loads(str_instruction)
                        self.path_follower.go([extract(movement)])
                    print('done')
                    conn.sendall(b'done')
        except KeyboardInterrupt:
            print("Interrupted! Closing")
            conn.close()
        finally:
            print("Ended. Closing")
            conn.close()
ev3 = EV3Listener()
ev3.get_instructions()