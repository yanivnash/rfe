import manageSSH
host = "192.168.1.20"
username = 'yaniv'
password = 'Yanivn911911'  # DELETE
ssh = manageSSH.connect_to_ssh(host, username, password)
sftp = ssh.open_sftp()

ROOT_PROJ_DIR = r'C:\git\rfe\rfe-project\Remote File Explorer - oop\GUI'

temp = r'C:\Users\yaniv\Desktop\CoronaCertificate - 210041646.pdf'
# f = sftp.open(r'C:\git\rfe\rfe-project\Remote File Explorer - oop\GUI\openfile.bat', 'w')
# # f.write('test')
# f.write(f'"{temp}"')
#
# # manageSSH.run_action(ssh, f'"{ROOT_PROJ_DIR}\openfile.bat"')
#
# stdin, stdout, stderr = ssh.exec_command(f'"{ROOT_PROJ_DIR}\openfile.bat"')

open_file_path = ROOT_PROJ_DIR + r'\openfile.bat'
print([open_file_path])
sftp2 = ssh.open_sftp()
f = sftp2.open(open_file_path, 'w')
# f.write(f'"{temp}"')
f.write('test')

manageSSH.run_action(ssh, f'"{ROOT_PROJ_DIR}\openfile.bat"')

# # stdin, stdout, stderr = ssh.exec_command(r'powershell -InputFormat none -OutputFormat Text start "C:\Users\yaniv\Desktop\All My Sons Project.docx"')
# # stdin, stdout, stderr = ssh.exec_command(r'powershell -InputFormat none -OutputFormat Text ipconfig')
# stdin, stdout, stderr = ssh.exec_command(r'"C:\Users\yaniv\Desktop\All My Sons Project.docx"')
#
#
print(f'stdin: {stdin}')
print(f'stdout: {stdout.read()}')
print(f'stderror: {stderr.read()}')