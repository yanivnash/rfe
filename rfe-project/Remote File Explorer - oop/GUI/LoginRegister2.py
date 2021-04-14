__author__ = 'Yaniv Nash'

import threading
from tkinter import *
from tkinter import messagebox, ttk
from tkinter import simpledialog  # opens the popup to add a new ip
import imageio
import psutil
import wx
import re
from PIL import ImageTk, Image
import os
import socket
import win32con
import win32service
import win32com.shell.shell as shell
import pywintypes

# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

import manageSERVER
import manageSSH
from time import sleep
import main_window2

ROOT_PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
SELF_NAME = os.getlogin()
SELF_IP = socket.gethostbyname(socket.gethostname())


# app = wx.App(False)
# screen_width, screen_height = wx.GetDisplaySize()
# screen_width = 1000#1280  # temp
# screen_height = 700#720  # temp
#
# if screen_width / screen_height != (1920 / 1080):
#     screen_height = screen_width / (1920 / 1080)
#
# if screen_width >= 1070 and screen_height >= 700:
#     screen_width = 1920
#     screen_height = 1080
#
# app_width = int(screen_width / 1.794)
# app_height = int(screen_height / 1.542)
# print(screen_width, screen_height, app_width, app_height)  # temp

screen_width = main_window2.screen_width
screen_height = main_window2.screen_height

label_bg_color = '#e9eed6'
buttons_bg_color = '#d9dcc7'
# start_video_name = f'{ROOT_PROJ_DIR}\start-animation.mp4'
start_video_name = 'start-animation.mp4'
# mid_video_name = f'{ROOT_PROJ_DIR}\mid-animation.mp4'
mid_video_name = 'mid-animation.mp4'
# end_video_name = f'{ROOT_PROJ_DIR}\end-animation.mp4'
end_video_name = 'end-animation.mp4'


# def calc_width(size):
#     return int(app_width / (1070 / size))
# def calc_height(size):
#     return int(app_height / (700 / size))


def email_regex(email):
    regex = r"""^[a-zA-Z]+(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    if re.match(regex, email):
        return True
    else:
        return False

def acc_signout():
    discon_msg_box = messagebox.askquestion(title='Sign Out', message='Are you sure you want to sign out of your account?')
    if discon_msg_box == 'yes':
        root.destroy()
        main_window2.main()


def choose_mode(choose_frame, control_pic, be_controlled_pic):#, old_frame):
    global mode, root
    global app_width, app_height
    mode = None
    def return_button(event):
        pass
    root.bind('<Return>', return_button)
    def control_bttn():
        global mode
        mode = 'control'
        choose_frame.quit()  # works
        # login_to_ssh_client(choose_frame, ip_dict)  # doesnt work
    def be_controlled_bttn():
        global mode
        mode = 'be_controlled'
        choose_frame.quit()  # works
        # set_be_controlled(choose_frame)  # doesnt work
    # main_title = Label(choose_frame, text='Remote File Explorer', font=('Eras Bold ITC', 35, 'bold'), fg='gray20', bg=label_bg_color)
    main_title = Label(choose_frame, text='Choose an action for this PC:', font=('Eras Bold ITC', main_window2.calc_width(35), 'bold'), fg='gray20', bg=label_bg_color)
    main_title.place(x=main_window2.calc_width(180), y=main_window2.calc_height(25))  # (x=270, y=25)
    frame = Frame(choose_frame, bg='white')
    frame.place(x=main_window2.calc_width(231), y=main_window2.calc_height(133), width=main_window2.calc_width(610), height=main_window2.calc_height(392))  # (x=231, y=133, width=610, height=392)
    # choose_label = Label(frame, text='Choose an action for this PC:', font=('Eras Bold ITC', 25, 'bold underline'), fg='gray20', bg='white')
    # choose_label = Label(frame, text='Choose an action for this PC:', font=('Eras Bold ITC', main_window.calc_width(25), 'bold underline'), fg='gray20', bg='white')
    # choose_label.place(x=main_window.calc_width(55), y=main_window.calc_height(25))  # (x=55, y=25)
    control_button = Button(frame, cursor='hand2', command=control_bttn, image=control_pic, bd=0, bg='white')
    control_button.place(x=main_window2.calc_width(70), y=main_window2.calc_height(142))  # (x=70, y=142)
    # control_label = Label(frame, text='CONTROL', font=('Eras Bold ITC', 20, 'bold'), fg='gray20', bg='white')
    control_label = Label(frame, text='CONTROL', font=('Eras Bold ITC', main_window2.calc_width(20), 'bold'), fg='gray20', bg='white')
    control_label.place(x=main_window2.calc_width(75), y=main_window2.calc_height(100))  # (x=75, y=100)
    be_controlled_button = Button(frame, cursor='hand2', command=be_controlled_bttn, image=be_controlled_pic, bd=0, bg='white')
    be_controlled_button.place(x=main_window2.calc_width(350), y=main_window2.calc_height(140))  # (x=360, y=140)
    # control_label = Label(frame, text='BE CONTROLLED', font=('Eras Bold ITC', 20, 'bold'), fg='gray20', bg='white')
    control_label = Label(frame, text='BE CONTROLLED', font=('Eras Bold ITC', main_window2.calc_height(20), 'bold'), fg='gray20', bg='white')
    control_label.place(x=main_window2.calc_width(320), y=main_window2.calc_height(100))  # (x=320, y=100)

    choose_frame.mainloop()
    return mode


def get_network_ip_list():
    ipconfig = os.popen('ipconfig').read()
    # ipconfig = ipconfig[ipconfig.find(SELF_IP) + len(SELF_IP):ipconfig.find('Default Gateway')]
    self_ip = ipconfig[ipconfig.find('IPv4 Address'):ipconfig.find('Subnet Mask')]
    subnet_mask = ipconfig[ipconfig.find('Subnet Mask'):ipconfig.find('Default Gateway')]
    if 'Subnet Mask' in subnet_mask and 'IPv4 Address' in self_ip:
        self_ip = self_ip[self_ip.find(': ') + 2:].replace('\n', '').replace(' ', '')
        # subnet_mask = ipconfig[ipconfig.find(': ') + 2:].replace('\n', '').replace(' ', '')

        count = subnet_mask.count('255')
        masked_ip = self_ip
        for _ in range(4 - count):
            masked_ip = masked_ip[:masked_ip.rfind('.')]

        arp = os.popen('arp -a').read()
        arp = arp[arp.find(f'Interface: {self_ip}'):]
        while arp.count('Interface:') > 1:
            arp = arp[:arp.rfind('Interface:')]

        arp = arp.split()
        network_ips = list()
        for ip in arp:
            if ip.startswith(masked_ip):
                network_ips.append(ip)
        return network_ips
    else:
        return []


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
#         network_ips = list()
#         for ip in arp:
#             if ip.startswith(masked_ip):
#                 network_ips.append(ip)
#         return network_ips
#     else:
#         return []


def login_to_ssh_client(ip_frame, ip_dict):
    global mode, root, count, ssh, sftp, ip_butns_dict, scrollable_frame, email, username, canvas, scrollbar
    global app_width, app_height

    def close_window():
        global ssh, sftp, username
        close_msg_box = messagebox.askquestion(title='Close', message='Are you sure you want to close the window?')
        if close_msg_box == 'yes':
            ssh = None
            sftp = None
            username = None
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", close_window)

    ip_butns_dict = dict()

    main_title = Label(ip_frame, text='Choose a computer to connect to:', font=('Eras Bold ITC', main_window2.calc_width(35), 'bold'), fg='gray20', bg=label_bg_color)
    main_title.place(x=main_window2.calc_width(120), y=main_window2.calc_height(25))

    frame = Frame(ip_frame, bg='white')
    frame.place(x=main_window2.calc_width(231), y=main_window2.calc_height(133), width=main_window2.calc_width(610), height=main_window2.calc_height(392))

    # canvas = Canvas(frame)
    # scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    # # # scrollable_frame = Frame(canvas)

    def mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def ip_butn_click(event):
        global ssh, sftp, check_var, username

        key_list = list(ip_butns_dict.keys())
        val_list = list(ip_butns_dict.values())
        bttn_name = key_list[val_list.index(event.widget)]
        if bttn_name.__contains__('bttn'):
            host = bttn_name[:bttn_name.rfind('-bttn')]
            username = simpledialog.askstring('Enter Username', f'Enter the Username of {host}:')
            if username != None:
                check_var = IntVar(value=1)
                try_connect(host, username)
        else:
            host = bttn_name[:bttn_name.index('-')]
            username = bttn_name[bttn_name.index('-') + 1:]
            check_var = IntVar(value=0)
            try_connect(host, username)

        # event.widget.bind('<ButtonRelease-1>', True)  ###########

    def try_connect(host, username):
        global ssh, sftp
        ssh = None
        sftp = None
        password = simpledialog.askstring('Enter password', f'Enter the password to {host}:', show='•')
        # con_ask = messagebox.askquestion(title='Connect', message=f'You are about to connect to {host}\nWould you like to connect')
        # if con_ask == 'yes':
        if password == None:# or password == '':
            pass
        # elif password == '':
        #     password = simpledialog.askstring('Enter password', f'Enter the password to {host}:')
        else:
            ssh = manageSSH.connect_to_ssh(host, username, password)
            if ssh == "wrong password/username":
                messagebox.showerror(title="Couldn't connect", message=f"Couldn't connect to {host}\nPlease make sure the password and the username are correct and try again")
            elif ssh == "no connection":
                messagebox.showerror(title="Couldn't connect", message=f"Couldn't connect to {host}\nPlease make sure that the computer is connected to the internet, has Remote File Explorer open in the 'Be Controlled' screen and try again")
            elif ssh == "timeout":
                messagebox.showerror(title="Couldn't connect", message=f"Couldn't connect to {host}\nPlease make sure the password is correct, that the computer is connected to the internet, has Remote File Explorer open in the 'Be Controlled' screen and try again")
            else:
                sftp = ssh.open_sftp()
                if check_var.get() == 1:
                    manageSERVER.update_pc_in_account(email, (host, username))
                ip_frame.quit()

    # def create_scroll_frame():
    #     global scrollable_frame, ip_butns_dict
    #     scrollable_frame = Frame(canvas)
    #     scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    #     scrollable_frame.bind_all("<MouseWheel>", mouse_wheel)
    #
    #     back_pic = ImageTk.PhotoImage(Image.open('back.png').resize((main_window.calc_width(57), main_window.calc_height(44)), Image.ANTIALIAS))
    #     show_enter_ip_btn = Button(scrollable_frame, command=open_ip_list, image=back_pic, cursor='hand2', bg=buttons_bg_color)
    #     show_enter_ip_btn.place(x=main_window.calc_width(10), y=main_window.calc_height(10))
    #
    #     for key, value in ip_dict.items():
    #         ip_butns_dict[key] = Button(scrollable_frame, text=f'{value} - {key}', cursor='hand2',
    #                                             font=('Eras Bold ITC', main_window.calc_width(12)),
    #                                             anchor=CENTER, fg='gray20', bg=buttons_bg_color,
    #                                             activebackground='yellow')
    #         ip_butns_dict[key].pack(anchor=CENTER, pady=4)
    #         ip_butns_dict[key].bind("<Button-1>", ip_butn_click)
    #
    #     canvas.create_window((0, 0), window=scrollable_frame, anchor=CENTER, width=main_window.calc_width(610), height=main_window.calc_height(392))

    # create_scroll_frame()



    # for key, value in ip_dict.items():
    #     ip_butns_dict[key] = Button(scrollable_frame, text=f'{value} - {key}', cursor='hand2', font=('Eras Bold ITC', main_window.calc_width(12)), anchor=CENTER, fg='gray20', bg=buttons_bg_color, activebackground='yellow')
    #     ip_butns_dict[key].pack(anchor=CENTER, pady=5)
    #     ip_butns_dict[key].bind("<Button-1>", ip_butn_click)

    # scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    # scrollable_frame.bind_all("<MouseWheel>", mouse_wheel)
    #
    # canvas.create_window((0, 0), window=scrollable_frame, anchor=CENTER, width=main_window.calc_width(610), height=main_window.calc_height(392))


    # def go_back():
    #     acc_signout()
    #     # main(root, app_width, app_height, account, ssh_service_menu, email)  # LAST
    #
    #     # can work
    #     # print('back')
    #     # frame.destroy()
    #     # can work
    #
    #     # return choose_mode_window(email)  # doesnt work
    #
    #     # # works
    #     # manageSSH.disconnect_ssh(ssh)
    #     # root.destroy()
    #     # main_window2.main()
    #     # # works

    back_pic = ImageTk.PhotoImage(Image.open('back.png').resize((main_window2.calc_width(57), main_window2.calc_height(44)), Image.ANTIALIAS))
    signout_pic = ImageTk.PhotoImage(Image.open('signout.png').resize((main_window2.calc_width(57), main_window2.calc_height(51)), Image.ANTIALIAS))
    signout_bttn = Button(ip_frame, image=signout_pic, cursor='hand2',# text='Sign Out', compound=TOP,
                       font=('Eras Bold ITC', main_window2.calc_width(10)), fg='gray20', bg=buttons_bg_color,
                       command=acc_signout)#go_back)
    signout_bttn.place(x=main_window2.calc_width(10), y=main_window2.calc_height(10))

    def create_enter_frame():
        global check_var, username

        main_title.configure(text="Enter a computer's info to connect to:")
        main_title.place(x=main_window2.calc_width(85), y=main_window2.calc_height(25))

        def return_button(event):
            connect_button.invoke()
        root.bind('<Return>', return_button)

        def check_ip():
            global username
            host = enter_ip.get()
            username = enter_username.get()
            ip_error_title.place_forget()
            username_error_title.place_forget()
            if host == '' or username == '':
                if host == '':
                    ip_error_title.configure(text='Please enter an ip')
                    ip_error_title.place(x=main_window2.calc_width(50), y=main_window2.calc_height(110), width=main_window2.calc_width(500))
                if username == '':
                    username_error_title.configure(text='Please enter a username')
                    username_error_title.place(x=main_window2.calc_width(50), y=main_window2.calc_height(215), width=main_window2.calc_width(500))
            else:
                print(check_var.get())
                try_connect(host, username)

        enter_frame = Frame(frame, bg='white')
        enter_frame.place(x=main_window2.calc_width(0), y=main_window2.calc_height(0), width=main_window2.calc_width(610), height=main_window2.calc_height(392))

        def close_enter_frame():
            main_title.configure(text='Choose a computer to connect to:')
            main_title.place(x=main_window2.calc_width(120), y=main_window2.calc_height(25))
            def no_action(event):
                pass
            root.bind('<Return>', no_action)
            enter_frame.destroy()

        signout_bttn = Button(enter_frame, command=close_enter_frame, cursor='hand2', bg=buttons_bg_color, image=back_pic)
        signout_bttn.place(x=main_window2.calc_width(10), y=main_window2.calc_height(10))

        ip_error_title = Label(enter_frame, text='Please enter an ip', font=('Eras Bold ITC', main_window2.calc_width(10)), fg='red', bg='white')
        ip_error_title.place(x=main_window2.calc_width(50), y=main_window2.calc_height(110), width=main_window2.calc_width(500))
        username_error_title = Label(enter_frame, text='Please enter a username', font=('Eras Bold ITC', main_window2.calc_width(10)), fg='red', bg='white')
        username_error_title.place(x=main_window2.calc_width(50), y=main_window2.calc_height(215), width=main_window2.calc_width(500))
        ip_error_title.place_forget()
        username_error_title.place_forget()

        enter_ip_title = Label(enter_frame, text='IP:', font=('Eras Bold ITC', main_window2.calc_width(20), 'bold'), fg='gray20', bg='white').place(x=main_window2.calc_width(285), y=main_window2.calc_height(35))
        enter_ip = Entry(enter_frame, font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20', bg='white', justify='center')
        enter_ip.place(x=main_window2.calc_width(55), y=main_window2.calc_height(75), width=main_window2.calc_width(500), height=main_window2.calc_height(35))

        enter_username_title = Label(enter_frame, text='Username:', font=('Eras Bold ITC', main_window2.calc_width(20), 'bold'), fg='gray20', bg='white').place(x=main_window2.calc_width(225), y=main_window2.calc_height(140))  # (x=225, y=140)
        enter_username = Entry(enter_frame, font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20', bg='white', justify='center')
        enter_username.place(x=main_window2.calc_width(55), y=main_window2.calc_height(180), width=main_window2.calc_width(500), height=main_window2.calc_height(35))

        check_var = IntVar(value=1)
        save_to_acc = Checkbutton(enter_frame, cursor='hand2', text="Save this PC's info to your account for future connections", fg='gray20', bg=buttons_bg_color, font=('Eras Bold ITC', main_window2.calc_width(10)), onvalue=1, offvalue=0, variable=check_var)
        save_to_acc.place(x=main_window2.calc_width(105), y=main_window2.calc_height(245))

        connect_button = Button(enter_frame, text='Connect', cursor='hand2', font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20', bg=buttons_bg_color, command=check_ip)
        connect_button.place(x=main_window2.calc_width(255), y=main_window2.calc_height(292), width=main_window2.calc_width(100), height=main_window2.calc_height(35))

        enter_ip.focus()


    def on_enter(event):
        event.widget['background'] = 'papaya whip'

    def on_leave(event):
        event.widget['background'] = buttons_bg_color


    def show_local_ip_list():
        global scrollable_frame, scrollbar, canvas
        scrollbar.destroy()
        scrollable_frame.destroy()
        local_ip_bttn.configure(relief=SUNKEN)
        account_ip_bttn.configure(relief=RAISED)
        def no_action(event):
            pass
        scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg='white')
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        scrollable_frame.bind_all("<MouseWheel>", no_action)

        Label(scrollable_frame, height=main_window2.calc_height(2), bg='white').pack()

        local_ip_list = get_network_ip_list()
        if local_ip_list == []:
            Label(scrollable_frame, text='No IP Addresses Found', font=('Eras Bold ITC', main_window2.calc_width(20)), bg=buttons_bg_color).place(x=main_window2.calc_width(155), y=main_window2.calc_height(170))
        else:
            for local_ip in local_ip_list:
                ip_butns_dict[f'{local_ip}-bttn'] = Button(scrollable_frame, bd=0, text=local_ip, cursor='hand2',
                                                         font=('Eras Bold ITC', main_window2.calc_width(12)), anchor=CENTER,
                                                         fg='gray20', bg=buttons_bg_color)
                ip_butns_dict[f'{local_ip}-bttn'].pack(anchor=CENTER, pady=4)
                ip_butns_dict[f'{local_ip}-bttn'].bind("<Button-1>", ip_butn_click)
                ip_butns_dict[f'{local_ip}-bttn'].bind("<Enter>", on_enter)
                ip_butns_dict[f'{local_ip}-bttn'].bind("<Leave>", on_leave)

            if (num_of_temp_items - len(local_ip_list)) > 0:
                for _ in range(num_of_temp_items - len(local_ip_list)):
                    Button(scrollable_frame, bg='blue', bd=0, font=('Eras Bold ITC', main_window2.calc_width(12)),
                           state='disable').pack(anchor=CENTER, pady=4)

        if len(local_ip_list) > 8:
            canvas.create_window((0, 0), window=scrollable_frame, anchor=S,
                                 width=main_window2.calc_width(610))
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollable_frame.bind_all("<MouseWheel>", mouse_wheel)
            scrollbar.pack(side="right", fill="y")
        else:
            canvas.create_window((0, 0), window=scrollable_frame, anchor=S,
                                 width=main_window2.calc_width(610))#, height=main_window2.calc_height(392))
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
        canvas.yview_moveto('0.0')


    def show_account_ip_list():
        global scrollable_frame, scrollbar, canvas
        scrollbar.destroy()
        scrollable_frame.destroy()
        local_ip_bttn.configure(relief=RAISED)
        account_ip_bttn.configure(relief=SUNKEN)
        def no_action(event):
            pass
        scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg='white')
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        scrollable_frame.bind_all("<MouseWheel>", no_action)

        Label(scrollable_frame, height=main_window2.calc_height(2), bg='white').pack()

        if ip_dict == {}:
            Label(scrollable_frame, text='No IP Addresses Found', font=('Eras Bold ITC', main_window2.calc_width(20)), bg=buttons_bg_color).place(x=main_window2.calc_width(155), y=main_window2.calc_height(170))
        else:
            Label(scrollable_frame, wraplength=550,
                  text="*These IP addresses are only available if you're connected to the same local network as they are",
                  font=('Eras Bold ITC', main_window2.calc_width(10)), bg='white').pack()
            for key, value in ip_dict.items():
                ip_butns_dict[f'{key}-{value}'] = Button(scrollable_frame, bd=0, text=f'{value} - {key}', cursor='hand2',
                                                         font=('Eras Bold ITC', main_window2.calc_width(12)), anchor=CENTER,
                                                         fg='gray20', bg=buttons_bg_color)
                ip_butns_dict[f'{key}-{value}'].pack(anchor=CENTER, pady=4)
                ip_butns_dict[f'{key}-{value}'].bind("<Button-1>", ip_butn_click)
                ip_butns_dict[f'{key}-{value}'].bind("<Enter>", on_enter)
                ip_butns_dict[f'{key}-{value}'].bind("<Leave>", on_leave)

            print(num_of_temp_items - len(ip_dict) - 1)
            if (num_of_temp_items - len(ip_dict) - 1) > 0:
                for _ in range(num_of_temp_items - len(ip_dict) - 1):
                    Button(scrollable_frame, bg='white', bd=0, font=('Eras Bold ITC', main_window2.calc_width(12)),
                           state='disable').pack(anchor=CENTER, pady=4)

        if len(ip_dict) > 8:
            canvas.create_window((0, 0), window=scrollable_frame, anchor=S,
                                 width=main_window2.calc_width(610))
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollable_frame.bind_all("<MouseWheel>", mouse_wheel)
            scrollbar.pack(side="right", fill="y")
        else:
            canvas.create_window((0, 0), window=scrollable_frame, anchor=S,
                                 width=main_window2.calc_width(610))#, height=main_window2.calc_height(392))
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
        canvas.yview_moveto('0.0')

    num_of_temp_items = max(len(get_network_ip_list()), len(ip_dict))
    canvas = Canvas(frame, bg='white')

    enter_ip_pic = ImageTk.PhotoImage(
        Image.open('entry.png').resize((main_window2.calc_width(55), main_window2.calc_height(41)),
                                       Image.ANTIALIAS))
    show_enter_frame_btn = Button(frame, command=create_enter_frame, image=enter_ip_pic, cursor='hand2',
                                  bg=buttons_bg_color, compound=BOTTOM, text='Enter an IP',
                                  font=('Eras Bold ITC', main_window2.calc_width(10)))
    show_enter_frame_btn.place(x=main_window2.calc_width(490), y=main_window2.calc_height(60))

    local_ip_bttn = Button(frame, cursor='hand2', command=show_local_ip_list, bg=buttons_bg_color, borderwidth=3, text='Local Network IPs', font=('Eras Bold ITC', main_window2.calc_width(14)))
    local_ip_bttn.place(x=main_window2.calc_width(0), y=main_window2.calc_height(0), width=main_window2.calc_width(305), height=main_window2.calc_height(40))

    account_ip_bttn = Button(frame, cursor='hand2', command=show_account_ip_list, bg=buttons_bg_color, borderwidth=3, text='IPs saved to your account', font=('Eras Bold ITC', main_window2.calc_width(14)))
    account_ip_bttn.place(x=main_window2.calc_width(305), y=main_window2.calc_height(0), width=main_window2.calc_width(305), height=main_window2.calc_height(40))

    # canvas = Canvas(frame)
    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack()
    scrollable_frame = Frame(canvas, bg='white')

    show_local_ip_list()

    canvas.yview_moveto('0.0')

    ip_frame.mainloop()
    return ssh, sftp, username


def check_sshd_service(service_name):
    service = None
    try:
        service = psutil.win_service_get(service_name)
        service = service.as_dict()
    except Exception:
        pass

    if service:
        if service and service['status'] == 'running':
            return 'ON'
        else:
            return 'OFF'
    else:
        return 'NOT INSTALLED'

def set_be_controlled(be_controlled_frame):
    def close_window():
        sshd_status = check_sshd_service('sshd')
        if sshd_status == 'OFF' or sshd_status == 'NOT INSTALLED':
            close_msg_box = messagebox.askquestion(title='Close', message='Are you sure you want to close the window?')
            if close_msg_box == 'yes':
                root.destroy()
        elif sshd_status == 'ON':
            close_msg_box = messagebox.askquestion(title='Stop Service / Close', message='Would you like to Close the window and Stop the SSH Service?\n(Stopping the SSH service will make your computer not available for others to connect to)')
            if close_msg_box == 'yes':
                if run_power_shell('off_cmnd') == 'DONE':
                    root.destroy()
            elif close_msg_box == 'no':
                root.destroy()
    root.protocol("WM_DELETE_WINDOW", close_window)

    def recheck_sshd():
        print('refresh')
        # frame.destroy()
        set_be_controlled(be_controlled_frame)

    import time
    def run_power_shell(cmnd):
        # install_cmnd = """
        # Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0
        # """
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

        if cmnd == 'install_and_on_cmnd':
            def start():
                for x in range(200):
                    p_bar['value'] += 0.1
                    root.update_idletasks()
                    time.sleep(0.01)
                for x in range(4):
                    root.update_idletasks()
                    sshd_status = check_sshd_service('sshd')
                    print(sshd_status)
                    if sshd_status == 'ON':
                        p_bar['value'] = 100
                        recheck_sshd()
                        break
                    else:
                        time.sleep(2)
                        for x in range(200):
                            p_bar['value'] += 0.1
                            root.update_idletasks()
                            time.sleep(0.01)
                    # if sshd_status == 'NOT INSTALLED':
                    #     time.sleep(2)
                    #     for x in range(200):
                    #         p_bar['value'] += 0.1
                    #         root.update_idletasks()
                    #         time.sleep(0.01)
                    # else:
                    #     p_bar['value'] = 100
                    #     recheck_sshd()
                    #     break

            # loading_label = Label(frame, text='Installing SSH Service...', font=('Eras Bold ITC', main_window2.calc_width(20)), bg='white')
            try:
                shell.ShellExecuteEx(lpVerb='runas', lpFile='powershell.exe', lpParameters='/c ' + install_and_on_cmnd)
                loading_label = Label(frame, text='Installing SSH Service...', font=('Eras Bold ITC', main_window2.calc_width(20)), bg='white')
                loading_label.place(x=0, y=0, width=610, height=392)
                p_bar = ttk.Progressbar(loading_label, orient=HORIZONTAL, length=400, mode='determinate')
                p_bar.pack(pady=100)
                root.update_idletasks()
                # loading_label.after(1000, start)
                start()

                sshd_status = check_sshd_service('sshd')
                if sshd_status == 'ON':
                    root.update_idletasks()
                    time.sleep(1)
                    recheck_sshd()
                else:
                    print('2')
                    # loading_label = Label(frame, text='Installing service...')
                    loading_label.place(x=0, y=0, width=610, height=392)
                    # p_bar = ttk.Progressbar(loading_label, orient=HORIZONTAL, length=400, mode='determinate')
                    p_bar.pack(pady=100)
                    start()

                # if sshd_status == 'NOT INSTALLED':
                # if sshd_status == 'OFF' or sshd_status == 'NOT INSTALLED':
                # if sshd_status != 'ON':
                #     print('2')
                #     # loading_label = Label(frame, text='Installing service...')
                #     loading_label.place(x=0, y=0, width=610, height=392)
                #     # p_bar = ttk.Progressbar(loading_label, orient=HORIZONTAL, length=400, mode='determinate')
                #     p_bar.pack(pady=100)
                #     start()
                # else:
                #     root.update_idletasks()
                #     time.sleep(1)
                #     recheck_sshd()

                return 'DONE'
            except pywintypes.error:
                messagebox.showerror(title='Access Denied', message=f"The SSH Service can't be Installed & Started without Admin access,\nPlease click 'Yes' in the popup window")
                return 'REJECTED'
            loading_label.destroy()  #
        elif cmnd == 'on_cmnd':
            try:
                shell.ShellExecuteEx(lpVerb='runas', lpFile='powershell.exe', lpParameters='/c ' + on_cmnd)
                loading_label = Label(frame, text='Starting SSH Service...', font=('Eras Bold ITC', main_window2.calc_width(20)), bg='white')
                loading_label.place(x=0, y=0, width=610, height=392)
                loading_label.after(5000, recheck_sshd)
                return 'DONE'
            except pywintypes.error:
                messagebox.showerror(title='Access Denied', message=f"The SSH Service can't be Started without Admin access,\nPlease click 'Yes' in the popup window")
                return 'REJECTED'
            loading_label.destroy()  #
        elif cmnd == 'off_cmnd':
            try:
                shell.ShellExecuteEx(lpVerb='runas', lpFile='powershell.exe', lpParameters='/c ' + off_cmnd)
                loading_label = Label(frame, text='Stopping SSH Service...', font=('Eras Bold ITC', main_window2.calc_width(20)), bg='white')
                loading_label.place(x=0, y=0, width=610, height=392)
                loading_label.after(5000, recheck_sshd)
                return 'DONE'
            except pywintypes.error:
                messagebox.showerror(title='Access Denied', message=f"The SSH Service can't be Stopped without Admin access,\nPlease click 'Yes' in the popup window")
                return 'REJECTED'
            loading_label.destroy()  #


    sshd_status = check_sshd_service('sshd')
    print(sshd_status)  # TEMP
    print(email)  # TEMP
    main_title = Label(be_controlled_frame, text='Be Controlled:', font=('Eras Bold ITC', main_window2.calc_width(35), 'bold'), fg='gray20', bg=label_bg_color)
    main_title.place(x=main_window2.calc_width(350), y=main_window2.calc_height(25))

    # def go_back():
    #     acc_signout()
    #     # frame.destroy()

    # def go_back():  # works
    #     sshd_status = check_sshd_service()
    #     if sshd_status == 'ON':
    #         messagebox.showinfo(title='SSH Service',
    #                              message='Please note that the SSH Service is still ON.\nTo stop it please go back and stop it')
    #         return choose_mode_window(email)
    #         # be_controlled_frame.destroy()
    #     else:
    #         return choose_mode_window(email)
    #         # be_controlled_frame.destroy()

    # # back_pic = ImageTk.PhotoImage(Image.open('back.png').resize((main_window2.calc_width(65), main_window2.calc_height(50)), Image.ANTIALIAS))
    # back_pic = ImageTk.PhotoImage(Image.open('back.png').resize((main_window2.calc_width(57), main_window2.calc_height(44)), Image.ANTIALIAS))  # GOOD
    signout_pic = ImageTk.PhotoImage(Image.open('signout.png').resize((main_window2.calc_width(57), main_window2.calc_height(51)), Image.ANTIALIAS))

    back_bttn = Button(be_controlled_frame, image=signout_pic, cursor='hand2',
                       font=('Eras Bold ITC', main_window2.calc_width(12)), fg='gray20', bg=buttons_bg_color,
                       command=acc_signout)#go_back)
    back_bttn.place(x=main_window2.calc_width(10), y=main_window2.calc_height(10))

    frame = Frame(be_controlled_frame, bg='white')
    frame.place(x=main_window2.calc_width(231), y=main_window2.calc_height(133), width=main_window2.calc_width(610), height=main_window2.calc_height(392))
    refresh_pic = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}\\icons\\refresh.png').resize((main_window2.calc_width(50), main_window2.calc_height(54)), Image.ANTIALIAS))

    refresh_bttn = Button(frame, text='Recheck\nService', font=('Eras Bold ITC', main_window2.calc_width(10), 'bold'), command=recheck_sshd, compound=TOP, justify=CENTER, image=refresh_pic, bg=buttons_bg_color)
    refresh_bttn.place(x=10, y=10)
    subtitle = Label(frame, font=('Eras Bold ITC', main_window2.calc_width(18), 'bold'), fg='gray20', bg='white')
    v_mark_pic = ImageTk.PhotoImage(Image.open('v.png').resize((main_window2.calc_width(70), main_window2.calc_height(70)), Image.ANTIALIAS))
    x_mark_pic = ImageTk.PhotoImage(Image.open('x.png').resize((main_window2.calc_width(70), main_window2.calc_height(70)), Image.ANTIALIAS))
    mark_label = Label(frame, font=('Eras Bold ITC', main_window2.calc_width(18), 'bold'), compound=LEFT, justify=CENTER, bg='white', padx=20)
    if sshd_status == 'ON':
        mark_label.configure(text='SSH Service is ON', image=v_mark_pic, fg='green')
        mark_label.place(x=main_window2.calc_width(110), y=main_window2.calc_height(10))
        subtitle.configure(text=f"This computer is ready to be connected to,\n\nEnter it's info and connect to it:\nIP: {SELF_IP}\nUsername: {SELF_NAME}")
        subtitle.place(x=main_window2.calc_width(0), y=main_window2.calc_height(130), width=main_window2.calc_width(610))
        # email_bttn = Button(frame, text='Email this info to someone', cursor='hand2', font=('Eras Bold ITC', main_window.calc_width(15)), bg=buttons_bg_color)#, command=)
        # email_bttn.place(x=150, y=285)
        off_bttn = Button(frame, text='Stop SSH Service', cursor='hand2', font=('Eras Bold ITC', main_window2.calc_width(15)), bg='brown1', command=lambda: run_power_shell('off_cmnd'))  # 'firebrick1/2 / red/red2
        off_bttn.place(x=main_window2.calc_width(200), y=main_window2.calc_height(310))
        # off_bttn.place(x=200, y=340)  # place like that if email button is placed

    elif sshd_status == 'OFF':
        start_button = Button(frame, text='Start SSH Service', cursor='hand2', font=('Eras Bold ITC', main_window2.calc_width(15)), bg='dodger blue', command=lambda: run_power_shell('on_cmnd'))
        start_button.place(x=main_window2.calc_width(200), y=main_window2.calc_height(300))
        mark_label.configure(text='SSH Service is OFF', image=x_mark_pic, fg='red')
        mark_label.place(x=main_window2.calc_width(110), y=main_window2.calc_height(10))
        subtitle.configure(font=('Eras Bold ITC', main_window2.calc_width(14), 'bold'), text=f"This computer needs to have the SSH service running\nfor other computers to connect to it.\n\nTo turn the service on please click the button bellow\nand approve the window that will popup:")
        subtitle.place(x=main_window2.calc_width(0), y=main_window2.calc_height(130), width=main_window2.calc_width(610))

    elif sshd_status == 'NOT INSTALLED':
        start_button = Button(frame, text='Install & Start SSH Service', cursor='hand2', font=('Eras Bold ITC', main_window2.calc_width(15)), bg='dodger blue', command=lambda: run_power_shell('install_and_on_cmnd'))
        start_button.place(x=main_window2.calc_width(160), y=main_window2.calc_height(300))
        mark_label.configure(text='SSH Service is\nNOT INSTALLED', image=x_mark_pic, fg='red')
        mark_label.place(x=main_window2.calc_width(130), y=main_window2.calc_height(10))
        subtitle.configure(font=('Eras Bold ITC', main_window2.calc_width(14), 'bold'), text=f"This computer needs to have the SSH service running\nfor other computers to connect to it.\n\nTo install the service and turn it on\nplease click the button bellow\nand approve the window that will popup:")
        subtitle.place(x=main_window2.calc_width(0), y=main_window2.calc_height(130), width=main_window2.calc_width(610))




    be_controlled_frame.mainloop()


def start_login_window(main_frame):
    global email, ip_dict, root
    email = None
    ip_dict = None

    def return_button(event):
        login_button.invoke()
        print('LOGIN')
    root.bind('<Return>', return_button)

    root.title('Remote File Explorer - Login')
    def submit():
        global email, ip_dict
        email_error_title.place_forget()
        pass_error_title.place_forget()
        # while True:
        #  add notification if server is down
        if enter_email.get() == '' or enter_password.get() == '':
            if enter_email.get() == '':
                email_error_title.configure(text='Please enter your email')
                email_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(110), width=main_window2.calc_width(500))  # (x=55, y=110, width=500)
            if enter_password.get() == '':
                pass_error_title.configure(text='Please enter your password')
                pass_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(215), width=main_window2.calc_width(500))  # (x=55, y=215, width=500)
            # break
        elif not manageSERVER.check_if_email_exists(enter_email.get()):  # check if email doesn't exist in the DB
            email_error_title.configure(text="This email address doesn't have an account")
            email_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(110), width=main_window2.calc_width(500))  # (x=55, y=110, width=500)
            # break
        elif manageSERVER.login(enter_email.get(), enter_password.get(), check_var.get()) == False:  # check if password doesn't match the email
            pass_error_title.configure(text='Email or Password are incorrect, Try again')
            pass_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(215), width=main_window2.calc_width(500))  # (x=55, y=215, width=500)
            # break
        else:  # email exists and the password matches
            email = enter_email.get()
            ip_dict = manageSERVER.get_ip_dict(email)
            # is_control = choose_is_control(root, login_frame)
            # print(is_control)
            login_frame.destroy()
            main_frame.quit()
            # break

    def forgot_pass():
        main_title.destroy()
        login_frame.destroy()
        play_video(mid_video_name)
        start_forgot_window(main_frame)

    def register():
        main_title.destroy()
        login_frame.destroy()
        play_video(mid_video_name)
        start_register_window(main_frame)

    def show_hide_pass():
        if enter_password.cget('show') == '':
            enter_password.configure(show='•')
            show_hide_button.configure(image=show_icon)
        else:
            enter_password.configure(show='')
            show_hide_button.configure(image=hide_icon)

    login_frame = Frame(main_frame, bg='white')
    login_frame.place(x=main_window2.calc_width(231), y=main_window2.calc_height(133), width=main_window2.calc_width(610), height=main_window2.calc_height(392))  # (x=231, y=133, width=610, height=392)

    email_error_title = Label(login_frame, text='Please enter your email', font=('Eras Bold ITC', main_window2.calc_width(10)), fg='red', bg='white')
    email_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(110), width=main_window2.calc_width(500))  # (x=55, y=110, width=500)
    pass_error_title = Label(login_frame, text='Please enter your password', font=('Eras Bold ITC', main_window2.calc_width(10)), fg='red', bg='white')
    pass_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(215), width=main_window2.calc_width(500))  # (x=55, y=215, width=500)
    email_error_title.place_forget()
    pass_error_title.place_forget()

    main_title = Label(main_frame, text='Remote File Explorer - Login', font=('Eras Bold ITC', main_window2.calc_width(35), 'bold'), fg='gray20', bg=label_bg_color)  # fg='goldenrod2'
    main_title.place(x=main_window2.calc_width(180), y=main_window2.calc_height(25))  # (x=180, y=25)

    email_title = Label(login_frame, text='Email:', font=('Eras Bold ITC', main_window2.calc_width(20), 'bold'), fg='gray20', bg='white').place(x=main_window2.calc_width(255), y=main_window2.calc_height(35))  # (x=255, y=35)
    enter_email = Entry(login_frame, font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20', bg='white', justify='center')
    enter_email.place(x=main_window2.calc_width(55), y=main_window2.calc_height(75), width=main_window2.calc_width(500), height=main_window2.calc_height(35))  # (x=55, y=75, width=500, height=35)

    password_title = Label(login_frame, text='Password:', font=('Eras Bold ITC', main_window2.calc_width(20), 'bold'), fg='gray20', bg='white').place(x=main_window2.calc_width(225), y=main_window2.calc_height(140))  # (x=225, y=140)
    enter_password = Entry(login_frame, font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20', bg='white', justify='center', show='•')
    enter_password.place(x=main_window2.calc_width(55), y=main_window2.calc_height(180), width=main_window2.calc_width(500), height=main_window2.calc_height(35))  # (x=55, y=180, width=500, height=35)

    show_hide_button = Button(login_frame, image=show_icon, cursor='hand2', bg=buttons_bg_color, command=show_hide_pass)
    show_hide_button.place(x=main_window2.calc_width(555), y=main_window2.calc_height(180), width=main_window2.calc_width(35), height=main_window2.calc_height(35))  # (x=555, y=180, width=35, height=35)

    check_var = IntVar(value=1)
    save_to_acc = Checkbutton(login_frame, cursor='hand2',
                              text="Save this PC's info to your account for future connections", fg='gray20',
                              bg=buttons_bg_color, font=('Eras Bold ITC', main_window2.calc_width(10)), onvalue=1, offvalue=0, variable=check_var)
    save_to_acc.place(x=main_window2.calc_width(105), y=main_window2.calc_height(245))  # (x=105, y=245)

    login_button = Button(login_frame, text='Login', cursor='hand2', font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20', bg=buttons_bg_color, command=submit)
    login_button.place(x=main_window2.calc_width(255), y=main_window2.calc_height(292), width=main_window2.calc_width(100), height=main_window2.calc_height(35))  # (x=255, y=292, width=100, height=35)

    register_button = Button(login_frame, text="Create a new account", cursor='hand2', bd=0, font=('Eras Bold ITC', main_window2.calc_width(10)), fg='gray20', bg=buttons_bg_color, command=register)
    register_button.place(x=main_window2.calc_width(130), y=main_window2.calc_height(350))  # (x=130, y=350)

    sep_line = ttk.Separator(login_frame, orient=VERTICAL)
    sep_line.place(x=main_window2.calc_width(302), y=main_window2.calc_height(342), width=main_window2.calc_width(1), height=main_window2.calc_height(40))  # (x=302, y=342, width=1, height=40)

    forgot_button = Button(login_frame, text='Reset your password', cursor='hand2', bd=0, font=('Eras Bold ITC', main_window2.calc_width(10)), fg='gray20', bg=buttons_bg_color, command=forgot_pass)
    # forgot_button.place(x=320, y=350)

    # main_frame.mainloop()
    # return email

    forgot_button.place(x=main_window2.calc_width(320), y=main_window2.calc_height(350))  # (x=320, y=350)

    enter_email.focus()


def start_register_window(main_frame):
    global email, ip_dict, root
    email = None
    ip_dict = None

    def return_button(event):
        register_button.invoke()
    root.bind('<Return>', return_button)

    root.title('Remote File Explorer - Register')
    def submit():
        global email, ip_dict
        email_error_title.place_forget()
        pass_error_title.place_forget()
        re_pass_error_title.place_forget()
        # while True:
        if enter_email.get() == '' or enter_password.get() == '' or re_enter_password.get() == '' or not email_regex(enter_email.get()):
            if enter_email.get() == '':
                email_error_title.configure(text='Please enter your email')
                email_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(85), width=main_window2.calc_width(500))  # (x=55, y=85, width=500)
            if enter_password.get() == '':
                pass_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(180), width=main_window2.calc_width(500))  # (x=55, y=180, width=500)
            if re_enter_password.get() == '':
                re_pass_error_title.configure(text='Please Retype the password')
                re_pass_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(275), width=main_window2.calc_width(500))  # (x=55, y=275, width=500)
            if not email_regex(enter_email.get()) and enter_email.get() != '':  # check if email is invalid
                email_error_title.configure(text='Please enter a valid email address')
                email_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(85), width=main_window2.calc_width(500))  # (x=55, y=85, width=500)
            # break
        elif enter_password.get() != re_enter_password.get():  # check if the two passwords aren't the same
            re_pass_error_title.configure(text="The passwords don't match")
            re_pass_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(275), width=main_window2.calc_width(500))  # (x=55, y=275, width=500)
            # break
        elif manageSERVER.check_if_email_exists(enter_email.get()):  # check if email exists already
            email_error_title.configure(text='This email address already has an account')
            email_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(85), width=main_window2.calc_width(500))  # (x=55, y=85, width=500)
            # break
        else:
            email = enter_email.get()
            password = enter_password.get()
            # ip_dict = dict()  # maybe add a tic box as well
            new_user_answr = manageSERVER.create_new_user(email, password)
            print(new_user_answr)
            if new_user_answr == 'EMAIL NOT SENT':
                # re_pass_error_title.configure(text="The account was created, but we were unable to send a confirmation email to this address")
                # re_pass_error_title.place(x=main_window.calc_width(55), y=main_window.calc_height(275), width=main_window.calc_width(500))
                error_label = Label(root, text="The account was created, but we were unable to send a confirmation email to this address")
                error_label.place(x=10, y=10)
            if new_user_answr:
                error_label = Label(root, text="Account created successfully")
                error_label.place(x=10, y=10)
                ip_dict = manageSERVER.get_ip_dict(email)
                # is_control = choose_is_control(root, register_frame)
                register_frame.destroy()
                main_frame.quit()
                # break
            elif not new_user_answr:
                re_pass_error_title.configure(text="An error occurred, account wasn't created. Please try again later")
                re_pass_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(275), width=main_window2.calc_width(500))


    def login():
        main_title.destroy()
        register_frame.destroy()
        play_video(mid_video_name)
        start_login_window(main_frame)

    def show_hide_pass1():
        if enter_password.cget('show') == '':
            enter_password.configure(show='•')
            show_hide_button1.configure(image=show_icon)
        else:
            enter_password.configure(show='')
            show_hide_button1.configure(image=hide_icon)

    def show_hide_pass2():
        if re_enter_password.cget('show') == '':
            re_enter_password.configure(show='•')
            show_hide_button2.configure(image=show_icon)
        else:
            re_enter_password.configure(show='')
            show_hide_button2.configure(image=hide_icon)

    def key_entered(key):
        password1 = enter_password.get()
        password2 = re_enter_password.get()
        if len(password1) > len(password2):
            password2 = re_enter_password.get() + key.char
        else:
            password1 = enter_password.get() + key.char
        print(f'pass1: {password1}\npass2: {password2}\n')
        re_pass_error_title.place_forget()
        if password1 != password2:
            re_pass_error_title.configure(text="The passwords don't match")
            re_pass_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(275), width=main_window2.calc_width(500))  # (x=55, y=275, width=500)

    # def pass_key_entered(key):
    #     if enter_password.get() != '' and re_enter_password.get() != '':
    #         password1 = enter_password.get() + key.char
    #         password2 = re_enter_password.get()
    #         re_pass_error_title.place_forget()
    #         if password1 != password2:
    #             re_pass_error_title.configure(text="The passwords don't match")
    #             re_pass_error_title.place(x=55, y=275, width=500)
    #
    # def re_pass_key_entered(key):
    #     if enter_password.get() != '' and re_enter_password.get() != '':
    #         password1 = enter_password.get()
    #         password2 = re_enter_password.get() + key.char
    #         re_pass_error_title.place_forget()
    #         if password1 != password2:
    #             re_pass_error_title.configure(text="The passwords don't match")
    #             re_pass_error_title.place(x=55, y=275, width=500)


    register_frame = Frame(main_frame, bg='white')
    register_frame.place(x=main_window2.calc_width(231), y=main_window2.calc_height(133), width=main_window2.calc_width(610), height=main_window2.calc_height(392))  # (x=231, y=133, width=610, height=392)

    email_error_title = Label(register_frame, text='Please enter your email', font=('Eras Bold ITC', main_window2.calc_width(10)), fg='red', bg='white')
    email_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(85), width=main_window2.calc_width(500))  # (x=55, y=85, width=500)
    pass_error_title = Label(register_frame, text='Please enter a password', font=('Eras Bold ITC', main_window2.calc_width(10)), fg='red', bg='white')
    pass_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(180), width=main_window2.calc_width(500))  # (x=55, y=180, width=500)
    re_pass_error_title = Label(register_frame, text='Please Retype the password', font=('Eras Bold ITC', main_window2.calc_width(10)), fg='red', bg='white')
    re_pass_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(275), width=main_window2.calc_width(500))  # (x=55, y=275, width=500)
    email_error_title.place_forget()
    pass_error_title.place_forget()
    re_pass_error_title.place_forget()

    main_title = Label(root, text='Remote File Explorer - Register', font=('Eras Bold ITC', main_window2.calc_width(35), 'bold'), fg='gray20', bg=label_bg_color)  # fg='goldenrod2'
    main_title.place(x=main_window2.calc_width(150), y=main_window2.calc_height(25))  # (x=150, y=25)

    email_title = Label(register_frame, text='Email:', font=('Eras Bold ITC', main_window2.calc_width(20), 'bold'), fg='gray20', bg='white').place(x=main_window2.calc_width(255), y=main_window2.calc_height(10))  # (x=255, y=10)
    enter_email = Entry(register_frame, font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20', bg='white', justify='center')
    enter_email.place(x=main_window2.calc_width(55), y=main_window2.calc_height(50), width=main_window2.calc_width(500), height=main_window2.calc_height(35))  # (x=55, y=50, width=500, height=35)

    password_title = Label(register_frame, text='Password:', font=('Eras Bold ITC', main_window2.calc_width(20), 'bold'), fg='gray20', bg='white').place(x=main_window2.calc_width(225), y=main_window2.calc_height(105))  # (x=225, y=105)
    enter_password = Entry(register_frame, font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20', bg='white', justify='center', show="•")
    enter_password.place(x=main_window2.calc_width(55), y=main_window2.calc_height(145), width=main_window2.calc_width(500), height=main_window2.calc_height(35))  # (x=55, y=145, width=500, height=35)

    enter_password.bind("<Key>", key_entered)

    show_hide_button1 = Button(register_frame, image=show_icon, cursor='hand2', bg=buttons_bg_color, command=show_hide_pass1)
    show_hide_button1.place(x=main_window2.calc_width(555), y=main_window2.calc_height(145), width=main_window2.calc_width(35), height=main_window2.calc_height(35))  # (x=555, y=145, width=35, height=35)

    re_password_title = Label(register_frame, text='Retype Password:', font=('Eras Bold ITC', main_window2.calc_width(20), 'bold'), fg='gray20', bg='white').place(x=main_window2.calc_width(180), y=main_window2.calc_height(200))  # (x=180, y=200)
    re_enter_password = Entry(register_frame, font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20', bg='white', justify='center', show="•")
    re_enter_password.place(x=main_window2.calc_width(55), y=main_window2.calc_height(240), width=main_window2.calc_width(500), height=main_window2.calc_height(35))  # (x=55, y=240, width=500, height=35)

    re_enter_password.bind("<Key>", key_entered)

    show_hide_button2 = Button(register_frame, image=show_icon, cursor='hand2', bg=buttons_bg_color, command=show_hide_pass2)
    show_hide_button2.place(x=main_window2.calc_width(555), y=main_window2.calc_height(240), width=main_window2.calc_width(35), height=main_window2.calc_height(35))  # (x=555, y=240, width=35, height=35)

    register_button = Button(register_frame, text='Register', cursor='hand2', font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20', bg=buttons_bg_color, command=submit)
    register_button.place(x=main_window2.calc_width(255), y=main_window2.calc_height(300), width=main_window2.calc_width(100), height=main_window2.calc_height(35))  # (x=255, y=300, width=100, height=35)

    login_button = Button(register_frame, text="Login to your account", cursor='hand2', bd=0, font=('Eras Bold ITC', main_window2.calc_width(10)), fg='gray20', bg=buttons_bg_color, command=login)
    # login_button.place(x=227, y=350)

    # main_frame.mainloop()
    # return email

    login_button.place(x=main_window2.calc_width(227), y=main_window2.calc_height(350))  # (x=227, y=350)

    enter_email.focus()


def start_forgot_window(main_frame):
    global email, root, reset_frame
    email = None

    def return_button(event):
        send_email_button.invoke()
    root.bind('<Return>', return_button)

    root.title('Remote File Explorer - Reset Password')
    def submit():
        global email
        email_error_title.place_forget()
        # while True:
        if enter_email.get() == '':
            email_error_title.configure(text='Please enter your email', fg='red')
            email_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(205), width=main_window2.calc_width(500))  # (x=55, y=205, width=500)
            # break
        elif manageSERVER.check_if_email_exists(enter_email.get()) == False:  # check if email doesn't exist
            email_error_title.configure(text="This email address doesn't have an account", fg='red')
            email_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(205), width=main_window2.calc_width(500))  # (x=55, y=205, width=500)
            # break
        else:  # email exists
            email = enter_email.get()
            if manageSERVER.generate_and_send_reset_code(email):
                email_error_title.configure(text='Email Sent!\nCheck your inbox and get back here with the reset code to reset you password', fg='green')
                email_error_title.place(x=main_window2.calc_width(305), y=main_window2.calc_height(225), width=main_window2.calc_width(610), anchor=CENTER)
            else:
                email_error_title.configure(text='There was an error!\nPlease try again', fg='red')
                email_error_title.place(x=main_window2.calc_width(305), y=main_window2.calc_height(225), width=main_window2.calc_width(610), anchor=CENTER)

    def login():
        main_title.destroy()
        reset_frame.destroy()
        play_video(mid_video_name)
        start_login_window(main_frame)

    back_pic = ImageTk.PhotoImage(Image.open('back.png').resize((main_window2.calc_width(46), main_window2.calc_height(35)), Image.ANTIALIAS))

    def new_pass_code():

        def return_button(event):
            reset_pass_bttn.invoke()
        root.bind('<Return>', return_button)

        def close_code_frame():
            enter_code_frame.destroy()

            def return_button(event):
                send_email_button.invoke()
            root.bind('<Return>', return_button)

        enter_code_frame = Frame(main_frame, bg='white')
        enter_code_frame.place(x=main_window2.calc_width(231), y=main_window2.calc_height(133),
                               width=main_window2.calc_width(610), height=main_window2.calc_height(392))
        back_bttn = Button(enter_code_frame, image=back_pic, cursor='hand2',
                           font=('Eras Bold ITC', main_window2.calc_width(12)), fg='gray20', bg=buttons_bg_color,
                           command=close_code_frame)
        back_bttn.place(x=main_window2.calc_width(5), y=main_window2.calc_height(5))

        def show_hide_pass1():
            if enter_password.cget('show') == '':
                enter_password.configure(show='•')
                show_hide_button1.configure(image=show_icon)
            else:
                enter_password.configure(show='')
                show_hide_button1.configure(image=hide_icon)

        def show_hide_pass2():
            if re_enter_password.cget('show') == '':
                re_enter_password.configure(show='•')
                show_hide_button2.configure(image=show_icon)
            else:
                re_enter_password.configure(show='')
                show_hide_button2.configure(image=hide_icon)

        def key_entered(key):
            password1 = enter_password.get()
            password2 = re_enter_password.get()
            if len(password1) > len(password2):
                password2 = re_enter_password.get() + key.char
            else:
                password1 = enter_password.get() + key.char
            print(f'pass1: {password1}\npass2: {password2}\n')
            re_pass_error_title.place_forget()
            if password1 != password2:
                re_pass_error_title.configure(text="The passwords don't match")
                re_pass_error_title.place(x=main_window2.calc_width(305), y=main_window2.calc_height(338), width=main_window2.calc_width(610), anchor=CENTER)

        reset_code_title = Label(enter_code_frame, text='Reset Code:',
                                 font=('Eras Bold ITC', main_window2.calc_width(20), 'bold'), fg='gray20',
                                 bg='white').place(x=main_window2.calc_width(305), y=main_window2.calc_height(20), width=main_window2.calc_width(300), anchor=CENTER)
        enter_reset_code = Entry(enter_code_frame, font=('Eras Bold ITC', main_window2.calc_width(15)),
                                 fg='gray20',
                                 bg='white', justify='center')
        enter_reset_code.place(x=main_window2.calc_width(305), y=main_window2.calc_height(57), width=main_window2.calc_width(300), height=main_window2.calc_height(35), anchor=CENTER)

        email_title = Label(enter_code_frame, text='Email:',
                            font=('Eras Bold ITC', main_window2.calc_width(20), 'bold'), fg='gray20',
                            bg='white').place(x=main_window2.calc_width(255),
                                              y=main_window2.calc_height(85))  # (x=255, y=10)
        enter_email = Entry(enter_code_frame, font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20',
                            bg='white', justify='center')
        enter_email.place(x=main_window2.calc_width(55), y=main_window2.calc_height(122),
                          width=main_window2.calc_width(500),
                          height=main_window2.calc_height(35))

        password_title = Label(enter_code_frame, text='New Password:',
                               font=('Eras Bold ITC', main_window2.calc_width(20), 'bold'), fg='gray20',
                               bg='white').place(x=main_window2.calc_width(165), y=main_window2.calc_height(167), width=main_window2.calc_width(300))
        enter_password = Entry(enter_code_frame, font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20',
                               bg='white', justify='center', show="•")
        enter_password.place(x=main_window2.calc_width(55), y=main_window2.calc_height(204),
                             width=main_window2.calc_width(500),
                             height=main_window2.calc_height(35))  # (x=55, y=145, width=500, height=35)

        enter_password.bind("<Key>", key_entered)

        show_hide_button1 = Button(enter_code_frame, image=show_icon, cursor='hand2', bg=buttons_bg_color,
                                           command=show_hide_pass1)
        show_hide_button1.place(x=main_window2.calc_width(555), y=main_window2.calc_height(204),
                                width=main_window2.calc_width(35),
                                height=main_window2.calc_height(35))  # (x=555, y=145, width=35, height=35)

        re_password_title = Label(enter_code_frame, text='Retype New Password:',
                                  font=('Eras Bold ITC', main_window2.calc_width(20), 'bold'), fg='gray20',
                                  bg='white').place(x=main_window2.calc_width(140),
                                                    y=main_window2.calc_height(254))  # (x=180, y=200)
        re_enter_password = Entry(enter_code_frame, font=('Eras Bold ITC', main_window2.calc_width(15)),
                                  fg='gray20', bg='white', justify='center', show="•")
        re_enter_password.place(x=main_window2.calc_width(55), y=main_window2.calc_height(291),
                                width=main_window2.calc_width(500),
                                height=main_window2.calc_height(35))  # (x=55, y=240, width=500, height=35)

        re_enter_password.bind("<Key>", key_entered)

        show_hide_button2 = Button(enter_code_frame, image=show_icon, cursor='hand2', bg=buttons_bg_color,
                                           command=show_hide_pass2)
        show_hide_button2.place(x=main_window2.calc_width(555), y=main_window2.calc_height(291),
                                width=main_window2.calc_width(35), height=main_window2.calc_height(35))


        reset_code_error_title = Label(enter_code_frame, text='Please enter the code you received in the email', font=('Eras Bold ITC', main_window2.calc_width(10)), fg='red', bg='white')
        email_error_title = Label(enter_code_frame, text='Please enter your email', font=('Eras Bold ITC', main_window2.calc_width(10)), fg='red', bg='white')
        pass_error_title = Label(enter_code_frame, text='Please enter a password', font=('Eras Bold ITC', main_window2.calc_width(10)), fg='red', bg='white')
        re_pass_error_title = Label(enter_code_frame, text='Please Retype the password', font=('Eras Bold ITC', main_window2.calc_width(10)), fg='red', bg='white')

        def reset_pass():
            reset_code_error_title.place_forget()
            email_error_title.place_forget()
            pass_error_title.place_forget()
            re_pass_error_title.place_forget()

            if reset_pass_bttn['text'] == 'Reset Password':
                if enter_reset_code.get() == '' or enter_email.get() == '' or enter_password.get() == '' or re_enter_password.get() == '':
                    if enter_reset_code.get() == '':
                        reset_code_error_title.place(x=main_window2.calc_width(305), y=main_window2.calc_height(83), width=main_window2.calc_width(610), height=main_window2.calc_height(16), anchor=CENTER)

                    if enter_email.get() == '':
                        email_error_title.configure(text='Please enter your email')
                        email_error_title.place(x=main_window2.calc_width(305), y=main_window2.calc_height(167), width=main_window2.calc_width(610), height=main_window2.calc_height(16), anchor=CENTER)

                    if enter_password.get() == '':
                        pass_error_title.place(x=main_window2.calc_width(305), y=main_window2.calc_height(252), width=main_window2.calc_width(610), anchor=CENTER)  # (x=55, y=180, width=500)

                    if re_enter_password.get() == '':
                        re_pass_error_title.configure(text='Please Retype the password')
                        re_pass_error_title.place(x=main_window2.calc_width(305), y=main_window2.calc_height(338), width=main_window2.calc_width(610), anchor=CENTER)

                elif enter_password.get() != re_enter_password.get():  # check if the two passwords aren't the same
                    re_pass_error_title.configure(text="The passwords don't match")
                    re_pass_error_title.place(x=main_window2.calc_width(305), y=main_window2.calc_height(338), width=main_window2.calc_width(610), anchor=CENTER)
                    # break
                elif not manageSERVER.check_if_email_exists(enter_email.get()):  # check if email doesn't exist
                    email_error_title.configure(text="This email address doesn't has an account")
                    email_error_title.place(x=main_window2.calc_width(305), y=main_window2.calc_height(167), width=main_window2.calc_width(610), height=main_window2.calc_height(8), anchor=CENTER)
                    # break
                else:
                    email = enter_email.get()
                    reset_code = enter_reset_code.get()
                    new_password = enter_password.get()
                    if not manageSERVER.reset_password(email, reset_code, new_password):
                        re_pass_error_title.configure(text='Some Information is incorrect! Please make sure the code and your email are correct and try again', fg='red')
                        re_pass_error_title.place(x=main_window2.calc_width(305), y=main_window2.calc_height(338), width=main_window2.calc_width(610), anchor=CENTER)
                    else:
                        enter_reset_code.configure(text='')
                        enter_email.configure(text='')
                        enter_password.configure(text='')
                        re_enter_password.configure(text='')

                        re_pass_error_title.configure(text='Your password was reset successfully!', fg='green')
                        re_pass_error_title.place(x=main_window2.calc_width(305), y=main_window2.calc_height(338), width=main_window2.calc_width(610), anchor=CENTER)
                        reset_pass_bttn.configure(text='Go to Log in')
            elif reset_pass_bttn['text'] == 'Go to Log in':
                main_title.destroy()
                reset_frame.destroy()
                play_video(mid_video_name)
                start_login_window(main_frame)

        reset_pass_bttn = Button(enter_code_frame, text='Reset Password', cursor='hand2',
                                 font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20',
                                 bg=buttons_bg_color, command=reset_pass)
        reset_pass_bttn.place(x=main_window2.calc_width(218), y=main_window2.calc_height(352),
                              width=main_window2.calc_width(174), height=main_window2.calc_height(35))
        enter_reset_code.focus()

    reset_frame = Frame(main_frame, bg='white')
    reset_frame.place(x=main_window2.calc_width(231), y=main_window2.calc_height(133), width=main_window2.calc_width(610), height=main_window2.calc_height(392))  # (x=231, y=133, width=610, height=392)

    email_error_title = Label(reset_frame, text='Please enter your email', font=('Eras Bold ITC', main_window2.calc_width(10)), fg='red', bg='white')
    email_error_title.place(x=main_window2.calc_width(55), y=main_window2.calc_height(205), width=main_window2.calc_width(500))  # (x=55, y=205, width=500)
    email_error_title.place_forget()

    main_title = Label(main_frame, text='Remote File Explorer - Reset Password', font=('Eras Bold ITC', main_window2.calc_width(35), 'bold'), fg='gray20', bg=label_bg_color)  # fg='goldenrod2'
    main_title.place(x=main_window2.calc_width(59), y=main_window2.calc_height(25))  # (x=59, y=25)

    email_title = Label(reset_frame, text='Email:', font=('Eras Bold ITC', main_window2.calc_width(20), 'bold'), fg='gray20', bg='white').place(x=main_window2.calc_width(255), y=main_window2.calc_height(130))  # (x=255, y=130)
    enter_email = Entry(reset_frame, font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20', bg='white', justify='center')
    enter_email.place(x=main_window2.calc_width(55), y=main_window2.calc_height(170), width=main_window2.calc_width(500), height=main_window2.calc_height(35))  # (x=55, y=170, width=500, height=35)

    email_title = Label(reset_frame, text='already got an email?', font=('Eras Bold ITC', main_window2.calc_width(12)), fg='gray20', bg='white').place(x=main_window2.calc_width(120), y=main_window2.calc_height(15))
    enter_reset_code_bttn = Button(reset_frame, text='Enter reset code', cursor='hand2', font=('Eras Bold ITC', main_window2.calc_width(12)), fg='gray20', bg=buttons_bg_color, command=new_pass_code)
    enter_reset_code_bttn.place(x=main_window2.calc_width(315), y=main_window2.calc_height(10), width=main_window2.calc_width(150), height=main_window2.calc_height(35))  # (x=235, y=270, width=140, height=35)

    send_email_button = Button(reset_frame, text='Send Email', cursor='hand2', font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20', bg=buttons_bg_color, command=submit)
    send_email_button.place(x=main_window2.calc_width(235), y=main_window2.calc_height(270), width=main_window2.calc_width(140), height=main_window2.calc_height(35))

    login_button = Button(reset_frame, text="Login to your account", cursor='hand2', bd=0, font=('Eras Bold ITC', main_window2.calc_width(10)), fg='gray20', bg=buttons_bg_color, command=login)
    # login_button.place(x=228, y=350)

    # main_frame.mainloop()
    # return email

    login_button.place(x=main_window2.calc_width(228), y=main_window2.calc_height(350))  # (x=228, y=350)

    enter_email.focus()


def close_window():
    discon_msg_box = messagebox.askquestion(title='Exit the app', message='Are you sure you want to exit the app?')
    if discon_msg_box == 'yes':
        root.destroy()


def play_video(video_name):
    global video, app_width, app_height, count
    count = 0
    video = imageio.get_reader(video_name)
    vid_frame = Frame(root)
    vid_frame.place(x=0, y=0, width=app_width, height=app_height)
    vid_label = Label(vid_frame)
    vid_label.place(x=0, y=0, width=app_width, height=app_height)
    thread = threading.Thread(target=stream, args=(vid_label, vid_frame, video_name))
    thread.daemon = 1
    thread.start()


def stream(vid_label, vid_frame, video_name):
    global count, video
    for image in video.iter_data():
        frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize((app_width, app_height), Image.ANTIALIAS))
        vid_label.config(image=frame_image)
        vid_label.image = frame_image
        count += 1
        # print(count)  # find out the number of frames
        if video_name == 'mid-animation.mp4' and count == 25:
            vid_frame.destroy()
        elif video_name == 'start-animation.mp4' and count == 20:
            vid_frame.destroy()
        elif video_name == 'end-animation.mp4' and count == 26:
            vid_frame.destroy()


def server_status(main_frame):
    status = manageSERVER.get_server_status()
    print(status)
    if status != 'SERVER IS UP':
        error_frame = Frame(main_frame, bg='white')
        error_frame.place(x=main_window2.calc_width(231), y=main_window2.calc_height(133), width=main_window2.calc_width(610), height=main_window2.calc_height(392))
        error_label = Label(error_frame, text='error', bg='white', font=('Arial', main_window2.calc_width(17), 'bold'))
        if status == 'SERVER IS DOWN':
            error_label.configure(text='The servers are currently DOWN!\n(You may also want to check your internet connection)\nPlease try again later.')
            # error_label.place(x=main_window.calc_width(225), y=main_window.calc_height(140))
        elif status == 'ERROR':
            error_label.configure(text='There was an error connecting to the servers!\nPlease try again later.')
            # error_label.place(x=main_window.calc_width(225), y=main_window.calc_height(140))
        error_label.place(x=main_window2.calc_width(305), y=main_window2.calc_height(170), width=main_window2.calc_width(610), anchor=CENTER)
        error_frame.mainloop()


def choose_mode_window(email):
    global answr
    answr = None
    def create_popup_window(title, label_text, msg_box_text, approve_text):
        global answr
        popup_width = main_window2.calc_width(400)
        popup_height = main_window2.calc_height(200)
        popup_x = int((screen_width - popup_width) / 2)
        popup_y = int((screen_height - popup_height) / 2)

        def submit():
            global answr
            pass_error_title.place_forget()
            password = enter_password.get()
            if password == '':
                if password == '':
                    pass_error_title.configure(text='Please enter your password')
                    pass_error_title.place(x=main_window2.calc_width(0), y=main_window2.calc_height(120),
                                           width=main_window2.calc_width(400))
            elif not manageSERVER.check_if_email_exists(email):  # check if email doesn't exist in the DB
                pass_error_title.configure(text="This email address doesn't have an account")
                pass_error_title.place(x=main_window2.calc_width(0), y=main_window2.calc_height(120),
                                       width=main_window2.calc_width(400))
            elif not manageSERVER.login(email, password, 0):  # check if password doesn't match the email
                pass_error_title.configure(text='Password is incorrect, Try again')
                pass_error_title.place(x=main_window2.calc_width(0), y=main_window2.calc_height(120),
                                       width=main_window2.calc_width(400))
            else:  # email exists and the password matches
                pass_error_title.place_forget()
                msg_box = messagebox.askquestion(title=title, message=f'{msg_box_text}\nThis action is not reversible!')
                if msg_box == 'yes':
                    if title == 'Reset saved IP list in your account':
                        if manageSERVER.reset_ip_dict(email, password):
                            answr = True
                            messagebox.showinfo(title=title, message=approve_text)
                            popup.quit()
                            # return True
                        else:
                            answr = False
                            popup.quit()
                            # return False

                    elif title == 'Permanently delete your account':
                        if manageSERVER.delete_account(email, password):
                            answr = True
                            messagebox.showinfo(title=title, message=approve_text)
                            popup.quit()
                            # return True
                        else:
                            answr = False
                            popup.quit()
                            # return False
                elif msg_box == 'no':
                    popup.quit()
                    answr = None

        def show_hide_pass():
            if enter_password.cget('show') == '':
                enter_password.configure(show='•')
                show_hide_button.configure(image=show_icon)
            else:
                enter_password.configure(show='')
                show_hide_button.configure(image=hide_icon)

        popup = Toplevel(bg=label_bg_color)
        popup.geometry(f'{popup_width}x{popup_height}+{popup_x}+{popup_y}')
        popup.iconbitmap('icon.ico')
        popup.resizable(False, False)
        popup.title(title)

        def enter_key(event):
            login_button.invoke()

        popup.bind('<Return>', enter_key)

        pass_error_title = Label(popup, text='Please enter your password', font=('Eras Bold ITC', main_window2.calc_width(10)), fg='red', bg=label_bg_color)
        pass_error_title.place(x=main_window2.calc_width(0), y=main_window2.calc_height(120), width=main_window2.calc_width(400))
        pass_error_title.place_forget()

        Label(popup, text=label_text, wraplength=popup_width, bg=label_bg_color, font=('Eras Bold ITC', main_window2.calc_width(12))).place(x=main_window2.calc_width(0), y=main_window2.calc_height(5), width=main_window2.calc_width(400))
        Label(popup, text=f'{email}', wraplength=popup_width, bg=label_bg_color, font=('Eras Bold ITC', main_window2.calc_width(15))).place(x=main_window2.calc_width(0), y=main_window2.calc_height(50), width=main_window2.calc_width(400))
        enter_password = Entry(popup, font=('Eras Bold ITC', main_window2.calc_width(15)), bg='white', justify='center', show='•')
        enter_password.place(x=main_window2.calc_width(32), y=main_window2.calc_height(85), width=main_window2.calc_width(300), height=main_window2.calc_height(35))
        show_hide_button = Button(popup, image=show_icon, cursor='hand2', bg=buttons_bg_color, command=show_hide_pass)
        show_hide_button.place(x=main_window2.calc_width(333), y=main_window2.calc_height(85), width=main_window2.calc_width(35), height=main_window2.calc_height(35))

        login_button = Button(popup, text='Login', cursor='hand2', font=('Eras Bold ITC', main_window2.calc_width(15)), fg='gray20', bg=buttons_bg_color, command=submit)
        login_button.place(x=main_window2.calc_width(150), y=main_window2.calc_height(145), width=main_window2.calc_width(100), height=main_window2.calc_height(32))
        enter_password.focus()
        # print(answr)
        popup.mainloop()
        # print(answr)
        # return answr

    def reset_ip_list():
        global answr
        create_popup_window('Reset saved IP list in your account', "Enter your account's password to delete all the saved IPs in your account:", f'Are you sure you want to delete all the IPs saved to your account: {email}?', 'IP list reset successfully')
        print(f'answr {answr}')
        if answr:
            root.destroy()
            main_window2.main()
        elif not answr:
            messagebox.showerror(title='Error', message="An error occurred while resetting your account's saved IPs list")

    def delete_account():
        global answr
        create_popup_window('Permanently delete your account', "Enter your account's password to permanently delete it:", f'Are you sure you want to permanently delete your account: {email}?', 'Account deleted successfully')
        print(f'answr {answr}')
        if answr:
            root.destroy()
            main_window2.main()
        elif not answr:
            messagebox.showerror(title='Error', message='An error occurred while deleting your account')
            root.destroy()
            main_window2.main()

    print(f'email: {email}')
    mode = None
    if email != None:
        try:
            account.delete(email)
            account.delete('Account Settings')
            account.delete('Sign Out')
            account.delete(0)
        except:
            pass
        finally:
            account.add_command(label=email, command=None, state='disabled', activebackground='grey90')

            settings_menu = Menu(account, tearoff=0)
            settings_menu.add_command(label='Reset saved IP list in your account', command=reset_ip_list,activebackground='steelblue2', activeforeground='black')
            settings_menu.add_command(label='Permanently delete your account', command=delete_account, activebackground='steelblue2', activeforeground='black')
            account.add_cascade(label='Account Settings', menu=settings_menu, activebackground='steelblue2', activeforeground='black')

            account.add_separator()
            account.add_command(label='Sign Out', command=acc_signout, activebackground='steelblue2', activeforeground='black')  # DodgerBlue2, DeepSkyBlue2
            root.title('Remote File Explorer')
            choose_frame = Frame(root)
            choose_frame.place(x=0, y=0, width=app_width, height=app_height)
            bg = ImageTk.PhotoImage(Image.open('background.png').resize((app_width, app_height), Image.ANTIALIAS))
            bg_image = Label(choose_frame, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
            # control_pic = ImageTk.PhotoImage(Image.open('control-pic.png').resize((160, 160), Image.ANTIALIAS))
            # be_controlled_pic = ImageTk.PhotoImage(Image.open('be-controlled-pic.png').resize((200, 160), Image.ANTIALIAS))
            control_pic = ImageTk.PhotoImage(
                Image.open('control-pic.png').resize((main_window2.calc_width(160), main_window2.calc_height(160)),
                                                     Image.ANTIALIAS))
            be_controlled_pic = ImageTk.PhotoImage(
                Image.open('be-controlled-pic.png').resize((main_window2.calc_width(200), main_window2.calc_height(160)),
                                                           Image.ANTIALIAS))
            mode = choose_mode(choose_frame, control_pic, be_controlled_pic)
            try:
                choose_frame.destroy()
            except:
                pass
            # if email == 'yaniv2':
            #     choose_frame.destroy()
            # choose_frame.mainloop()

    # if email != None:
    #     root = Tk()
    #     root.protocol("WM_DELETE_WINDOW", close_window)
    #     root.geometry(f'{app_width}x{app_height}+{x}+{y}')
    #     root.geometry(f'1070x700+{x}+{y}')
    #     root.iconbitmap('icon.ico')
    #     root.resizable(False, False)
    #     bg = PhotoImage(file='background.png')
    #     bg_image = Label(root, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    #     # mode = choose_is_control(root)
    #     frame = Frame(root, bg='black')
    #     frame.place(x=229, y=132, width=610, height=392)
    #     if email == 'yaniv2':
    #         frame.destroy()
    #     frame.mainloop()


    print(mode)
    # root.mainloop()
    # if email != None and mode != None:
    #     play_video(end_video_name)

    ssh = None
    sftp = None
    username = None
    if mode == 'control' and email != None:
        root.title('Remote File Explorer')
        ip_frame = Frame(root)
        ip_frame.place(x=0, y=0, width=app_width, height=app_height)
        bg = ImageTk.PhotoImage(Image.open('background.png').resize((app_width, app_height), Image.ANTIALIAS))
        bg_image = Label(ip_frame, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
        # control_pic = ImageTk.PhotoImage(Image.open('control-pic.png').resize((main_window.calc_width(160), main_window.calc_height(160)), Image.ANTIALIAS))
        # be_controlled_pic = ImageTk.PhotoImage(Image.open('be-controlled-pic.png').resize((main_window.calc_width(200), main_window.calc_height(160)), Image.ANTIALIAS))
        ssh, sftp, username = login_to_ssh_client(ip_frame, ip_dict)

    elif mode == 'be_controlled' and email != None:
        root.title('Remote File Explorer')
        be_controlled_frame = Frame(root)
        be_controlled_frame.place(x=0, y=0, width=app_width, height=app_height)
        bg = ImageTk.PhotoImage(Image.open('background.png').resize((app_width, app_height), Image.ANTIALIAS))
        bg_image = Label(be_controlled_frame, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
        set_be_controlled(be_controlled_frame)

    if email != None and mode != None and ssh != None:
        back_frame = Frame(root, bg=label_bg_color)
        back_frame.place(x=0, y=0, width=app_width, height=app_height)

    return email, mode, ssh, sftp, username


def main(root1, app_width1, app_height1, account1, ssh_service_menu1, email1):
    global main_frame, show_icon, hide_icon, mode, email, root, ip_dict
    global app_width, app_height, account, ssh_service_menu

    root = root1
    app_width = app_width1
    app_height = app_height1
    account = account1
    email = email1
    ssh_service_menu = ssh_service_menu1
    root.protocol("WM_DELETE_WINDOW", close_window)

    # app = wx.App(False)
    # screen_width, screen_height = wx.GetDisplaySize()

    # testing
    # app = Toplevel()
    # app.geometry('1280x720')
    # app2 = Toplevel()
    # app2.geometry('1070x700')
    #
    # screen_width = 1280
    # screen_height = 720
    # app_width = int(screen_width / 1.794)
    # app_height = int(screen_height / 1.542)
    # testing

    # if screen_width >= 1920 and screen_height >= 1080:
    #     app_width = 1070
    #     app_height = 700
    # else:
    #     app_width = int(screen_width / 1.794)
    #     app_height = int(screen_height / 1.542)


    # good - but no need
    # print(f'screen_width: {screen_width}')
    # print(f'screen_height: {screen_height}')
    #
    # print(f'app_width: {app_width}')
    # print(f'app_height: {app_height}')
    # x = int((screen_width - app_width) / 2)
    # y = int((screen_height - app_height) / 2)
    # print(f'x={x}, y={y}')
    # root.geometry(f'{app_width}x{app_height}+{x}+{y}')
    # # root.geometry(f'1070x700+{x}+{y}')
    # root.iconbitmap('icon.ico')
    # root.resizable(False, False)
    # good - but no need

    if email == None:

        main_frame = Frame(root)
        main_frame.place(x=0, y=0, width=app_width, height=app_height)

        # bg = PhotoImage(file='background.png')
        bg = ImageTk.PhotoImage(Image.open('background.png').resize((app_width, app_height), Image.ANTIALIAS))
        bg_image = Label(main_frame, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
        show_icon = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}/show.png').resize((main_window2.calc_width(30), main_window2.calc_height(30)), Image.ANTIALIAS))
        hide_icon = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}/hide.png').resize((main_window2.calc_width(30), main_window2.calc_height(30)), Image.ANTIALIAS))

        print(server_status(main_frame))

        play_video(start_video_name)
        # email = start_login_window(main_frame)

        start_login_window(main_frame)
        main_frame.mainloop()

    print(email)  # DELETE


    # while response == 'forgot' or response == 'login' or response == 'register':
    #     print(response)
    #     if response == 'forgot':
    #         response = start_forgot_window(root)
    #     if response == 'login':
    #         response = start_login_window(root)
    #     if response == 'register':
    #         response = start_register_window(root)

    # email = 'yaniv'  # test

    # def choose_mode_window(email):
    #     def acc_signout():
    #         discon_msg_box = messagebox.askquestion(title='Sign Out', message='Are you sure you want to sign out of your account?')
    #         if discon_msg_box == 'yes':
    #             root.destroy()
    #             main_window.main()
    #
    #     def settings_popup():
    #         pass
    #
    #     mode = None
    #     if email != None:
    #         account.add_command(label=email, command=None, state='disabled', activebackground='grey90')
    #         account.add_command(label='Account Settings', command=settings_popup, activebackground='steelblue2', activeforeground='black')
    #         account.add_separator()
    #         account.add_command(label='Sign Out', command=acc_signout, activebackground='steelblue2', activeforeground='black')  # DodgerBlue2, DeepSkyBlue2
    #         root.title('Remote File Explorer')
    #         choose_frame = Frame(root)
    #         choose_frame.place(x=0, y=0, width=app_width, height=app_height)
    #         bg = ImageTk.PhotoImage(Image.open('background.png').resize((app_width, app_height), Image.ANTIALIAS))
    #         bg_image = Label(choose_frame, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    #         # control_pic = ImageTk.PhotoImage(Image.open('control-pic.png').resize((160, 160), Image.ANTIALIAS))
    #         # be_controlled_pic = ImageTk.PhotoImage(Image.open('be-controlled-pic.png').resize((200, 160), Image.ANTIALIAS))
    #         control_pic = ImageTk.PhotoImage(Image.open('control-pic.png').resize((main_window.calc_width(160), main_window.calc_height(160)), Image.ANTIALIAS))
    #         be_controlled_pic = ImageTk.PhotoImage(Image.open('be-controlled-pic.png').resize((main_window.calc_width(200), main_window.calc_height(160)), Image.ANTIALIAS))
    #         mode = choose_mode(choose_frame, control_pic, be_controlled_pic)
    #         # if email == 'yaniv2':
    #         #     choose_frame.destroy()
    #         # choose_frame.mainloop()
    #
    #     # if email != None:
    #     #     root = Tk()
    #     #     root.protocol("WM_DELETE_WINDOW", close_window)
    #     #     root.geometry(f'{app_width}x{app_height}+{x}+{y}')
    #     #     root.geometry(f'1070x700+{x}+{y}')
    #     #     root.iconbitmap('icon.ico')
    #     #     root.resizable(False, False)
    #     #     bg = PhotoImage(file='background.png')
    #     #     bg_image = Label(root, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    #     #     # mode = choose_is_control(root)
    #     #     frame = Frame(root, bg='black')
    #     #     frame.place(x=229, y=132, width=610, height=392)
    #     #     if email == 'yaniv2':
    #     #         frame.destroy()
    #     #     frame.mainloop()
    #
    #     print(mode)
    #     # root.mainloop()
    #     # if email != None and mode != None:
    #     #     play_video(end_video_name)
    #
    #     ssh = None
    #     sftp = None
    #     username = None
    #     if mode == 'control' and email != None:
    #         root.title('Remote File Explorer')
    #         ip_frame = Frame(root)
    #         ip_frame.place(x=0, y=0, width=app_width, height=app_height)
    #         bg = ImageTk.PhotoImage(Image.open('background.png').resize((app_width, app_height), Image.ANTIALIAS))
    #         bg_image = Label(ip_frame, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    #         # control_pic = ImageTk.PhotoImage(Image.open('control-pic.png').resize((main_window.calc_width(160), main_window.calc_height(160)), Image.ANTIALIAS))
    #         # be_controlled_pic = ImageTk.PhotoImage(Image.open('be-controlled-pic.png').resize((main_window.calc_width(200), main_window.calc_height(160)), Image.ANTIALIAS))
    #         ssh, sftp, username = login_to_ssh_client(ip_frame, ip_dict)

    return choose_mode_window(email)

    # if email != None and mode != None and ssh != None:
    #     back_frame = Frame(root)
    #     back_frame.place(x=0, y=0, width=app_width, height=app_height)
    # return email, mode, ssh, sftp, username


# DELETE
# if __name__ == '__main__':
#     app = wx.App(False)
#     screen_width, screen_height = wx.GetDisplaySize()
#     # screen_width = 1000  # 1280  # temp
#     # screen_height = 700  # 720  # temp
#
#     if screen_width / screen_height != (1920 / 1080):
#         screen_height = screen_width / (1920 / 1080)
#
#     if screen_width >= 1070 and screen_height >= 700:
#         screen_width = 1920
#         screen_height = 1080
#
#     app_width = int(screen_width / 1.794)
#     app_height = int(screen_height / 1.542)
#     print(screen_width, screen_height, app_width, app_height)  # temp
#     root = Tk()
#     x = int((screen_width - app_width) / 2)
#     y = int((screen_height - app_height) / 2)
#     print(f'x={x}, y={y}')
#     root.geometry(f'{app_width}x{app_height}+{x}+{y}')
#     root.iconbitmap('icon.ico')
#     # root.resizable(False, False)
#     # def resize(event):
#     #     print("New size is: {}x{}".format(event.width, event.height))
#     # root.bind("<Configure>", resize)
#
#     # main(root, app_width, app_height)
#
#     root.title('Remote File Explorer')
#     choose_frame = Frame(root)
#     choose_frame.place(x=0, y=0, width=app_width, height=app_height)
#     bg = ImageTk.PhotoImage(Image.open('background.png').resize((app_width, app_height), Image.ANTIALIAS))
#     bg_image = Label(choose_frame, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
#     # control_pic = ImageTk.PhotoImage(Image.open('control-pic.png').resize((160, 160), Image.ANTIALIAS))
#     # be_controlled_pic = ImageTk.PhotoImage(Image.open('be-controlled-pic.png').resize((200, 160), Image.ANTIALIAS))
#     control_pic = ImageTk.PhotoImage(
#         Image.open('control-pic.png').resize((main_window.calc_width(160), main_window.calc_height(160)),
#                                              Image.ANTIALIAS))
#     be_controlled_pic = ImageTk.PhotoImage(
#         Image.open('be-controlled-pic.png').resize((main_window.calc_width(200), main_window.calc_height(160)),
#                                                    Image.ANTIALIAS))
#     # mode = choose_control(choose_frame, control_pic, be_controlled_pic)
#     # print(mode)
#
#
#     root.title('Remote File Explorer')
#     ip_frame = Frame(root)
#     ip_frame.place(x=0, y=0, width=app_width, height=app_height)
#     bg = ImageTk.PhotoImage(Image.open('background.png').resize((app_width, app_height), Image.ANTIALIAS))
#     bg_image = Label(ip_frame, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
#     # control_pic = ImageTk.PhotoImage(Image.open('control-pic.png').resize((main_window.calc_width(160), main_window.calc_height(160)), Image.ANTIALIAS))
#     # be_controlled_pic = ImageTk.PhotoImage(Image.open('be-controlled-pic.png').resize((main_window.calc_width(200), main_window.calc_height(160)), Image.ANTIALIAS))
#     ip_dict = {"10.211.55.4": "root", "192.168.56.1": "yaniv"}
#     print(show_ip_dict(ip_frame, ip_dict))