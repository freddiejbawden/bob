import socket

 # Get local machine name
PORT = 65432 # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    HOST  = socket.gethostbyname(socket.gethostname())
    s.bind((HOST, PORT))
    print("Listening on {}:{}".format(HOST,PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if data:
                conn.sendall(b'done')