#! /usr/bin/env python3

import socket
from followPath import FollowPath
from bobTranslation import extract
from followLine import FollowLine
import ev3dev.ev3 as ev3
import json
 # Get local machine name


PORT = 65433 # Port to listen on (non-privileged ports are > 1023)

s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST  = socket.gethostbyname(socket.gethostname())
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
print("Listening on {}:{}".format(HOST,PORT))
#ev3.Sound.tone([(1000, 250, 0),(1500, 250, 0),(2000, 250, 0)]).wait()
while True:
    s.listen(2)
    conn, addr = s.accept()
    print('Connected by', addr)

    data = conn.recv(1024)
    if data:

        str_instruction = data.decode('utf-8')
        str_instruction = str_instruction.replace('\'', '\"')
        str_instruction = str_instruction.replace('u\"', '\"')
        print(str_instruction)
        #TODO: fix follow path so that it can move in or make a new function to handle it.
        #MoveIn()

        if str_instruction == 'move_in':

            line_follower = FollowLine()
            line_follower.move_toward_shelf()
        elif str_instruction == 'move_out':
            print('inb')
            line_follower = FollowLine()
            line_follower.move_away_from_shelf()
        elif str_instruction == 'stop_shelf':
            line_follower = FollowLine()
            line_follower.stop()
            #stop moving in
    

        #else:
        #    robot = FollowPath()
        #    robot.start([extract(json.loads(str_instruction))])



        print('done')
        conn.sendall(b'done')
        conn.close()
