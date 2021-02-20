# testing

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



# import win32com.shell.shell as shell
# import pywintypes
# # commands = 'net start sshd'
# # shell.ShellExecuteEx(lpVerb='runas', lpFile='cmd.exe', lpParameters='/c '+commands)
#
# # command = 'Remove-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0'
# # c = 'Start-Service sshd'
# on_cmnd = """
# Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
# Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
# Start-Service sshd
# """
#
# off_cmnd = """
# Stop-Service sshd
# """
# try:
#     # print(shell.ShellExecuteEx(lpVerb='runas', lpFile='powershell.exe', lpParameters='/c '+on_cmnd))
#     print(shell.ShellExecuteEx(lpVerb='runas', lpFile='powershell.exe', lpParameters='/c '+off_cmnd))
# except pywintypes.error:
#     print('Please approve the process')



import win32con
import win32service

def check_sshd_service():
    resume = 0
    accessSCM = win32con.GENERIC_READ
    accessSrv = win32service.SC_MANAGER_ALL_ACCESS

    #Open Service Control Manager
    hscm = win32service.OpenSCManager(None, None, accessSCM)

    #Enumerate Service Control Manager DB
    typeFilter = win32service.SERVICE_WIN32
    stateFilter = win32service.SERVICE_STATE_ALL

    statuses = win32service.EnumServicesStatus(hscm, typeFilter, stateFilter)
    for (short_name, desc, status) in statuses:
        if short_name == 'sshd':
            if status == (16, 4, 1, 0, 0, 0, 0):
                return 'ON'
            elif status == (16, 1, 0, 0, 0, 0, 0):
                return 'OFF'
            print(f'short name:{short_name}, desc:{desc}, status:{status}')
    return 'NOT INSTALLED'

print(check_sshd_service())




import win32com.shell.shell as shell
import pywintypes
install_and_on_cmnd = """
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
"""

on_cmnd = """
Start-Service sshd
"""

off_cmnd = """
Stop-Service sshd
"""

service_status = check_sshd_service()

print(service_status)

if service_status == 'OFF':
    try:
        shell.ShellExecuteEx(lpVerb='runas', lpFile='powershell.exe', lpParameters='/c ' + on_cmnd)
    except pywintypes.error:
        print('Please approve the process')

elif service_status == 'ON':
    try:
        shell.ShellExecuteEx(lpVerb='runas', lpFile='powershell.exe', lpParameters='/c ' + off_cmnd)
    except pywintypes.error:
        print('Please approve the process')

elif service_status == 'NOT INSTALLED':
    try:
        shell.ShellExecuteEx(lpVerb='runas', lpFile='powershell.exe', lpParameters='/c ' + install_and_on_cmnd)
    except pywintypes.error:
        print('Please approve the process')

else:
    print('ERROR')