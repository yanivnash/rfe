import socket
import sqlite3

# s = socket.socket()
# IP = socket.gethostbyname(socket.gethostname())
# PORT = 5050
# FORMAT = 'utf-8'
# MSG_LEN = 2048
# s.bind((IP, PORT))
# s.listen()
#
# print('Listening for connections...')
# conn, addr = s.accept()
# print('OK')
# conn.send(file_ending.encode(FORMAT))
# conn.recv(MSG_LEN).decode(FORMAT)
#
# s.close()

with sqlite3.connect('RFE.db') as db:
    cursor = db.cursor()

# PRIMARY KEY
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
    email TEXT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL,
    ip_dict dictionary NOT NULL);
    """)

import json

FORMAT = 'utf-8'

sqlite3.register_adapter(dict, lambda d: json.dumps(d).encode(FORMAT))
sqlite3.register_converter("dictionary", lambda d: json.loads(d.decode(FORMAT)))

email = "yaniv/@gmail.com"
password = "123456789"
ip_dict = {'yaniv': '192.168.1.20', 'router': '192.168.1.1'}

# try:
#     new_user = f"""
#             INSERT INTO users(email,password,ip_dict)
#             VALUES(?, ?, ?)
#             """
#     cursor.execute(new_user, (email, password.encode(FORMAT), ip_dict))  # passing a dictionary and not a string
#
#     # cursor.execute(f"""
#     #     INSERT INTO users(email,password,ip_dict)
#     #     VALUES("yanivs mail", "123456789", "{ip_dict}")
#     #     """)
# except sqlite3.IntegrityError:
#     print('ERROR')
# finally:
#     db.commit()

email = 'yanivnash@gmail.com'
find_user = ("SELECT ip_dict FROM users WHERE email = ?")
cursor.execute(find_user, [(email.lower())])
answr = cursor.fetchall()
print(answr[0][0])
if answr:
    ip_dict = json.loads(answr[0][0])
    print(ip_dict.keys())

# cursor.execute('SELECT * FROM users')
# rows = cursor.fetchall()
# print(rows)
# for row in rows:
#     print(json.loads(row[2].decode('utf-8')))
#     print(type(json.loads(row[2].decode('utf-8'))))

# new_ip_dict = {'yaniv-pc': '192.168.1.20'}
# update_ip_dict = "UPDATE users SET ip_dict = ? WHERE email = ?"
# cursor.execute(update_ip_dict, [(new_ip_dict), (email.lower())])


# cursor.execute('SELECT * FROM users')
# rows = cursor.fetchall()
# print(rows)
# for row in rows:
#     print(json.loads(row[0].decode('utf-8')))
#     print(type(json.loads(row[2].decode('utf-8'))))
#     # print(type(json.loads(row[2].decode('utf-8'))))  # when selecting * from users
#
# cursor.execute('SELECT ip_dict FROM users')
# rows = cursor.fetchall()
# print(rows)
# for row in rows:
#     print(json.loads(row[0].decode('utf-8')))
#     print(type(json.loads(row[0].decode('utf-8'))))
#     # print(type(json.loads(row[2].decode('utf-8'))))  # when selecting * from users


# find_user = ("SELECT ip_dict FROM users WHERE email = ? AND password = ?")
# cursor.execute(find_user, [(email.lower()), (password)])
# answr = cursor.fetchall()
# if answr:
#     print(answr)
# else:
#     print('no')

# cursor.execute("""SELECT * FROM users """)
# print(cursor.fetchall())
#
# db.commit()


# cursor.execute("""SELECT ip_dict FROM users""")
# all = cursor.fetchall()
# dicti = all[0][0]
# print(all)
# new = json.loads(json.dumps(dicti))
# print(new)
# # new = new.replace("'", '"')
# print(new)
# new = json.loads(dicti)
# print(new)
# print(type(new))
# # str_dict = f'"{all}"'
# # load = json.loads(str_dict)
# # print(json.loads(load))
# # print(type(load))
#
# db.commit()