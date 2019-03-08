#!/usr/bin/env python3

import socket
import sys
import requests
import json
from time import sleep
from bobTranslation import extract


class RobotJobListener():
    def __init__(self,server_info, rasp_info, ev3_info):
        self.server_info = {'ip':server_info[0],'port':server_info[1]}
        self.rasp_info = {"ip":rasp_info[0],'port':rasp_info[1]}
        self.ev3_info = {'ip':ev3_info[0],'port':ev3_info[1]}
        self.rasp_target = 'ra'
        self.ev3_target = 'ev'
    def listen_to_server(self,username):
        while True:
            header = {'username':username}
            r = requests.get('http://{}:{}/robotjob'.format(self.server_info['ip'],self.server_info['port']), headers=header)
            path = json.loads(r.text)
            if path['job'] != []:
                print(path['job'])
                self.job_handler(path['job']['instruction_set'])
            sleep(5)
    def job_handler(self,instruction_set):
        # TODO, open this on a new thread
        i = 0
        for instruction in (instruction_set):
            command = instruction['command']
            if command == "lift" or command == "grab" or command == "drop":
                self.open_and_send(self.rasp_target,str(instruction))
            else:
                self.open_and_send(self.ev3_target,str(instruction))
    
    def open_and_send(self, target,payload):
        HOST = None
        PORT = None
        print(self.ev3_info)
        if target == self.rasp_target:
            HOST = self.rasp_info['ip']
            PORT = self.rasp_info['port']
        elif target == self.ev3_target:
            HOST = self.ev3_info['ip']
            PORT = self.ev3_info['port']

        #convert instruction to payload
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(payload)
            s.sendall(str.encode(payload))
            instruction_ack = s.recv(1024)
            #TODO: handle lost etc.
            if instruction_ack == b'done':
                print('done')



if __name__ == "__main__":
    rjl = RobotJobListener(['192.168.105.38',9000],['192.168.105.38',65432],['192.168.105.94',65432])
    rjl.listen_to_server('robot')

    

