# import ctypes, sys, os
# command = 'net start sshd'
# def is_admin():
#     try:
#         return ctypes.windll.shell32.IsUserAnAdmin()
#     except:
#         return False
#
# if is_admin():
#     os.system(command)
#     # Code of your program here
# else:
#     # Re-run the program with admin rights
#     ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
#     os.system(command)



import win32com.shell.shell as shell
import pywintypes
# commands = 'net start sshd'
# shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)

# command = 'Remove-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0'
# c = 'Start-Service sshd'
on_cmnd = """
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
Start-Service sshd
"""

off_cmnd = """
Stop-Service sshd
"""
try:
    # print(shell.ShellExecuteEx(lpVerb='runas', lpFile='powershell.exe', lpParameters='/c '+on_cmnd))
    print(shell.ShellExecuteEx(lpVerb='runas', lpFile='powershell.exe', lpParameters='/c '+off_cmnd))
except pywintypes.error:
    print('Please approve the process')