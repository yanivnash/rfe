__author__ = 'Yaniv Nash'

import paramiko
import stat


def connect_to_ssh(host, username, password):
    port = 22

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, port, username, password)
        return ssh
    except paramiko.ssh_exception.NoValidConnectionsError:
        return "no connection"
    except paramiko.ssh_exception.AuthenticationException:
        return "wrong password/username"
    except TimeoutError:
        return "timeout"


def disconnect_ssh(ssh):
    if ssh:
        try:
            ssh.close()
        except:
            pass


def chdir(sftp, path):
    try:
        sftp.chdir(path)
        return True
    except FileNotFoundError:
        try:
            sftp.chdir(None)
            sftp.chdir(path)
        except FileNotFoundError:
            return 'path not found'


def run_action(ssh, action):
    stdin, stdout, stderr = ssh.exec_command(action)
    return stdout


def cmd_terminal(ssh, cmnd):
    stdin, stdout, stderr = ssh.exec_command(cmnd)
    return stdin, stdout, stderr


def check_if_item_is_dir(sftp, cur_path, item_name):
    chdir(sftp, cur_path)
    for file in sftp.listdir_attr():
        if str(file)[55:] == item_name:
            if stat.S_ISDIR(file.st_mode):
                return 'dir'
            else:
                return 'file'
    return 'item not found'


def get_dirs_files_lists(sftp, path):
    files_list = list()
    dirs_list = list()
    chdir(sftp, path)
    for file in sftp.listdir_attr():
        if stat.S_ISDIR(file.st_mode):
            dirs_list.append(str(file))
        else:
            files_list.append(str(file))

    for dir_i in range(len(dirs_list)):
        dirs_list[dir_i] = dirs_list[dir_i][55:]
    for file_i in range(len(files_list)):
        files_list[file_i] = files_list[file_i][55:]
    return dirs_list, files_list


def tree_items(sftp, remotedir, tree_list, search_key, plat):
    for item in sftp.listdir_attr(remotedir):
        if plat == 'windows':
            remotepath = remotedir + '\\' + item.filename
        else:
            remotepath = remotedir + '/' + item.filename
        mode = item.st_mode
        if stat.S_ISDIR(mode):
            tree_items(sftp, remotepath, tree_list, search_key, plat)
            if item.filename.lower().__contains__(search_key.lower()):
                tree_list.append(remotepath)
        elif stat.S_ISREG(mode):
            if item.filename.lower().__contains__(search_key.lower()):
                tree_list.append(remotepath)
    return tree_list
