import subprocess
import manageSSH
import paramiko

# temp = 'C:\Users\yaniv\Desktop\Remote File Explorer\My Presentation.pptx'

# subprocess.run(r"C:\Users\yaniv\Desktop\Remote File Explorer\My Presentation.pptx", shell=True, universal_newlines=True)
# subprocess.run(r'Stop-Service -Name "OpenSSH SSH Server"', shell=True, universal_newlines=True)

ssh = manageSSH.connect_to_ssh('192.168.1.20', 'yaniv', 'Yanivn911911')
sftp = ssh.open_sftp()

answr = str(manageSSH.run_action(ssh, 'wmic logicaldisk get caption').read())
drives_list = answr[answr.find('Caption') + 9:answr.rfind(r'       \r\r\n\r\r\n')].split(r'       \r\r\n')
drives_list[0] = drives_list[0].replace(r'\r\r\n', '')
for i in range(len(drives_list)):
    drives_list[i] += '\\'
print(drives_list)

import os
print(os.getenv("SystemDrive"))
# stdin, stdout, stderr = ssh.exec_command(r"C:\Users\yaniv\Desktop\Remote File Explorer\pic.png")
#
# print(stdin)
# print(stdout)
# print(stderr)

# chan = ssh.invoke_shell()
# chan.send(r"C:\Users\yaniv\Desktop\Remote File Explorer\My Logo.png")