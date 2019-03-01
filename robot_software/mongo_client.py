#!/usr/bin/python3
import traceback
#check that the robot packages are present
print("Starting Client")
print("Using API level v1")
ev3_package_check = True
try:
    import ev3dev.ev3 as ev3
    from followLineServer import FollowLine
    print("ev3 modules imported")
except:
    traceback.print_exc()
    print("Unable to load robot control packages package!")
    ev3_package_check = False
import requests
print("request imported")
import socket
print("socket imported")
import struct
print("struct imported")
import time
print("time imported")
import sys
print("sys imported")
import datetime
print("datetime imported")
import json
print("json imported")
from threading import Thread
print("threading imported")
from zeroconf import ServiceBrowser, Zeroconf
print("zeroconf imported")
#remove me

last_json = {}

def polling(ip_addr, port, run_robot,username):
    running = True
    movement = False
    if run_robot:
        bob_bot = FollowLine()
    while running:
        try:
            headers = {'username':username}
            r = requests.get("http://{}:{}/robotjob".format(ip_addr,port),headers=headers)
            path = json.loads(r.text)
            if (path["job"] == []):
                print("No order")
            else:
                print(path['job'])
                #TODO: pass to robot
            
        except:
            url = "http://{}:{}/getmovement".format(ip_addr,port)
            print("GET request: {} failed at {}".format(url,datetime.datetime.now()))
            traceback.print_exc()

        time.sleep(5)

class MyListener:
    def __init__(self,run_robot):
        self.run_robot = run_robot
    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        ip_addr =(socket.inet_ntoa(info.address))
        port = info.port
        print(ip_addr,port,name)
        if (name == "assis10t._http._tcp.local."):
            #TODO: call get 3 times
            try:
                base_url = "http://{}:{}".format(ip_addr,port)
                
                r = requests.get("http://{}:{}/ping".format(ip_addr, port))
                # wait for response
                if (r.text == "pong"):
                    print("Server running on {}:{}".format(ip_addr,port))
                    username = "bob_test"
                    body = {'username':username,'type':'robot'}
                    r = requests.post('http://{}:{}/register'.format(ip_addr,port),json=body)
                    if (json.loads(r.text)["success"]):
                        print('Registered bob_test')
                    else:
                        print(r.text)
                    
                    r = requests.get('http://{}:{}/robot'.format(ip_addr,port),headers={'username':'bob_test'})
                    print(r.text)
                    if (self.run_robot):
                        ev3.Sound.tone([(1000, 250, 0),(1500, 250, 0),(2000, 250, 0)]).wait()
                        ev3.Sound.speak("i am bob. Beep. i collect your shopping").wait()
                        # TODO: add light to indicate status
                    poller = Thread(target=polling, name="poller",args=(ip_addr,port,self.run_robot,username))
                    poller.start()
                else:
                    print("Server did not respond!")
                    if (self.run_robot):
                        ev3.Sound.tone([(750, 250, 0),(750, 250, 0)]).wait()
                        # TODO: add light to indicate status
            except:
                print("Failed to connect to server!")
                traceback.print_exc()
                if (self.run_robot):
                    ev3.Sound.tone([(750, 250, 0),(750, 250, 0)]).wait()
                    # TODO: add light to indicate status





if __name__ == "__main__":
    run_robot = None
    if (len(sys.argv) > 1):
        mode_str = sys.argv[1]
        #TODO: clean this up
        if (mode_str == 'r' or mode_str == 'robot' and ev3_package_present == True):
            ev3.Sound().beep().wait()
            run_robot = True
        elif (mode_str == "t" or mode_str=="test"):
            print("Running client in test mode...")
            print(''.join(['-' for x in range(40)]) + '\n')
            run_robot = False
        else:
            print('Unable to determine mode! r/robot -> robot | t/test -> test')
            exit()
    else:
        if (ev3_package_check):
            #assume robot mode
            run_robot = True
        else:
            print("Unable to start client as ev3 package not present and test mode not indicated")
            exit()
    if (run_robot):
        ev3.Sound.beep().wait()
    zeroconf = Zeroconf()
    listener = MyListener(run_robot)
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
    try:

        input("Press enter to exit...\n\n")
    finally:
        zeroconf.close()
