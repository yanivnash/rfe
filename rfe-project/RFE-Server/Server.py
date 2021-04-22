__author__ = 'Yaniv Nash'

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
import json
import datetime
from termcolor import colored
import os
import requests


class server(object):
    def __init__(self):
        self.MSG_LEN = 2048
        self.PORT = 5050
        self.FORMAT = 'utf-8'
        self.LOCAL_IP = socket.gethostbyname(socket.gethostname())
        self.EXTERNAL_IP = requests.get('http://ip.42.pl/raw').text
        self.SERVER = '0.0.0.0'
        self.ROOT_PROJ_DIR = os.path.dirname(os.path.abspath(__file__))


    def start_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.SERVER, self.PORT))
        print(colored("[STARTING] Server is up", "yellow"))
        server.listen()
        print(colored(f"[LISTENING] Server is listening - {self.EXTERNAL_IP}:{self.PORT} | {self.LOCAL_IP}:{self.PORT}", "yellow"))
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=self.manage_client_db, args=(conn, addr))
            thread.start()


    def manage_client_db(self, conn, addr):
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
        msg = conn.recv(self.MSG_LEN).decode(self.FORMAT)
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
                cursor.execute(new_user, (email.lower().encode(self.FORMAT), password.encode(self.FORMAT), ip_dict, ''.encode(self.FORMAT)))
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
                messagePlain = f"""
                            Hey, {email}
                            Your account was successfully created!
                            © Remote File Explorer 2021 - Yaniv Nash
                            """

                msg = MIMEMultipart('alternative')
                msg['From'] = 'Remote File Explorer'
                msg['To'] = send_to_email
                msg['Subject'] = subject

                msg.attach(MIMEText(messagePlain, 'plain'))
                msg.attach(MIMEText(messageHTML, 'html'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                text = msg.as_string()
                try:
                    server.sendmail(sender_email, send_to_email, text)
                except smtplib.SMTPRecipientsRefused:
                    answr = 'EMAIL NOT SENT'
                finally:
                    server.quit()

            except sqlite3.IntegrityError:
                answr = False
                print('email already exists')
            finally:
                db.commit()

        elif action == "CHECK_EMAIL":
            email = msg["email"]
            find_email = ("SELECT * FROM users WHERE email = ?")
            cursor.execute(find_email, [(email.lower().encode(self.FORMAT))])
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
            cursor.execute(find_user, [(email.lower().encode(self.FORMAT))])
            answr = cursor.fetchall()
            if answr:
                ip_dict = json.loads(answr[0][0])
                if not pc_ip in ip_dict.keys():
                    ip_dict[pc_ip] = pc_name
                    update_ip_dict = "UPDATE users SET ip_dict = ? WHERE email = ?"
                    cursor.execute(update_ip_dict, [(ip_dict), (email.lower().encode(self.FORMAT))])
                answr = ip_dict
            else:
                answr = False

        elif action == "LOGIN":
            email = msg["email"]
            password = msg["password"]
            find_user = ("SELECT ip_dict FROM users WHERE email = ? AND password = ?")
            cursor.execute(find_user, [(email.lower().encode(self.FORMAT)), (password.encode(self.FORMAT))])
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
            cursor.execute(update_password, [(new_password.encode(self.FORMAT)), (email.lower().encode(self.FORMAT)), (password.encode(self.FORMAT))])
            find_user = "SELECT password FROM users WHERE email = ?"
            cursor.execute(find_user, [(email.lower().encode(self.FORMAT))])
            answr = cursor.fetchall()[0][0].decode(self.FORMAT)
            if answr:
                if answr == new_password:
                    answr = True

                    sender_email = 'rfe.noreply@gmail.com'  # sending email
                    password = 'RFE123456789'  # sending email's password
                    send_to_email = email  # receiving email
                    subject = 'Your password was changed'
                    messageHTML = f"""
                            <body style="text-align:center; background-color:#e9eed6;">
                            <h1><span style="color: #496dd0">Hey, {email}</span></h1>
                            <h1>Your password was changed successfully!</h1>
                            <img src="https://i.ibb.co/Wy56qnN/email-logo.png" alt="LOGO">
                            <h3>© Remote File Explorer 2021 - Yaniv Nash</h3>
                            </body>
                            """

                    messagePlain = f"""
                            Hey, {email}
                            Your password was changed successfully!
                            © Remote File Explorer 2021 - Yaniv Nash
                            """

                    msg = MIMEMultipart('alternative')
                    msg['From'] = 'Remote File Explorer'
                    msg['To'] = send_to_email
                    msg['Subject'] = subject

                    msg.attach(MIMEText(messagePlain, 'plain'))
                    msg.attach(MIMEText(messageHTML, 'html'))

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(sender_email, password)
                    text = msg.as_string()
                    try:
                        server.sendmail(sender_email, send_to_email, text)
                    except smtplib.SMTPRecipientsRefused:
                        answr = 'EMAIL NOT SENT'
                    finally:
                        server.quit()

                else:
                    answr = False
            else:
                answr = False

        elif action == "GET_IP_DICT":
            email = msg["email"]

            find_user = ("SELECT ip_dict FROM users WHERE email = ?")
            cursor.execute(find_user, [(email.lower().encode(self.FORMAT))])
            answr = cursor.fetchall()
            if answr:
                ip_dict = json.loads(answr[0][0])
                answr = ip_dict
            else:
                answr = False

        elif action == "DELETE_USER":
            email = msg["email"]
            password = msg["password"]
            find_user = ("SELECT ip_dict FROM users WHERE email = ? AND password = ?")
            cursor.execute(find_user, [(email.lower().encode(self.FORMAT)), (password.encode(self.FORMAT))])
            answr = cursor.fetchall()
            if answr:
                answr = True

                delete_user = ("DELETE FROM users WHERE email = ? AND password = ?")
                cursor.execute(delete_user, [(email.lower().encode(self.FORMAT)), (password.encode(self.FORMAT))])

                sender_email = 'rfe.noreply@gmail.com'  # sending email
                password = 'RFE123456789'  # sending email's password
                send_to_email = email  # receiving email
                subject = 'Remote File Explorer'
                messageHTML = f"""
                            <body style="text-align:center; background-color:#e9eed6;">
                            <h1><span style="color: #496dd0">Hey, {email}</span></h1>
                            <h1>Your account was successfully deleted!</h1>
                            <img src="https://i.ibb.co/Wy56qnN/email-logo.png" alt="LOGO">
                            <h3>© Remote File Explorer 2021 - Yaniv Nash</h3>
                            </body>
                            """

                messagePlain = f"""
                            Hey, {email}
                            Your account was successfully deleted!
                            © Remote File Explorer 2021 - Yaniv Nash
                            """

                msg = MIMEMultipart('alternative')
                msg['From'] = 'Remote File Explorer'
                msg['To'] = send_to_email
                msg['Subject'] = subject

                msg.attach(MIMEText(messagePlain, 'plain'))
                msg.attach(MIMEText(messageHTML, 'html'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                text = msg.as_string()
                try:
                    server.sendmail(sender_email, send_to_email, text)
                except smtplib.SMTPRecipientsRefused:
                    answr = 'ERROR'
                finally:
                    server.quit()

            else:
                answr = False

        elif action == "TEST_SERVER":
            answr = "SERVER IS UP"

        elif action == "GENERATE_SEND_RESET_CODE":
            reset_code_length = 10
            email = msg["email"]
            update_reset_code = "UPDATE users SET reset_code = ? WHERE email = ?"
            letters_and_digits = string.ascii_letters + string.digits
            reset_code = ''.join((random.choice(letters_and_digits) for _ in range(reset_code_length)))
            cursor.execute(update_reset_code, [(reset_code.encode(self.FORMAT)), (email.lower().encode(self.FORMAT))])
            answr = cursor.fetchall()
            find_code = "SELECT reset_code FROM users WHERE email = ?"
            cursor.execute(find_code, [(email.lower().encode(self.FORMAT))])
            answr = cursor.fetchall()[0][0].decode(self.FORMAT)
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
                © Remote File Explorer 2021 - Yaniv Nash
                """

                msg = MIMEMultipart('alternative')
                msg['From'] = 'Remote File Explorer'
                msg['To'] = send_to_email
                msg['Subject'] = subject

                msg.attach(MIMEText(messagePlain, 'plain'))
                msg.attach(MIMEText(messageHTML, 'html'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                text = msg.as_string()
                try:
                    server.sendmail(sender_email, send_to_email, text)
                except smtplib.SMTPRecipientsRefused:
                    answr = 'ERROR'
                finally:
                    server.quit()

            else:
                answr = False

        elif action == "RESET_PASSWORD":
            email = msg["email"]
            reset_code = msg["reset_code"]
            new_password = msg["new_password"]
            find_user = ("SELECT reset_code FROM users WHERE email = ? AND reset_code = ?")
            cursor.execute(find_user, [(email.lower().encode(self.FORMAT)), (reset_code.encode(self.FORMAT))])
            answr = cursor.fetchall()
            if answr:
                update_password = "UPDATE users SET password = ? WHERE email = ? AND reset_code = ?"
                cursor.execute(update_password,
                               [(new_password.encode(self.FORMAT)), (email.lower().encode(self.FORMAT)),
                                (reset_code.encode(self.FORMAT))])
                update_reset_code = "UPDATE users SET reset_code = ? WHERE email = ? AND password = ?"
                cursor.execute(update_reset_code, [(''.encode(self.FORMAT)), (email.lower().encode(self.FORMAT)),
                                                   (new_password.encode(self.FORMAT))])
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

                messagePlain = f"""
                        Hey, {email}
                        Your password was reset successfully!
                        © Remote File Explorer 2021 - Yaniv Nash
                        """

                msg = MIMEMultipart('alternative')
                msg['From'] = 'Remote File Explorer'
                msg['To'] = send_to_email
                msg['Subject'] = subject

                msg.attach(MIMEText(messagePlain, 'plain'))
                msg.attach(MIMEText(messageHTML, 'html'))

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                text = msg.as_string()
                try:
                    server.sendmail(sender_email, send_to_email, text)
                except smtplib.SMTPRecipientsRefused:
                    answr = 'ERROR'
                finally:
                    server.quit()
            else:
                answr = False

        elif action == "RESET_IP_DICT":
            email = msg["email"]
            password = msg["password"]
            find_user = ("SELECT ip_dict FROM users WHERE email = ? AND password = ?")
            cursor.execute(find_user, [(email.lower().encode(self.FORMAT)), (password.encode(self.FORMAT))])
            answr = cursor.fetchall()
            if answr:
                update_ip_dict = "UPDATE users SET ip_dict = ? WHERE email = ? AND password = ?"
                cursor.execute(update_ip_dict,
                               [({}), (email.lower().encode(self.FORMAT)), (password.encode(self.FORMAT))])
                answr = True
            else:
                answr = False

        else:
            answr = None

        db.commit()
        conn.send(json.dumps(answr).encode(self.FORMAT))
        if type(answr) == type(dict()):
            print(colored(f"{action} - True"))
        else:
            print(colored(f"{action} - {answr}"))
        conn.close()
        print(colored(f"[DISCONNECTED] {addr[0]}", "red"))

        # # PRINT THE DB
        # cursor.execute("""SELECT * FROM users""")
        # print(cursor.fetchall())
        # # PRINT THE DB


if __name__ == '__main__':
    s = server()
    s.start_server()