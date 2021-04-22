# from tkinter import *
# from tkinter import ttk
# import time
#
# root = Tk()
# root.geometry('500x500')
#
# def start():
#     for x in range(20):
#         p_bar['value'] += 1
#         root.update_idletasks()
#         time.sleep(0.1)
#     root.update_idletasks()
#     time.sleep(2)
#     for x in range(200):
#         p_bar['value'] += 0.1
#         root.update_idletasks()
#         time.sleep(0.01)
#
#
# p_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate')
# p_bar.pack(pady=20)
#
# bttn = Button(root, text='Start', command=start)
# bttn.pack(pady=20)
#
# root.mainloop()



import psutil
#
# Python Script to Check if...
# Windows Service is found|installed,stopped|running without pywin32
# Found at https://stackoverflow.com/questions/33843024
# Update to work on python 3.x
#


def getService(name):
    service = None
    try:
        service = psutil.win_service_get(name)
        service = service.as_dict()
    except Exception:
        pass
        # print(str(ex))
    return service

service = getService('sshd')
# print(service)

if service:
    # print("service found")
    if service and service['status'] == 'running':
        print('ON')
        # print("service is running")
    else:
        print('OFF')
        # print("service is not running")
else:
    print('NOT INSTALLED')
    # print("service not found")



############################ old
# def old():
#     resume = 0
#     accessSCM = win32con.GENERIC_READ
#     accessSrv = win32service.SC_MANAGER_ALL_ACCESS
#
#     # Open Service Control Manager
#     hscm = win32service.OpenSCManager(None, None, accessSCM)
#
#     # Enumerate Service Control Manager DB
#     typeFilter = win32service.SERVICE_WIN32
#     stateFilter = win32service.SERVICE_STATE_ALL
#
#     statuses = win32service.EnumServicesStatus(hscm, typeFilter, stateFilter)
#     for (short_name, desc, status) in statuses:
#         if short_name == 'sshd':
#             print(f'short name:{short_name}, desc:{desc}, status:{status}')
#             if status == (16, 4, 1, 0, 0, 0, 0):
#                 return 'ON'
#             elif status == (16, 1, 0, 0, 0, 0, 0):
#                 return 'OFF'
#             # print(f'short name:{short_name}, desc:{desc}, status:{status}')
#     return 'NOT INSTALLED'