__author__ = 'Yaniv Nash'

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
    except TimeoutError:
        return 'SERVER IS DOWN'
    except ConnectionRefusedError:
        return 'ERROR'


def create_new_user(email, password):
    send_object = json.dumps({'action': 'NEW_USER', 'email': email, 'password': password, 'ip_dict': {}}).encode(FORMAT)
    answr = send_to_server(send_object)
    if answr:
        pc_ip = socket.gethostbyname(socket.gethostname())
        pc_name = os.getlogin()
        name_ip_tup = (pc_ip, pc_name)
        update_pc_in_account(email, name_ip_tup)
    return answr  # True =  user created | False = user not created


def check_if_email_exists(email):
    send_object = json.dumps({'action': 'CHECK_EMAIL', 'email': email}).encode(FORMAT)
    return send_to_server(send_object)  # True =  email exists | False = email doesn't exist


def update_pc_in_account(email, name_ip_tup):  # name_ip_tup = ('pc_username', 'pc_ip')
    send_object = json.dumps({'action': 'UPDATE_PC', 'email': email, 'name_ip_tup': name_ip_tup}).encode(FORMAT)
    send_to_server(send_object)  # maybe delete this note and not return anything
    # True =  pc was in account / pc wasn't in account and now is | False = pc wasn't in account but adding hit an error


def login(email, password, is_update):
    send_object = json.dumps({'action': 'LOGIN', 'email': email, 'password': password}).encode(FORMAT)
    answr = send_to_server(send_object)
    if is_update == 1:
        if answr:
            pc_ip = socket.gethostbyname(socket.gethostname())
            pc_name = os.getlogin()
            name_ip_tup = (pc_ip, pc_name)
            update_pc_in_account(email, name_ip_tup)
    return answr  # True - logged in successfully | False = email doesn't exist / error logging in


def change_password(email, password, new_password):
    send_object = json.dumps({'action': 'CHANGE_PASSWORD', 'email': email, 'password': password, 'new_password': new_password}).encode(FORMAT)
    return send_to_server(send_object)  # True = password changed | False = password didn't change


def get_ip_dict(email):
    send_object = json.dumps({'action': 'GET_IP_DICT', 'email': email}).encode(FORMAT)
    return send_to_server(send_object)  # *dict* = success | False = user not found


def delete_account(email, password):
    send_object = json.dumps({'action': 'DELETE_USER', 'email': email, 'password': password}).encode(FORMAT)
    return send_to_server(send_object)  # True = account deleted | False = account wasn't deleted


def get_server_status():
    send_object = json.dumps({'action': 'TEST_SERVER'}).encode(FORMAT)
    return send_to_server(send_object)


def generate_and_send_reset_code(email):
    send_object = json.dumps({'action': 'GENERATE_SEND_RESET_CODE', 'email': email}).encode(FORMAT)
    return send_to_server(send_object)  # True = reset code was generated and updated in the account | False = reset code did not generate


# def check_reset_code(email, reset_code):
#     send_object = json.dumps({'action': 'CHECK_RESET_CODE', 'email': email, 'reset_code': reset_code}).encode(FORMAT)
#     return send_to_server(send_object)  # True = reset code and email match | False = reset code and email DON'T match


def reset_password(email, reset_code, new_password):
    send_object = json.dumps({'action': 'RESET_PASSWORD', 'email': email, 'reset_code': reset_code, 'new_password': new_password}).encode(FORMAT)
    return send_to_server(send_object)  # True = password reset | False = password didn't reset

# if __name__ == '__main__':
#     print(delete_account('yanivnash1@gmail.com', '123'))

# def get_icons_dict():
#     send_object = json.dumps({'action': 'GET_ICONS'}).encode(FORMAT)
#     return send_to_server(send_object)  # True =  password changed | False = password didn't change


# DELETE
# if __name__ == '__main__':
#     print(create_new_user('yanivnash@gmail.com', '1'))
#     print(login('yanivnash@gmail.com', '1234', 0))
#     print(generate_and_send_reset_code('yanivnash@gmail.com'))
#     print(reset_password('yanivnash@gmail.com', 'OP2SI7mdkj', '1234'))
#     print(get_icons_dict())
#     print(create_new_user('yanivnash@gmail.com', '123456789'))
#     print(create_new_user('ronitnash5@gmail.com', 'ronit5'))
#     print(create_new_user('yaniv/@gmail.com', 'test', {'router': '192.168.1.1'}))
#     print(check_if_email_exists('yanivnash@gmail.com'))
#     print(check_if_email_exists('yaniv/@gmail.com'))
#     print(check_if_email_exists('yaniv@gmail.com'))
#     print(check_if_email_exists('Yaniv@gmail.com'))
#     update_pc_in_account('yanivnash@gmail.com')
#     print(login('yaniv/@gmail.com', 'test', False))
#     print(login('yanivnash@gmail.com', 'test', True))
#     print(login('yanivnash@gmail.com', '123456789', True))
#     print(get_ip_dict('yanivnash@gmail.com'))
#     print(change_password('yaniv/@gmail.com', 'test1', 'new_pass'))
#     print(change_password('yaniv/@gmail.com', 'test', 'new_pass'))



    # test = True
    # if test:
    #     print(True)
    # elif test == False:
    #     print(False)
    # else:
    #     print(None)