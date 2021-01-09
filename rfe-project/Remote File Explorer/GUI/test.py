import manageSSH, stat, re#, pyngrok
from pyngrok import ngrok

host = "84.111.109.58"
username = "yaniv-pc\yaniv"
password = 'Yanivn911911'  # DELETE
# ssh = manageSSH.connect_to_ssh(host, username, password)
# sftp = ssh.open_sftp()
#
# cur_path = r'C:\Users\yaniv\Desktop\Remote File Explorer'
# # paths_list = [r'C:\Users\yaniv', r'\Desktop', r'\Remote File Explorer']
#
# item_name = 'My Logo.png'
# # print(manageSSH.check_if_item_is_dir(sftp, cur_path, item_name))
# # temp = cur_path + '\\' + item_name
# temp = r'C:\Users\yaniv\Desktop\Remote File Explorer\My Project.docx'
# # manageSSH.chdir(sftp, cur_path)
# manageSSH.run_action(ssh, f'"{temp}"')
#
#
# manageSSH.disconnect_ssh(ssh)


# import socket
# ssh_tunnel = ngrok.connect(22)
#
# tunnels = ngrok.get_tunnels()
#
# print(tunnels)
# print(socket.gethostbyname(socket.gethostname()))
# print(socket.gethostname())

# ngrok.disconnect(ssh_tunnel.public_url)


# import socket
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# host = socket.gethostbyname(socket.gethostname())
# port = 22
#
# sock.bind((host, port))
# print(f'port={port}')
# print('bind')
# sock.listen(1)
# print('listen')
# conn, addr = sock.accept()
# print('accept')

import manageSSH

host = "2.53.26.73"
username = "lilac"
password = ''  # DELETE
ssh = manageSSH.connect_to_ssh(host, username, password)
sftp = ssh.open_sftp()