import subprocess
import manageSSH
import paramiko

# temp = 'C:\Users\yaniv\Desktop\Remote File Explorer - old\My Presentation.pptx'

# subprocess.run(r"C:\Users\yaniv\Desktop\Remote File Explorer - old\My Presentation.pptx", shell=True, universal_newlines=True)
# subprocess.run(r'Stop-Service -Name "OpenSSH SSH Server"', shell=True, universal_newlines=True)

ssh = manageSSH.connect_to_ssh('192.168.1.20', 'yaniv', 'Yanivn911911')
sftp = ssh.open_sftp()

# from stat import S_ISDIR, S_ISREG
#
# def tree_items(sftp, remotedir):
#     tree_list = list()
#     for item in sftp.listdir_attr(remotedir):
#         remotepath = remotedir + '\\' + item.filename
#         mode = item.st_mode
#         if S_ISDIR(mode):
#             tree_items(sftp, remotepath)
#             tree_list.append(remotepath)
#             print(remotepath)
#         elif S_ISREG(mode):
#             tree_list.append(remotepath)
#             print(remotepath)
#     return tree_list
#
# print(tree_items(sftp, r"C:\Users\yaniv\Desktop\Remote File Explorer - old"))


# import warnings
# warnings.filterwarnings("ignore")
# print(a)


manageSSH.chdir(sftp, r"C:\Users\yaniv\Desktop\Remote File Explorer")
sftp.mkdir(r"testing")


# warnings.filterwarnings("ignore")
# warnings.warn("NameError")


# print(sftp.listdir_attr(r"C:\Users\yaniv\Desktop\Remote File Explorer - old"))
# print(sftp.walktree(r"C:\Users\yaniv\Desktop\Remote File Explorer - old"))

# stdin, stdout, stderr = ssh.exec_command(r"C:\Users\yaniv\Desktop\Remote File Explorer - old\pic.png")
#
# print(stdin)
# print(stdout)
# print(stderr)

# chan = ssh.invoke_shell()
# chan.send(r"C:\Users\yaniv\Desktop\Remote File Explorer - old\My Logo.png")