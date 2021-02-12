"""
A server that can receive multiple requests from multiple clients at the same time - using threads
"""

import socket
import threading
import sqlite3
import random
import string

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import tkinter

from PIL import ImageTk, Image
import json
import datetime
from termcolor import colored
import os

MSG_LEN = 2048
PORT = 5050
FORMAT = 'utf-8'
# SERVER = socket.gethostbyname(socket.gethostname())
SERVER = '0.0.0.0'
ROOT_PROJ_DIR = os.path.dirname(os.path.abspath(__file__))


# def create_icons_dict():
#     global icons_dict
#     icons_dict = dict()
#     icons_list = os.listdir(f'{ROOT_PROJ_DIR}\\icons')
#     for icon in icons_list:
#         icons_dict[icon] = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}\\icons\\{icon}'))


def manage_client_db(conn, addr):
    global answr
    with sqlite3.connect('RFE.db') as db:
        cursor = db.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
        email TEXT PRIMARY KEY NOT NULL,
        password TEXT NOT NULL,
        ip_dict dictionary NOT NULL,
        reset_code TEXT NOT NULL);
        """)

    sqlite3.register_adapter(dict, lambda d: json.dumps(d).encode('utf-8'))
    sqlite3.register_converter("dictionary", lambda d: json.loads(d.decode('utf-8')))

    print(colored(f"\n{datetime.datetime.now()}", "blue"))
    print(colored(f"[CONNECTED] {addr[0]}", "green"))
    msg = conn.recv(MSG_LEN).decode(FORMAT)
    msg = json.loads(msg)
    action = msg["action"]
    if action == "NEW_USER":
        email = msg["email"]
        password = msg["password"]
        ip_dict = msg["ip_dict"]
        try:
            new_user = f"""
                        INSERT INTO users(email,password,ip_dict,reset_code)
                        VALUES(?, ?, ?, ?)
                        """
            cursor.execute(new_user, (email.lower().encode(FORMAT), password.encode(FORMAT), ip_dict, ''.encode(FORMAT)))
            answr = True

            sender_email = 'rfe.noreply@gmail.com'  # sending email
            password = 'RFE123456789'  # sending email's password
            send_to_email = email  # receiving email
            subject = 'Welcome to Remote File Explorer'
            messageHTML = f"""
                        <body style="text-align:center; background-color:#e9eed6;">
                        <h1><span style="color: #496dd0">Hey, {email}</span></h1>
                        <h1>Your account was successfully created!</h1>
                        <img src="https://i.ibb.co/Wy56qnN/email-logo.png" alt="LOGO">
                        <h3>© Remote File Explorer 2021 - Yaniv Nash</h3>
                        </body>
                        """

            # "https://i.ibb.co/Wy56qnN/email-logo.png"
            messagePlain = f"""
                        Hey, {email}
                        Your account was successfully created!
                        © Remote File Explorer - Yaniv Nash - 2021
                        """

            msg = MIMEMultipart('alternative')
            msg['From'] = 'Remote File Explorer'
            msg['To'] = send_to_email
            msg['Subject'] = subject

            # Attach both plain and HTML versions
            msg.attach(MIMEText(messagePlain, 'plain'))
            msg.attach(MIMEText(messageHTML, 'html'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, send_to_email, text)
            server.quit()

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
        pc_ip = msg["name_ip_tup"][0]
        pc_name = msg["name_ip_tup"][1]

        find_user = ("SELECT ip_dict FROM users WHERE email = ?")
        cursor.execute(find_user, [(email.lower().encode(FORMAT))])
        answr = cursor.fetchall()
        if answr:
            ip_dict = json.loads(answr[0][0])
            # dict_values = []
            # for key in ip_dict.keys():
            #     dict_values.append(key)
            if not pc_ip in ip_dict.keys():# dict_values:
                ip_dict[pc_ip] = pc_name
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
        # change the password from the user settings (after login)
        email = msg["email"]
        password = msg["password"]
        new_password = msg["new_password"]
        update_password = "UPDATE users SET password = ? WHERE email = ? AND password = ?"
        cursor.execute(update_password, [(new_password.encode(FORMAT)), (email.lower().encode(FORMAT)), (password.encode(FORMAT))])
        find_user = "SELECT password FROM users WHERE email = ?"
        cursor.execute(find_user, [(email.lower().encode(FORMAT))])
        answr = cursor.fetchall()[0][0].decode(FORMAT)
        if answr:
            if answr == new_password:
                answr = True

                sender_email = 'rfe.noreply@gmail.com'  # sending email
                password = 'RFE123456789'  # sending email's password
                send_to_email = email  # receiving email
                subject = 'Your password was reset'
                messageHTML = f"""
                        <body style="text-align:center; background-color:#e9eed6;">
                        <h1><span style="color: #496dd0">Hey, {email}</span></h1>
                        <h1>Your password was successfully changed!</h1>
                        <img src="https://i.ibb.co/Wy56qnN/email-logo.png" alt="LOGO">
                        <h3>© Remote File Explorer 2021 - Yaniv Nash</h3>
                        </body>
                        """

                # "https://i.ibb.co/Wy56qnN/email-logo.png"
                messagePlain = f"""
                        Hey, {email}
                        Your password was successfully changed!
                        © Remote File Explorer - Yaniv Nash - 2021
                        """

                msg = MIMEMultipart('alternative')
                msg['From'] = 'Remote File Explorer'
                msg['To'] = send_to_email
                msg['Subject'] = subject

                # Attach both plain and HTML versions
                msg.attach(MIMEText(messagePlain, 'plain'))
                msg.attach(MIMEText(messageHTML, 'html'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                text = msg.as_string()
                server.sendmail(sender_email, send_to_email, text)
                server.quit()

            else:
                answr = False
        else:
            answr = False

    elif action == "GET_IP_DICT":
        email = msg["email"]

        find_user = ("SELECT ip_dict FROM users WHERE email = ?")
        cursor.execute(find_user, [(email.lower().encode(FORMAT))])
        answr = cursor.fetchall()
        if answr:
            ip_dict = json.loads(answr[0][0])
            answr = ip_dict
        else:
            answr = False

    # elif action == "GET_ICONS":
    #     answr = icons_dict

    elif action == "DELETE_USER":
        email = msg["email"]
        password = msg["password"]
        find_user = ("SELECT ip_dict FROM users WHERE email = ? AND password = ?")
        cursor.execute(find_user, [(email.lower().encode(FORMAT)), (password.encode(FORMAT))])
        answr = cursor.fetchall()
        if answr:
            answr = True

            sender_email = 'rfe.noreply@gmail.com'  # sending email
            password = 'RFE123456789'  # sending email's password
            send_to_email = email  # receiving email
            subject = 'Welcome to Remote File Explorer'
            messageHTML = f"""
                        <body style="text-align:center; background-color:#e9eed6;">
                        <h1><span style="color: #496dd0">Hey, {email}</span></h1>
                        <h1>Your account was successfully deleted!!</h1>
                        <img src="https://i.ibb.co/Wy56qnN/email-logo.png" alt="LOGO">
                        <h3>© Remote File Explorer 2021 - Yaniv Nash</h3>
                        </body>
                        """

            # "https://i.ibb.co/Wy56qnN/email-logo.png"
            messagePlain = f"""
                        Hey, {email}
                        Your account was successfully deleted!
                        © Remote File Explorer - Yaniv Nash - 2021
                        """

            msg = MIMEMultipart('alternative')
            msg['From'] = 'Remote File Explorer'
            msg['To'] = send_to_email
            msg['Subject'] = subject

            # Attach both plain and HTML versions
            msg.attach(MIMEText(messagePlain, 'plain'))
            msg.attach(MIMEText(messageHTML, 'html'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, send_to_email, text)
            server.quit()

        else:
            answr = False
        delete_user = ("DELETE FROM users WHERE email = ? AND password = ?")
        cursor.execute(delete_user, [(email.lower().encode(FORMAT)), (password.encode(FORMAT))])

    elif action == "TEST_SERVER":
        answr = "SERVER IS UP"

    elif action == "GENERATE_SEND_RESET_CODE":
        reset_code_length = 10
        email = msg["email"]
        update_reset_code = "UPDATE users SET reset_code = ? WHERE email = ?"
        letters_and_digits = string.ascii_letters + string.digits
        reset_code = ''.join((random.choice(letters_and_digits) for _ in range(reset_code_length)))
        cursor.execute(update_reset_code, [(reset_code.encode(FORMAT)), (email.lower().encode(FORMAT))])
        answr = cursor.fetchall()
        find_code = "SELECT reset_code FROM users WHERE email = ?"
        cursor.execute(find_code, [(email.lower().encode(FORMAT))])
        answr = cursor.fetchall()[0][0].decode(FORMAT)
        if answr == reset_code:
            answr = True

            sender_email = 'rfe.noreply@gmail.com'  # sending email
            password = 'RFE123456789'  # sending email's password
            send_to_email = email  # receiving email
            subject = 'Your Password Reset Code'
            messageHTML = f"""
            <body style="text-align:center; background-color:#e9eed6;">
            <h1>Your password reset code is:</h1>
            <h1><span style="color: #496dd0">{reset_code}</span></h1>
            <h1>Go back to the "Remote File Explorer" app and use that code to reset your password and log back in to your account</h1>
            <img src="https://i.ibb.co/Wy56qnN/email-logo.png" alt="LOGO">
            <h3>© Remote File Explorer 2021 - Yaniv Nash</h3>
            </body>
            """
            messagePlain = f"""
            Your password reset code is:
            {reset_code}
            Go back to the "Remote File Explorer" app and use that code to reset your password and log back in to your account
            © Remote File Explorer - Yaniv Nash - 2021
            """

            msg = MIMEMultipart('alternative')
            msg['From'] = 'Remote File Explorer'
            msg['To'] = send_to_email
            msg['Subject'] = subject

            # Attach both plain and HTML versions
            msg.attach(MIMEText(messagePlain, 'plain'))
            msg.attach(MIMEText(messageHTML, 'html'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, send_to_email, text)
            server.quit()

        else:
            answr = False

    elif action == "RESET_PASSWORD":
        email = msg["email"]
        reset_code = msg["reset_code"]
        new_password = msg["new_password"]
        find_user = ("SELECT reset_code FROM users WHERE email = ? AND reset_code = ?")
        cursor.execute(find_user, [(email.lower().encode(FORMAT)), (reset_code.encode(FORMAT))])
        answr = cursor.fetchall()
        if answr:
            update_password = "UPDATE users SET password = ? WHERE email = ? AND reset_code = ?"
            cursor.execute(update_password, [(new_password.encode(FORMAT)), (email.lower().encode(FORMAT)), (reset_code.encode(FORMAT))])
            update_reset_code = "UPDATE users SET reset_code = ? WHERE email = ? AND password = ?"
            cursor.execute(update_reset_code, [(''.encode(FORMAT)), (email.lower().encode(FORMAT)), (new_password.encode(FORMAT))])
            answr = True

            sender_email = 'rfe.noreply@gmail.com'  # sending email
            password = 'RFE123456789'  # sending email's password
            send_to_email = email  # receiving email
            subject = 'Your password was reset'
            messageHTML = f"""
                    <body style="text-align:center; background-color:#e9eed6;">
                    <h1><span style="color: #496dd0">Hey, {email}</span></h1>
                    <h1>Your password was reset successfully!</h1>
                    <img src="https://i.ibb.co/Wy56qnN/email-logo.png" alt="LOGO">
                    <h3>© Remote File Explorer 2021 - Yaniv Nash</h3>
                    </body>
                    """

            # "https://i.ibb.co/Wy56qnN/email-logo.png"
            messagePlain = f"""
                    Hey, {email}
                    Your password was reset successfully!
                    © Remote File Explorer - Yaniv Nash - 2021
                    """

            msg = MIMEMultipart('alternative')
            msg['From'] = 'Remote File Explorer'
            msg['To'] = send_to_email
            msg['Subject'] = subject

            # Attach both plain and HTML versions
            msg.attach(MIMEText(messagePlain, 'plain'))
            msg.attach(MIMEText(messageHTML, 'html'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, send_to_email, text)
            server.quit()
        else:
            answr = False

    else:
        answr = None

    db.commit()
    conn.send(json.dumps(answr).encode(FORMAT))
    # conn.send(str(answr).encode(FORMAT))
    if type(answr) == type(dict()):
        print(colored(f"{action} - True"))
    else:
        print(colored(f"{action} - {answr}"))
    conn.close()
    print(colored(f"[DISCONNECTED] {addr[0]}", "red"))

    # DELETE
    cursor.execute("""SELECT * FROM users""")
    print(cursor.fetchall())
    # DELETE


def start_server():
    # temp_root = tkinter.Tk()
    # create_icons_dict()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER, PORT))
    print(colored("[STARTING] Server is up", "yellow"))
    server.listen()
    print(colored(f"[LISTENING] Server is listening - 84.111.109.58:{PORT}", "yellow"))
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=manage_client_db, args=(conn, addr))
        thread.start()
        # print(f"{threading.activeCount()-1} [ACTIVE CONNECTIONS]")


if __name__ == '__main__':
    start_server()