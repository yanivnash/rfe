import socket
import json
import os

# SERVER_IP = '192.168.56.1'
SERVER_IP = '84.111.109.58'
PORT = 5050
FORMAT = 'utf-8'
MSG_LEN = 2048

def send_to_server(send_object):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, PORT))
        client.send(send_object)
        answr = client.recv(MSG_LEN).decode(FORMAT)
        client.close()
        return json.loads(answr)  # None = action not found
    except ConnectionRefusedError:
        return 'SERVER IS DOWN'

def create_new_user(email, password, ip_dict):
    send_object = json.dumps({'action': 'NEW_USER', 'email': email, 'password': password, 'ip_dict': ip_dict}).encode(FORMAT)
    return send_to_server(send_object)  # True =  user created | False = user not created

def check_if_email_exists(email):
    send_object = json.dumps({'action': 'CHECK_EMAIL', 'email': email}).encode(FORMAT)
    return send_to_server(send_object)  # True =  email exists | False = email doesn't exist

def update_pc_in_account(email):
    pc_ip = socket.gethostbyname(socket.gethostname())
    pc_name = os.getlogin()
    name_ip_tup = (pc_ip, pc_name)
    send_object = json.dumps({'action': 'UPDATE_PC', 'email': email, 'name_ip_tup': name_ip_tup}).encode(FORMAT)
    send_to_server(send_object)  # maybe delete this note and not return anything
    # True =  pc was in account / pc wasn't in account and now is | False = pc wasn't in account but adding hit an error

def login(email, password, is_update):
    send_object = json.dumps({'action': 'LOGIN', 'email': email, 'password': password}).encode(FORMAT)
    answr = send_to_server(send_object)
    if is_update == 1:
        if answr:
            update_pc_in_account(email)
    return answr  # dict = ip_dict - logged in successfully | False = email doesn't exist / error logging in

def change_password(email, password, new_password):
    send_object = json.dumps({'action': 'CHANGE_PASSWORD', 'email': email, 'password': password, 'new_password': new_password}).encode(FORMAT)
    return send_to_server(send_object)  # True =  password changed | False = password didn't change

def get_icons_dict():
    send_object = json.dumps({'action': 'GET_ICONS'}).encode(FORMAT)
    return send_to_server(send_object)  # True =  password changed | False = password didn't change


# DELETE
if __name__ == '__main__':
    print(create_new_user('yanivnash@gmail.com', '123456789', {'192.168.1.20': 'mypc', '192.168.1.1': 'router'}))
    print(create_new_user('yaniv/@gmail.com', 'test', {'192.168.1.1': 'router'}))
    print(check_if_email_exists('yanivnash@gmail.com'))
    print(check_if_email_exists('yaniv/@gmail.com'))
    print(check_if_email_exists('yaniv@gmail.com'))
    print(check_if_email_exists('Yaniv@gmail.com'))
    update_pc_in_account('yanivnash@gmail.com')
    print(login('yaniv/@gmail.com', 'test', False))
    print(login('yanivnash@gmail.com', 'test', True))
    print(login('yanivnash@gmail.com', '123456789', True))
    print(change_password('yaniv/@gmail.com', 'test1', 'new_pass'))
    print(change_password('yaniv/@gmail.com', 'test', 'new_pass'))



    # test = True
    # if test:
    #     print(True)
    # elif test == False:
    #     print(False)
    # else:
    #     print(None)