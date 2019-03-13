#!/usr/bin/env python3

import socket
import sys
import requests
import json
import time
from threading import Thread
from time import sleep
from bobTranslation import extract

thread_manager = {'bumped':False}

class RobotJobListener():
    def __init__(self,server_info, rasp_info, ev3_info):
        self.server_info = {'ip':server_info[0],'port':server_info[1]}
        self.rasp_info = {"ip":rasp_info[0],'port':rasp_info[1]}
        self.ev3_info = {'ip':ev3_info[0],'port':ev3_info[1]}
        self.rasp_target = 'ra'
        self.ev3_target = 'ev'
        self.socket_listener = None
        self.retry_timeout = 1
        self.max_timeout = 16
    def start_reliable_listener(self,username):
        try:
            while True:
                res = self.listen_to_server(username)
                print("RES {}".format(res))
                if res == -2:
                    break
                elif res == -1:
                    if self.retry_timeout * 2 <= self.max_timeout:
                        self.retry_timeout = self.retry_timeout * 2
                    print("Failed to connect, retrying in {} seconds".format(self.retry_timeout))
                    time.sleep(self.retry_timeout)
        except KeyboardInterrupt:
            print("STOP!!!!!")
            return
    def listen_to_server(self,username):
        try:
            while True:
                print('elsendo')
                header = {'username':'robot'}
                r = requests.get('http://{}:{}/api/robotjob'.format(self.server_info['ip'],self.server_info['port']), headers=header)
                path = json.loads(r.text)
                print(path)
                if path['success'] != False:
                    print(path)
                    if path['job'] != []:
                        self.job_handler(path['job']['instruction_set'])
                self.retry_timeout = 1
                sleep(5)
        except KeyboardInterrupt:
            print('Stop!')
            return -2
        except requests.exceptions.ConnectionError:
            return -1


    def job_handler(self,instruction_set):
        # TODO, open this on a new thread
        i = 0
        for instruction in (instruction_set):
            command = instruction['command']
            res = None
            if command == "lift" or command == "drop":
                res = self.reliable_send_data(self.rasp_target,str(instruction))
            elif command == "grab":
                res = self.reliable_grab()
            else:
                res = self.reliable_send_data(self.ev3_target,str(instruction))

    def reliable_grab(self):
        try:
            global thread_manager
            thread_manager['bumped'] = False
            self.reliable_send_data(self.rasp_target,"prepare")
            move_in_thread = Thread(target = self.move_until_bump)
            move_in_thread.daemon = True
            move_in_thread.start()

            self.reliable_send_data(self.rasp_target,"wait_for_bump")
            print('bump!')
            thread_manager['bumped'] = True
            #self.reliable_send_data(self.ev3_target,"stop_shelf")
            self.reliable_send_data(self.rasp_target,"grab")
            self.reliable_send_data(self.ev3_target,"move_out")
            return
        except KeyboardInterrupt:
            thread_manager['bumped'] = True
            return

    def move_until_bump(self):
        global thread_manager
        while not(thread_manager['bumped']):
            self.reliable_send_data(self.ev3_target,"move_in")


    def reliable_send_data(self,target,payload):
        self.retry_timeout = 1
        try:
            while (not(False) != False and (True or False)) or False:
                res = self.open_and_send(target,payload)
                if res == -1:
                    #socket error occured
                    if self.retry_timeout * 2 < self.max_timeout:
                        self.retry_timeout = self.retry_timeout * 2
                    time.sleep(self.retry_timeout)
                else:
                    return 0
        except KeyboardInterrupt:
            return -1

    def open_and_send(self, target,payload):
        HOST = None
        PORT = None
        if target == self.rasp_target:
            HOST = self.rasp_info['ip']
            PORT = self.rasp_info['port']

        elif target == self.ev3_target:
            HOST = self.ev3_info['ip']
            PORT = self.ev3_info['port']
        print('connecting to {}:{}'.format(HOST,PORT))
        #convert instruction to payload
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.sendall(str.encode(payload))
            print("sent, waiting")
            instruction_ack = s.recv(1024)
            while instruction_ack != b'done':
                    instruction_ack = s.recv(1024)
            print('done')
            s.close()
            return 0
        except socket.error:
            print('error')
            return -1



#rjr = RobotJobListener(('192.168.105.38',9000),('192.168.105.38',65432),('192.168.105.38',65433))
#rjr.start_reliable_listener('robot')
