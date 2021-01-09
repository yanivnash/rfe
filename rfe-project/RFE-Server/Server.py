"""
A server that can receive multiple requests from multiple clients at the same time - using threads
"""

import socket
import threading
import sqlite3
import json
import datetime
from termcolor import colored

MSG_LEN = 2048
PORT = 5050
FORMAT = 'utf-8'
SERVER = socket.gethostbyname(socket.gethostname())


def manage_client_db(conn, addr):
    with sqlite3.connect('RFE.db') as db:
        cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
        email TEXT PRIMARY KEY NOT NULL,
        password TEXT NOT NULL,
        ip_dict dictionary NOT NULL);
        """)

    # maybe delete and just store the pictures on the local server
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS assets(
    # pic_name VARCHAR(max) PRIMARY KEY NOT NULL,
    # pic VARCHAR(max) NOT NULL);
    # """)

    sqlite3.register_adapter(dict, lambda d: json.dumps(d).encode('utf-8'))
    sqlite3.register_converter("dictionary", lambda d: json.loads(d.decode('utf-8')))

    print(colored(f"\n{datetime.datetime.now()}", "blue"))
    print(colored(f"[CONNECTED] {addr[0]}", "green"))
    # answr = None
    msg = conn.recv(MSG_LEN).decode(FORMAT)
    msg = json.loads(msg)
    action = msg["action"]
    if action == "NEW_USER":
        email = msg["email"]
        password = msg["password"]
        ip_dict = msg["ip_dict"]
        try:
            new_user = f"""
                        INSERT INTO users(email,password,ip_dict)
                        VALUES(?, ?, ?)
                        """
            cursor.execute(new_user, (email.lower().encode(FORMAT), password.encode(FORMAT), ip_dict))
            answr = True
        except sqlite3.IntegrityError:
            answr = False
            print('email already exists')
        finally:
            db.commit()

    elif action == "CHECK_EMAIL":
        email = msg["email"]
        find_email = ("SELECT * FROM users WHERE email = ?")
        cursor.execute(find_email, [(email.lower().encode(FORMAT))])
        answr = cursor.fetchall()
        if answr:
            answr = True
        else:
            answr = False

    elif action == "UPDATE_PC":
        email = msg["email"]
        pc_name = msg["name_ip_tup"][0]
        pc_ip = msg["name_ip_tup"][1]
        find_user = ("SELECT ip_dict FROM users WHERE email = ?")
        cursor.execute(find_user, [(email.lower().encode(FORMAT))])
        answr = cursor.fetchall()
        if answr:
            ip_dict = json.loads(answr[0][0])
            dict_values = []
            for _, value in ip_dict.items():
                dict_values.append(value)
            if not pc_ip in dict_values:
                ip_dict[pc_name] = pc_ip
                update_ip_dict = "UPDATE users SET ip_dict = ? WHERE email = ?"
                cursor.execute(update_ip_dict, [(ip_dict), (email.lower().encode(FORMAT))])
            answr = ip_dict
        else:
            answr = False


    elif action == "LOGIN":
        email = msg["email"]
        password = msg["password"]
        find_user = ("SELECT ip_dict FROM users WHERE email = ? AND password = ?")
        cursor.execute(find_user, [(email.lower().encode(FORMAT)), (password.encode(FORMAT))])
        answr = cursor.fetchall()
        if answr:
            answr = True
        else:
            answr = False

    elif action == "CHANGE_PASSWORD":
        email = msg["email"]
        password = msg["password"]
        new_password = msg["new_password"]
        update_password = "UPDATE users SET password = ? WHERE email = ? AND password = ?"
        cursor.execute(update_password, [(new_password.encode(FORMAT)), (email.lower().encode(FORMAT)), (password.encode(FORMAT))])
        find_user = ("SELECT password FROM users WHERE email = ?")
        cursor.execute(find_user, [(email.lower().encode(FORMAT))])
        answr = cursor.fetchall()[0][0].decode(FORMAT)
        if answr:
            if answr == new_password:
                answr = True
            else:
                answr = False
        else:
            answr = False

    elif action == "GET_ICON":
        pass

    else:
        answr = None

    db.commit()
    conn.send(json.dumps(answr).encode(FORMAT))
    # conn.send(str(answr).encode(FORMAT))
    print(colored(f"{action} - {answr}"))
    conn.close()
    print(colored(f"[DISCONNECTED] {addr[0]}", "red"))

    # DELETE
    cursor.execute("""SELECT * FROM users""")
    print(cursor.fetchall())
    # DELETE


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER, PORT))
    print(colored("[STARTING] Server is up", "yellow"))
    server.listen()
    print(colored(f"[LISTENING] Server is listening - {SERVER}:{PORT}", "yellow"))
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=manage_client_db, args=(conn, addr))
        thread.start()
        # print(f"{threading.activeCount()-1} [ACTIVE CONNECTIONS]")


if __name__ == '__main__':
    start_server()