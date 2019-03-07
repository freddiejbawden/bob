#!/usr/bin/env python3

import socket
import sys
from zeroconf import ServiceBrowser, Zeroconf

class MyListener:

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added, service info: %s" % (name, info))



def open_socket(ip_addr):
    HOST = ip_addr  # The server's hostname or IP address
    PORT = 65432        # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        send('hello',s)

def send(data,s):
    s.sendall(str.encode(data))
    x = s.recv(1024)
    print(x)

if __name__ == "__main__":
  ip_addr = sys.argv[1]
  open_socket(ip_addr)


    

