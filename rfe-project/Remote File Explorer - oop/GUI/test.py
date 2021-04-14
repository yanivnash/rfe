# import manageSSH
# host = "192.168.1.20"
# username = 'yaniv'
# password = input('Enter Password: ')
# ssh = manageSSH.connect_to_ssh(host, username, password)
# sftp = ssh.open_sftp()
#
# ROOT_PROJ_DIR = r'C:\git\rfe\rfe-project\Remote File Explorer - oop\GUI'
#
# temp = r'C:\Users\yaniv\Desktop\CoronaCertificate - 210041646.pdf'
# # f = sftp.open(r'C:\git\rfe\rfe-project\Remote File Explorer - oop\GUI\openfile.bat', 'w')
# # # f.write('test')
# # f.write(f'"{temp}"')
# #
# # # manageSSH.run_action(ssh, f'"{ROOT_PROJ_DIR}\openfile.bat"')
# #
# # stdin, stdout, stderr = ssh.exec_command(f'"{ROOT_PROJ_DIR}\openfile.bat"')
#
# open_file_path = ROOT_PROJ_DIR + r'\openfile.bat'
# print([open_file_path])
# sftp2 = ssh.open_sftp()
# f = sftp2.open(open_file_path, 'w')
# # f.write(f'"{temp}"')
# f.write('test')
#
# manageSSH.run_action(ssh, f'"{ROOT_PROJ_DIR}\openfile.bat"')
#
# # # stdin, stdout, stderr = ssh.exec_command(r'powershell -InputFormat none -OutputFormat Text start "C:\Users\yaniv\Desktop\All My Sons Project.docx"')
# # # stdin, stdout, stderr = ssh.exec_command(r'powershell -InputFormat none -OutputFormat Text ipconfig')
# # stdin, stdout, stderr = ssh.exec_command(r'"C:\Users\yaniv\Desktop\All My Sons Project.docx"')
# #
# #
# print(f'stdin: {stdin}')
# print(f'stdout: {stdout.read()}')
# print(f'stderror: {stderr.read()}')




import os
import socket

# SELF_IP = socket.gethostbyname(socket.gethostname())
#
# ipconfig = os.popen('ipconfig').read()
# ipconfig = ipconfig[ipconfig.find(SELF_IP) + len(SELF_IP):ipconfig.find('Default Gateway')]
# if 'Subnet Mask' in ipconfig:
#     # print('yes')  # TEMP
#     subnet_mask = ipconfig[ipconfig.find(': ') + 2:].replace('\n', '').replace(' ', '')
#     print(subnet_mask)
#     # print(len(sub_mask))
#     # print(ipcon_detail)
#
#     count = subnet_mask.count('255')
#     print(count)
#     masked_ip = SELF_IP
#     for _ in range(4 - count):
#         masked_ip = masked_ip[:masked_ip.rfind('.')]
#     print(masked_ip)
#
#     arp = os.popen('arp -a').read()
#     arp = arp[arp.find(f'Interface: {SELF_IP}'):]
#     while(arp.count('Interface:') > 1):
#         arp = arp[:arp.rfind('Interface:')]
#
#     arp = arp.split()
#     network_ips = list()
#     for item in arp:
#         if item.startswith(masked_ip):
#             network_ips.append(item)
#
#     # print(arp)
#     print(network_ips)
#
# else:
#     print('error')




# def get_network_ip_list(SELF_IP):
#     ipconfig = os.popen('ipconfig').read()
#     ipconfig = ipconfig[ipconfig.find(SELF_IP) + len(SELF_IP):ipconfig.find('Default Gateway')]
#     if 'Subnet Mask' in ipconfig:
#         subnet_mask = ipconfig[ipconfig.find(': ') + 2:].replace('\n', '').replace(' ', '')
#
#         count = subnet_mask.count('255')
#         masked_ip = SELF_IP
#         for _ in range(4 - count):
#             masked_ip = masked_ip[:masked_ip.rfind('.')]
#
#         arp = os.popen('arp -a').read()
#         arp = arp[arp.find(f'Interface: {SELF_IP}'):]
#         while arp.count('Interface:') > 1:
#             arp = arp[:arp.rfind('Interface:')]
#
#         arp = arp.split()
#         # network_ips_dict = dict()
#         # for ip in arp:
#         #     if ip.startswith(masked_ip):
#         #         network_ips_dict[ip] = socket.gethostbyaddr(ip)[0]
#         # return network_ips_dict
#         network_ips = list()
#         for ip in arp:
#             if ip.startswith(masked_ip):
#                 network_ips.append(ip)
#         return network_ips
#     else:
#         return []




# import requests
# EXTERNAL_IP = requests.get('http://ip.42.pl/raw').text