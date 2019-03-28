import socket
import json

def listen():
    PORT = 65432 # Port to listen on (non-privileged ports are > 1023)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    HOST  = socket.gethostbyname(socket.gethostname())
    s.bind((HOST, PORT))
    print("Listening on {}:{}".format(HOST,PORT))
    while True:
        s.listen(1)
        conn, addr = s.accept()

        print('Connected by', addr)
        
        data = conn.recv(1024)
        data = data.decode('utf-8')
        data = data.split(' ')
        if data[0] == 'grab':
            print('grab')
        elif data[0] == 'prepare':
            print('prepare_grabber')
        elif data[0] == 'wait_for_bump':
            print('wait for bump')
            raw_input()
            print("BUMP!")
        elif data[0] == 'lift':
            print('lift to {}'.format(data[1]))
        
        conn.sendall(b'done')
        conn.close()
