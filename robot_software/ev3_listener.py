#! /usr/bin/env python3

import socket
from robot_software.tcp.followPath import FollowPath
from robot_software.tcp.bobTranslation import extract
import ev3dev.ev3 as ev3

import json
 # Get local machine name


PORT = 65432 # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    HOST  = socket.gethostbyname(socket.gethostname())
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    print("Listening on {}:{}".format(HOST,PORT))
    ev3.Sound.tone([(1000, 250, 0),(1500, 250, 0),(2000, 250, 0)]).wait()
    while True:
        s.listen(2)
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
        
            data = conn.recv(1024)
            if data:
                str_instruction = data.decode('utf-8')
                str_instruction = str_instruction.replace('\'', '\"')
                print(str_instruction)
                robot = FollowPath()
                robot.start(extract(json.loads(str_instruction)))
                print('done')
                conn.sendall(b'done')
                    