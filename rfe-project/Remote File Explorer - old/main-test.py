import tkinter
import os
import fs
import paramiko
from fs.sshfs import SSHFS
import getpass
import sshtunnel
import socket
from ssh2.session import Session
import subprocess



def main():
    host = "84.111.109.58"
    port = 22
    username = "yaniv-pc\yaniv"
    password = 'Yanivn911911' # DELETE
    # password = input('Enter password: ')
    # password = getpass.getpass('Enter password: ')

    command_path = r'Desktop\apple'
    command1 = fr'dir {command_path} /b'
    command2 = fr'dir {command_path}'

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)


        stdin, stdout, stderr = ssh.exec_command(command1)
        stdin2, stdout2, stderr2 = ssh.exec_command(command2)
        files = stdout.readlines()
        files_info = stdout2.readlines()
        # print(files)
        print(files_info[3][14:])  # the path

        files_list = list()
        dirs_list = list()
        for i in range(len(files)):
            if files[i] in files_info[i + 7]:
                if '<DIR>' in files_info[i + 7]:
                    end_index = files[i].find(r'\r\n')
                    dirs_list.append(files[i][:end_index - 1])
                else:
                    end_index = files[i].find(r'\r\n')
                    files_list.append(files[i][:end_index - 1])
        items_list = dirs_list + files_list
        print(items_list)

    except paramiko.ssh_exception.NoValidConnectionsError:
        print("Can't connect")


def not_good():
    ssh_host = "84.111.109.58"
    ssh_port = 22
    userna = "yaniv-pc\yaniv"
    passw = 'Yanivn911911'  # DELETE
    REMOTE_HOST = "84.111.109.58"
    REMOTE_PORT = 22
    with sshtunnel.open_tunnel((ssh_host, ssh_port), ssh_host_key=None, ssh_username=userna, ssh_password=passw, ssh_private_key=None, remote_bind_address=(REMOTE_HOST, REMOTE_PORT)) as server:
        print("LOCAL PORT:", server.local_bind_port)


if __name__ == '__main__':
    # if not 'OpenSSH SSH Server' in os.popen('Get-Service'):
    #     cmd = "Get-WindowsCapability -Online | ? Name -like 'OpenSSH*'"
    #     completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    #     print(completed)
    port = 22
    host = "84.111.109.58"
    user = "yaniv-pc\yaniv"
    password = 'Yanivn911911'

    local_ip = socket.gethostbyname(socket.gethostname())
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((local_ip, port))

    session = Session()
    session.handshake(sock)
    session.userauth_password(user, password)

    channel1 = session.open_session()
    channel1.execute('show run')
    size, data = channel1.read()
    while size > 0:
        print(data.decode())
        size, data = channel1.read()
    channel1.close()
    print(f'Exit Status: {channel1.get_exit_signal()}')