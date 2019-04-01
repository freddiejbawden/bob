#!/usr/bin/env python3

import socket
import sys
import requests
import json
import time
from threading import Thread
from time import sleep
from bobTranslation import extract
from rasppi_listener import listen
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
        self.ev3_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ev3_socket.connect((ev3_info[0], ev3_info[1]))
        print("Ev3 socket connected")
        self.rasp_pi_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.rasp_pi_socket.connect((rasp_info[0], rasp_info[1]))
        print("Rasp Pi socket connected")
        
    def start_reliable_listener(self,username):
        try:
            while True:
                res = self.listen_to_server(username)
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
        finally:
            self.ev3_socket.sendall(str.encode("FIN"))
            self.ev3_socket.close()
            self.rasp_pi_socket.close()
    def listen_to_server(self,username):
        try:
            while True:
                print('elsendo')
                header = {'username':'robot'}
                r = requests.get('http://{}:{}/api/robotjob'.format(self.server_info['ip'],self.server_info['port']), headers=header)
                path = json.loads(r.text)
                print(path)
                if path['success'] != False:
                    
                    if path['job'] != []:
                        self.job_handler(path['job']['instruction_set'])
                        headers={'username':'merchant_01'}
                        url = 'http://{}:{}/api/warehouse/5c755f58bfcf4c592bfd00a6/orders/{}'.format(self.server_info['ip'],self.server_info['port'],path['job']['id'])
                        update = requests.post(url,headers=headers,json={'status':'READY_TO_COLLECT'})
                        while not(json.loads(update.text)['success']):
                            time.sleep(5)
                            update = requests.post(url,headers=headers,json={'status':'READY_TO_COLLECT'})
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
            print(instruction)
            command = instruction['command']
            res = None
          
            if command == "grab":
                res = self.reliable_grab(instruction["parameters"]['height'])
            elif command == "drop":
                res = self.reliable_send_data(self.rasp_target, str("drop"))
            else:
                res = self.reliable_send_data(self.ev3_target,str(instruction))
    def reliable_grab(self,height):
        try:
            global thread_manager
            self.reliable_send_data(self.rasp_target,"lift {}".format(height))
            self.reliable_send_data(self.rasp_target,"prepare")
            thread_manager['bumped'] = False
            move_in_thread = Thread(target = self.move_until_bump)
            move_in_thread.daemon = True
            move_in_thread.start()
            
            self.reliable_send_data(self.rasp_target,"wait_for_bump")
            print('bump!')
            self.reliable_send_data(self.ev3_target,"stop_shelf")
            thread_manager['bumped'] = True
            if int(height) >= 1:
                self.reliable_send_data(self.rasp_target, "upper_grab")
            else:
                self.reliable_send_data(self.rasp_target,"grab")
            self.reliable_send_data(self.ev3_target,"move_out")
            self.reliable_send_data(self.rasp_target, "retract")
            self.reliable_send_data(self.rasp_target,"lift 0")

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
                    time.sleep(1)
                    return 0
        except KeyboardInterrupt:
            return -1

    def open_and_send(self, target,payload):
        try:
            if target == self.rasp_target:
                self.rasp_pi_socket.sendall(str.encode(payload))
                instruction_ack =  self.rasp_pi_socket.recv(1024)
                while instruction_ack != b'done':
                        instruction_ack =  self.rasp_pi_socket.recv(1024)
                print('done')
            
            elif target == self.ev3_target:
                self.ev3_socket.sendall(str.encode(payload))        
                print("sent to ev3")
                instruction_ack =  self.ev3_socket.recv(1024)
                while instruction_ack != b'done':
                        instruction_ack =  self.ev3_socket.recv(1024)
                print('done')
            return 0
        except socket.error:
            print('Error sending to {}'.format(target))
            return -1

