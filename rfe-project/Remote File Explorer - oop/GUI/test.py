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




# from tkinter import *
# import main_window2
# import manageSERVER
# from tkinter import messagebox
#
# label_bg_color = '#e9eed6'
# buttons_bg_color = '#d9dcc7'
# show_icon = None
# hide_icon = None
# screen_width = main_window2.screen_width
# screen_height = main_window2.screen_height
# email = 'yanivnash1@gmail.com'
#
#
# def create_popup_window(title, label_text, msg_box_text, approve_text):
#     popup_width = main_window2.calc_width(400)
#     popup_height = main_window2.calc_height(200)
#     popup_x = int((screen_width - popup_width) / 2)
#     popup_y = int((screen_height - popup_height) / 2)
#
#
#     def submit():
#         pass_error_title.place_forget()
#         password = enter_password.get()
#         if password == '':
#             if password == '':
#                 pass_error_title.configure(text='Please enter your password')
#                 pass_error_title.place(x=main_window2.calc_width(0), y=main_window2.calc_height(120), width=main_window2.calc_width(400))
#         elif not manageSERVER.check_if_email_exists(email):  # check if email doesn't exist in the DB
#             pass_error_title.configure(text="This email address doesn't have an account")
#             pass_error_title.place(x=main_window2.calc_width(0), y=main_window2.calc_height(120), width=main_window2.calc_width(400))
#         elif not manageSERVER.login(email, password, 0):  # check if password doesn't match the email
#             pass_error_title.configure(text='Password is incorrect, Try again')
#             pass_error_title.place(x=main_window2.calc_width(0), y=main_window2.calc_height(120), width=main_window2.calc_width(400))
#         else:  # email exists and the password matches
#             pass_error_title.place_forget()
#             msg_box = messagebox.askquestion(title=title,
#                                                     message=f'{msg_box_text}\nThis action is not reversible!')
#             print(msg_box)
#             if msg_box == 'yes':
#                 if title == 'Reset saved IP list in your account':
#                     if manageSERVER.reset_ip_dict(email, password):
#                         popup.destroy()
#                         messagebox.showinfo(title=title, message=approve_text)
#                         return True
#                     else:
#                         return False
#
#                 elif title == 'Permanently delete your account':
#                     if manageSERVER.delete_account(email, password):
#                         popup.destroy()
#                         messagebox.showinfo(title=title, message=approve_text)
#                         return True
#                     else:
#                         return False
#             elif msg_box == 'no':
#                 popup.destroy()
#                 return None
#
#     def show_hide_pass():
#         if enter_password.cget('show') == '':
#             enter_password.configure(show='•')
#             show_hide_button.configure(image=show_icon)
#         else:
#             enter_password.configure(show='')
#             show_hide_button.configure(image=hide_icon)
#
#     popup = Toplevel(bg=label_bg_color)
#     popup.geometry(f'{popup_width}x{popup_height}+{popup_x}+{popup_y}')
#     popup.iconbitmap('icon.ico')
#     popup.resizable(False, False)
#     popup.title(title)
#     def enter_key(event):
#         submit()
#     popup.bind('<Return>', enter_key)
#
#     pass_error_title = Label(popup, text='Please enter your password',
#                              font=('Eras Bold ITC', main_window2.calc_width(10)), fg='red', bg=label_bg_color)
#     pass_error_title.place(x=main_window2.calc_width(0), y=main_window2.calc_height(120),
#                            width=main_window2.calc_width(400))
#     pass_error_title.place_forget()
#
#
#     Label(popup, text=label_text, wraplength=popup_width, bg=label_bg_color, font=('Eras Bold ITC', main_window2.calc_width(12))).place(x=main_window2.calc_width(0), y=main_window2.calc_height(5), width=main_window2.calc_width(400))
#     Label(popup, text=f'{email}', wraplength=popup_width, bg=label_bg_color, font=('Eras Bold ITC', main_window2.calc_width(15))).place(x=main_window2.calc_width(0), y=main_window2.calc_height(50), width=main_window2.calc_width(400))
#     enter_password = Entry(popup, font=('Eras Bold ITC', main_window2.calc_width(15)), bg='white', justify='center', show='•')
#     enter_password.place(x=main_window2.calc_width(32), y=main_window2.calc_height(85), width=main_window2.calc_width(300), height=main_window2.calc_height(35))
#     show_hide_button = Button(popup, image=show_icon, cursor='hand2', bg=buttons_bg_color, command=show_hide_pass)
#     show_hide_button.place(x=main_window2.calc_width(333), y=main_window2.calc_height(85), width=main_window2.calc_width(35), height=main_window2.calc_height(35))
#
#     login_button = Button(popup, text='Login', cursor='hand2',
#                           font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20', bg=buttons_bg_color,
#                           command=submit)
#     login_button.place(x=main_window2.calc_width(150), y=main_window2.calc_height(145),
#                        width=main_window2.calc_width(100), height=main_window2.calc_height(32))
#     enter_password.focus()
#     popup.mainloop()
#
# print(create_popup_window('Reset saved IP list in your account', "Enter your account's password to delete all the saved IPs in your account:", f'Are you sure you want to delete all the IPs saved to your account: {email}?', 'IP list reset successfully'))




from tkinter import filedialog
file = 'testing.txt'
file_type = '.txt'
file_name = 'testing'
save_file_path = filedialog.asksaveasfilename(defaultextension=file_type, title='Choose where to save the file', initialfile=file_name, filetypes=((file_type, file_type), ))
print(save_file_path)

open_file_path = filedialog.askopenfilename(title='Choose a file to copy', filetypes=(('All Files', '*.*'), ))
print(open_file_path)