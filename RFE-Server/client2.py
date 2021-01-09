
"""
this program is the  client
"""

import socket

#declare CONSTANT
MSG_LENGHT  = 1024
PORT = 5050
FORMAT = 'utf-8'
SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = 'exit'


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

while True:
    msg = input("[SEND MESSAGE] Type your message [exit]...:")
    if msg == DISCONNECT_MESSAGE:
        client.send(msg.encode(FORMAT))
        print("[CONNECTION CLOSED")
        client.close()
        break
    client.send(msg.encode(FORMAT))
    msg = client.recv(MSG_LENGHT).decode(FORMAT)
    print(msg)