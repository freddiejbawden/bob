import socket

serverMACAddress = 'B0:B4:48:76:F2:92'
port = 65432

s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress, port))
while 1:
    text = input()
    if text == "quit":
        break
    s.send(bytes(text, 'utf-8'))
