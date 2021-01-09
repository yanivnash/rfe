import os
import subprocess
import socket
import admin
cmd = "Get-WindowsCapability -Online | ? Name -like 'OpenSSH*'"

os.chdir("C:\\Users\\yaniv\\")
# change command
cmd = subprocess.Popen(["runas", "/noprofile", "/user:Administrator", "|", "echo", "Y", "|", "choco", "install", "dropbox"], stdin=sp.PIPE)
cmd.stdin.write('password')
cmd.communicate()


# if not admin.isUserAdmin():
#     admin.runAsAdmin()

# print(socket.gethostname())


# # answr = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
# # answr = subprocess.Popen("powershell.exe [Get-WindowsCapability -Online | ? Name -like 'OpenSSH*']")
# answr = subprocess.check_output("powershell.exe -ExecutionPolicy Unrestricted" + "Get-WindowsCapability -Online | ? Name -like 'OpenSSH*'", stderr=subprocess.STDOUT, shell=True)
# print(answr.stdout)

# if 'State : NotPresent' in answr:
#     print('not installed')
# else:
#     print('installed')