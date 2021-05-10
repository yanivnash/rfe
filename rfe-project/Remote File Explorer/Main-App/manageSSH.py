__author__ = 'Yaniv Nash'

import paramiko
import stat


def connect_to_ssh(host, username, password):
    """
    Connects to a client using the IP address, username and password.
    :param host: the user's IP address
    :param username: the user's username
    :param password: the user's password
    :return: ssh - SSH object that contains the connection info
            "no connection" - if the connection wasn't successful
            "wrong password/username" - if the IP address / username / password don't match
            "timeout" - if there was no response after some time
    """
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
    """
    Disconnects from the client.
    :param ssh: SSH object that contains the connection info
    :return: None
    """
    if ssh:
        try:
            ssh.close()
        except:
            pass


def chdir(sftp, path):
    """
    Goes to a different path in the remote computer.
    :param sftp: SFTP object
    :param path: The path to change to
    :return: True - path changed successfully
            'path not found' - the path was not found
    """
    try:
        sftp.chdir(path)
        return True
    except FileNotFoundError:
        try:
            sftp.chdir(None)
            sftp.chdir(path)
        except FileNotFoundError:
            return 'path not found'


def run_action(ssh, cmnd):
    """
    Runs a command on the remote computer.
    :param ssh: SSH object that contains the connection info
    :param cmnd: The command that needs to be ran
    :return: stdout - the result from the run.
    """
    stdin, stdout, stderr = ssh.exec_command(cmnd)
    return stdout


def cmd_terminal(ssh, cmnd):
    """
    Runs a command on the remote computer.
    :param ssh: SSH object that contains the connection info
    :param cmnd: The command that needs to be ran
    :return: stdin - the input from the run
            stdout - the result from the run
            stderr - if an error that occurred during the run
    """
    stdin, stdout, stderr = ssh.exec_command(cmnd)
    return stdin, stdout, stderr


def check_if_item_is_dir(sftp, cur_path, item_name):
    """
    Checks if an item is a directory or a file.
    :param sftp: SFTP object
    :param cur_path: The item's parent folder's path
    :param item_name: The name of the item
    :return: 'dir' - if the item is a directory
            'file' - if the item is a file
            'item not found' - if the item was not found.
    """
    chdir(sftp, cur_path)
    for item in sftp.listdir_attr():
        if str(item)[55:] == item_name:
            if stat.S_ISDIR(item.st_mode):
                return 'dir'
            else:
                return 'file'
    return 'item not found'


def get_dirs_files_lists(sftp, path):
    """
    Gets two lists - one with folders names and another with files names.
    :param sftp: SFTP object
    :param path: The path where the folders and files are
    :return: dirs_list - a list with the folders names
            files_list - a list with the files names
    """
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


def search_tree_items(sftp, remotedir, tree_list, search_key, plat):
    """
    Gets a list with all the paths of folders and files with the search key in their names.
    :param sftp: SFTP object
    :param remotedir: The path to search in for folders and files with the search key
    :param tree_list: An empty list that after running the func will contain all the items
    :param search_key: The value to be searched
    :param plat: The os of the remote computer
    :return: tree_list - a list with all the
    """
    if plat == 'windows':
        dir_sign = '\\'
    else:
        dir_sign = '/'
    for item in sftp.listdir_attr(remotedir):
        remotepath = remotedir + dir_sign + item.filename
        mode = item.st_mode
        if stat.S_ISDIR(mode):
            search_tree_items(sftp, remotepath, tree_list, search_key, plat)
            if item.filename.lower().__contains__(search_key.lower()):
                tree_list.append(remotepath)
        elif stat.S_ISREG(mode):
            if item.filename.lower().__contains__(search_key.lower()):
                tree_list.append(remotepath)
    return tree_list
