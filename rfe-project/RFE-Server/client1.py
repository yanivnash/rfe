
"""
this program is the  clien
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

import json

while True:
    msg = input("[SEND MESSAGE] Type your message [exit]...:")
    if msg == DISCONNECT_MESSAGE:
        client.send(msg.encode(FORMAT))
        print("[CONNECTION CLOSED")
        client.close()
        break
    # client.send(msg.encode(FORMAT))
    email = "yanivnash@gmail.com"
    password = "123456789"
    ip_list = "yaniv-pc/yaniv-192.168.1.20,192.168.1.1"
    send_object = json.dumps(("NEW_USER", f"""INSERT INTO users(email,password,IP_list) VALUES("{email}", "{password}", "{ip_list}")""")).encode(FORMAT)
    client.send(send_object)
    msg = client.recv(MSG_LENGHT).decode(FORMAT)
    print(msg)