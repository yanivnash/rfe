__author__ = 'Yaniv Nash'

import paramiko
import stat


def connect_to_ssh(host, username, password):
    PORT = 22
    # port = 5555

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host, PORT, username, password)
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

# def check_if_path_exists(sftp, path):
#     try:
#         chdir(sftp, path)
#     except FileNotFoundError:
#         return

def chdir(sftp, path):
    try:
        sftp.chdir(path)
    except FileNotFoundError:
        try:
            sftp.chdir(None)
            sftp.chdir(path)
        except FileNotFoundError:
            return 'path not found'
        # cur_path = sftp.getcwd()
        # if path[:2] == cur_path[1:cur_path[1:].find('/') + 1]:
        #     path = path[3:]
        #     path_list = cur_path.split('/')
        #     for _ in range(len(path_list) - 1):
        #         sftp.chdir('..')
        #     sftp.chdir(path)
        # else:
        #     sftp.chdir(None)
        #     sftp.chdir(path)

def run_action(ssh, action):
    stdin, stdout, stderr = ssh.exec_command(action)
    return stdout

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

def tree_items(sftp, remotedir, tree_list, search_key):
    # items_list = sftp.listdir(remotedir)
    # for item in items_list:#sftp.listdir_attr(remotedir):
    for item in sftp.listdir_attr(remotedir):
        remotepath = remotedir + '\\' + item.filename
        mode = item.st_mode
        if stat.S_ISDIR(mode):
            tree_items(sftp, remotepath, tree_list, search_key)
            if item.filename.lower().__contains__(search_key.lower()):
                tree_list.append(remotepath)
            # tree_list.append(remotepath)
            # print(remotepath)  # TEMP
        elif stat.S_ISREG(mode):
            if item.filename.lower().__contains__(search_key.lower()):
                tree_list.append(remotepath)
            # tree_list.append(remotepath)
            # print(item.filename)  # TEMP
    return tree_list


# def get_items_in_path(sftp, command_path):
#     return sftp.listdir(command_path)

# def get_items_in_path(ssh, command_path):
#     command_path = f'"{command_path}"'
#     command1 = fr'dir {command_path} /b'
#     command2 = fr'dir {command_path}'
#
#     # ssh.exec_command(fr'cd {command_path}')
#     stdin, stdout, stderr = ssh.exec_command(command1)
#     stdin2, stdout2, stderr2 = ssh.exec_command(command2)
#
#     if stdout != 'File Not Found':  # no need - if path doesn't exist it goes one dir up
#         files = stdout.readlines()
#         files_info = stdout2.readlines()
#         # items_path = files_info[3][14:files_info[3].find(r'\r\n') - 1]
#
#         files_list = list()
#         dirs_list = list()
#         for i in range(len(files)):
#             if files[i] in files_info[i + 7]:
#                 if '<DIR>' in files_info[i + 7]:
#                     end_index = files[i].find(r'\r\n')
#                     dirs_list.append(files[i][:end_index - 1])
#                 else:
#                     end_index = files[i].find(r'\r\n')
#                     files_list.append(files[i][:end_index - 1])
#         items_list = dirs_list + files_list
#         return items_list
#     else:
#         return "Path doesn't exist"