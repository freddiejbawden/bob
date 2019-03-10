#!/usr/bin/env python3

import socket
import sys
import requests
import json
from rasppi_listener import Listener
from threading import Thread
from time import sleep
from bobTranslation import extract


class RobotJobListener():
    def __init__(self,server_info, rasp_info, ev3_info):
        self.server_info = {'ip':server_info[0],'port':server_info[1]}
        self.rasp_info = {"ip":rasp_info[0],'port':rasp_info[1]}
        self.ev3_info = {'ip':ev3_info[0],'port':ev3_info[1]}
        self.rasp_target = 'ra'
        self.ev3_target = 'ev'
        self.socket_listener = None
    def listen_to_server(self,username):
        try:
            
            print('elsendo')
            header = {'username':'robot'}
            r = requests.get('http://{}:{}/robotjob'.format(self.server_info['ip'],self.server_info['port']), headers=header)
            path = json.loads(r.text)
            print(path)
            if path['success'] != False:
                print(path)
                if path['job'] != []:
                    self.job_handler(path['job']['instruction_set'])
            sleep(5)
        except KeyboardInterrupt:
            print('Stop!')
            return
            
    def job_handler(self,instruction_set):
        # TODO, open this on a new thread
        i = 0
        for instruction in (instruction_set):
            command = instruction['command']
            if command == "lift" or command == "grab" or command == "drop":
                self.open_and_send(self.rasp_target,str(instruction))
            else:
                self.open_and_send(self.ev3_target,str(instruction))
            print("sent")
    def open_and_send(self, target,payload):
        HOST = None
        PORT = None
        if target == self.rasp_target:
            HOST = self.rasp_info['ip']
            PORT = self.rasp_info['port']
        elif target == self.ev3_target:
            HOST = self.ev3_info['ip']
            PORT = self.ev3_info['port']

        #convert instruction to payload
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(str.encode(payload))
            instruction_ack = s.recv(1024)
            while instruction_ack != b'done':
                  instruction_ack = s.recv(1024)
            print('done')
        





    

