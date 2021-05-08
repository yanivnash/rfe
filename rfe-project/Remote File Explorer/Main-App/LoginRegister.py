__author__ = 'Yaniv Nash'

import manageSERVER
import manageSSH
import main_window
import threading
from tkinter import *
from tkinter import messagebox, ttk
from tkinter import simpledialog  # opens the popup to add a new ip
import imageio
import psutil
import wx
import re
from PIL import ImageTk, Image
import pyperclip  # copy to clipboard module
import sys
import os
import time
import socket

ROOT_PROJ_DIR = os.getcwd()
SELF_NAME = os.getlogin()
SELF_IP = socket.gethostbyname(socket.gethostname())

SELF_OS_PLATFORM = sys.platform
if SELF_OS_PLATFORM == 'win32' or SELF_OS_PLATFORM == 'cygwin':
    SELF_OS_PLATFORM = 'windows'
    import win32com.shell.shell as shell
    import pywintypes
elif SELF_OS_PLATFORM.startswith('linux'):
    SELF_OS_PLATFORM = 'linux'
elif SELF_OS_PLATFORM.startswith('darwin'):
    SELF_OS_PLATFORM = 'macos'

app = wx.App(False)

screen_width = main_window.screen_width
screen_height = main_window.screen_height

label_bg_color = '#e9eed6'
buttons_bg_color = '#d9dcc7'
start_video_name = f'{ROOT_PROJ_DIR}/assets/start-animation.mp4'
mid_video_name = f'{ROOT_PROJ_DIR}/assets/mid-animation.mp4'
end_video_name = f'{ROOT_PROJ_DIR}/assets/end-animation.mp4'


def no_action(event):
    pass


def email_regex(email):
    regex = r"""^[a-zA-Z]+(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    if re.match(regex, email):
        return True
    else:
        return False


def acc_signout():
    discon_msg_box = messagebox.askquestion(title='Sign Out',
                                            message='Are you sure you want to sign out of your account?')
    if discon_msg_box == 'yes':
        root.destroy()
        main_window.main()


def choose_mode(choose_frame, control_pic, be_controlled_pic):
    global mode, root
    global app_width, app_height
    mode = None

    def return_button(event):
        pass

    root.bind('<Return>', return_button)

    def control_bttn():
        global mode
        mode = 'control'
        choose_frame.quit()

    def be_controlled_bttn():
        global mode
        mode = 'be_controlled'
        choose_frame.quit()

    main_title = Label(choose_frame, text='Choose an action for this PC:',
                       font=('Eras Bold ITC', main_window.calc_size(35), 'bold'), fg='gray20', bg=label_bg_color)
    main_title.place(x=main_window.calc_size(180), y=main_window.calc_size(25))
    frame = Frame(choose_frame, bg='white')
    frame.place(x=main_window.calc_size(231), y=main_window.calc_size(133), width=main_window.calc_size(610),
                height=main_window.calc_size(392))
    control_button = Button(frame, cursor='hand2', command=control_bttn, image=control_pic, bd=0, bg='white')
    control_button.place(x=main_window.calc_size(70), y=main_window.calc_size(142))
    control_label = Label(frame, text='CONTROL', font=('Eras Bold ITC', main_window.calc_size(20), 'bold'),
                          fg='gray20', bg='white')
    control_label.place(x=main_window.calc_size(75), y=main_window.calc_size(100))
    be_controlled_button = Button(frame, cursor='hand2', command=be_controlled_bttn, image=be_controlled_pic, bd=0,
                                  bg='white')
    be_controlled_button.place(x=main_window.calc_size(350), y=main_window.calc_size(140))
    control_label = Label(frame, text='BE CONTROLLED', font=('Eras Bold ITC', main_window.calc_size(20), 'bold'),
                          fg='gray20', bg='white')
    control_label.place(x=main_window.calc_size(320), y=main_window.calc_size(100))

    choose_frame.mainloop()
    return mode


def get_network_ip_list():
    if SELF_OS_PLATFORM == 'windows':
        ipconfig = os.popen('ipconfig').read()
        self_ip = ipconfig[ipconfig.find('IPv4 Address'):ipconfig.find('Subnet Mask')]
        subnet_mask = ipconfig[ipconfig.find('Subnet Mask'):ipconfig.find('Default Gateway')]
        if 'Subnet Mask' in subnet_mask and 'IPv4 Address' in self_ip:
            self_ip = self_ip[self_ip.find(': ') + 2:].replace('\n', '').replace(' ', '')
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
    else:
        return []


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

    main_title = Label(ip_frame, text='Choose a computer to connect to:',
                       font=('Eras Bold ITC', main_window.calc_size(35), 'bold'), fg='gray20', bg=label_bg_color)
    main_title.place(x=main_window.calc_size(120), y=main_window.calc_size(25))

    frame = Frame(ip_frame, bg='white')
    frame.place(x=main_window.calc_size(231), y=main_window.calc_size(133), width=main_window.calc_size(610),
                height=main_window.calc_size(392))

    def mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def ip_butn_click(event):
        global ssh, sftp, check_var, username, host
        host = None
        key_list = list(ip_butns_dict.keys())
        val_list = list(ip_butns_dict.values())
        bttn_name = key_list[val_list.index(event.widget)]
        if bttn_name.__contains__('bttn'):
            host = bttn_name[:bttn_name.rfind('-bttn')]
            username = simpledialog.askstring('Enter Username', f'Enter the Username of {host}:', parent=root)
            if username != None:
                check_var = IntVar(value=1)
                try_connect(host, username)
        else:
            host = bttn_name[:bttn_name.index('-')]
            username = bttn_name[bttn_name.index('-') + 1:]
            check_var = IntVar(value=0)
            try_connect(host, username)

    def try_connect(host, username):
        global ssh, sftp
        ssh = None
        sftp = None
        password = simpledialog.askstring('Enter password', f'Enter the password to {host}:', show='•', parent=root)
        if password != None:
            ssh = manageSSH.connect_to_ssh(host, username, password)
            if ssh == "wrong password/username":
                messagebox.showerror(title="Couldn't connect",
                                     message=f"Couldn't connect to {host}\nPlease make sure the password and the username are correct and try again")
            elif ssh == "no connection":
                messagebox.showerror(title="Couldn't connect",
                                     message=f"Couldn't connect to {host}\nPlease make sure that the computer is connected to the internet, has Remote File Explorer open in the 'Be Controlled' screen and try again")
            elif ssh == "timeout":
                messagebox.showerror(title="Couldn't connect",
                                     message=f"Couldn't connect to {host}\nPlease make sure the password is correct, that the computer is connected to the internet, has Remote File Explorer open in the 'Be Controlled' screen and try again")
            else:
                sftp = ssh.open_sftp()
                if check_var.get() == 1:
                    manageSERVER.update_pc_in_account(email, (host, username))
                load_label = Label(ip_frame, text='Downloading Icons...', bg='white', font=('Eras Bold ITC',
                                                                                            main_window.calc_size(30)))
                load_label.place(x=main_window.calc_size(231), y=main_window.calc_size(133), width=main_window.calc_size(
                    610), height=main_window.calc_size(392))
                load_label.after(10, ip_frame.quit)

    back_pic = ImageTk.PhotoImage(
        Image.open(f'{ROOT_PROJ_DIR}/assets/back.png').resize((main_window.calc_size(57), main_window.calc_size(44)), Image.ANTIALIAS))
    signout_pic = ImageTk.PhotoImage(
        Image.open(f'{ROOT_PROJ_DIR}/assets/signout.png').resize((main_window.calc_size(57), main_window.calc_size(51)), Image.ANTIALIAS))
    signout_bttn = Button(ip_frame, image=signout_pic, cursor='hand2',
                          font=('Eras Bold ITC', main_window.calc_size(10)), fg='gray20', bg=buttons_bg_color,
                          command=acc_signout)
    signout_bttn.place(x=main_window.calc_size(10), y=main_window.calc_size(10))

    def create_enter_frame():
        global check_var, username

        main_title.configure(text="Enter a computer's info to connect to:")
        main_title.place(x=main_window.calc_size(85), y=main_window.calc_size(25))

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
                    ip_error_title.place(x=main_window.calc_size(50), y=main_window.calc_size(110),
                                         width=main_window.calc_size(500))
                if username == '':
                    username_error_title.configure(text='Please enter a username')
                    username_error_title.place(x=main_window.calc_size(50), y=main_window.calc_size(215),
                                               width=main_window.calc_size(500))
            else:
                try_connect(host, username)

        enter_frame = Frame(frame, bg='white')
        enter_frame.place(x=main_window.calc_size(0), y=main_window.calc_size(0), width=main_window.calc_size(610),
                          height=main_window.calc_size(392))

        def close_enter_frame():
            main_title.configure(text='Choose a computer to connect to:')
            main_title.place(x=main_window.calc_size(120), y=main_window.calc_size(25))

            root.bind('<Return>', no_action)
            enter_frame.destroy()

        signout_bttn = Button(enter_frame, command=close_enter_frame, cursor='hand2', bg=buttons_bg_color,
                              image=back_pic)
        signout_bttn.place(x=main_window.calc_size(10), y=main_window.calc_size(10))

        ip_error_title = Label(enter_frame, text='Please enter an ip',
                               font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg='white')
        ip_error_title.place(x=main_window.calc_size(50), y=main_window.calc_size(110),
                             width=main_window.calc_size(500))
        username_error_title = Label(enter_frame, text='Please enter a username',
                                     font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg='white')
        username_error_title.place(x=main_window.calc_size(50), y=main_window.calc_size(215),
                                   width=main_window.calc_size(500))
        ip_error_title.place_forget()
        username_error_title.place_forget()

        # enter ip
        Label(enter_frame, text='IP:', font=('Eras Bold ITC', main_window.calc_size(20), 'bold'), fg='gray20',
              bg='white').place(x=main_window.calc_size(285), y=main_window.calc_size(35))
        enter_ip = Entry(enter_frame, font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20', bg='white',
                         justify='center')
        enter_ip.place(x=main_window.calc_size(55), y=main_window.calc_size(75), width=main_window.calc_size(500),
                       height=main_window.calc_size(35))

        # enter username
        Label(enter_frame, text='Username:', font=('Eras Bold ITC', main_window.calc_size(20), 'bold'), fg='gray20',
              bg='white').place(x=main_window.calc_size(225), y=main_window.calc_size(140))  # (x=225, y=140)
        enter_username = Entry(enter_frame, font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20', bg='white',
                               justify='center')
        enter_username.place(x=main_window.calc_size(55), y=main_window.calc_size(180),
                             width=main_window.calc_size(500), height=main_window.calc_size(35))

        check_var = IntVar(value=1)
        save_to_acc = Checkbutton(enter_frame, cursor='hand2',
                                  text="Save this PC's info to your account for future connections", fg='gray20',
                                  bg=buttons_bg_color, font=('Eras Bold ITC', main_window.calc_size(10)), onvalue=1,
                                  offvalue=0, variable=check_var)
        save_to_acc.place(x=main_window.calc_size(105), y=main_window.calc_size(245))

        connect_button = Button(enter_frame, text='Connect', cursor='hand2',
                                font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20', bg=buttons_bg_color,
                                command=check_ip)
        connect_button.place(x=main_window.calc_size(255), y=main_window.calc_size(292),
                             width=main_window.calc_size(100), height=main_window.calc_size(35))

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

        scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg='white')
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        scrollable_frame.bind_all("<MouseWheel>", no_action)

        Label(scrollable_frame, height=main_window.calc_size(2), bg='white').pack()

        local_ip_list = get_network_ip_list()
        if local_ip_list == []:
            Label(scrollable_frame, text='No IP Addresses Found', font=('Eras Bold ITC', main_window.calc_size(20)),
                  bg=buttons_bg_color).place(x=main_window.calc_size(155), y=main_window.calc_size(170))
        else:
            for local_ip in local_ip_list:
                ip_butns_dict[f'{local_ip}-bttn'] = Button(scrollable_frame, bd=0, text=local_ip, cursor='hand2',
                                                           font=('Eras Bold ITC', main_window.calc_size(12)),
                                                           anchor=CENTER, fg='gray20', bg=buttons_bg_color)
                ip_butns_dict[f'{local_ip}-bttn'].pack(anchor=CENTER, pady=4)
                ip_butns_dict[f'{local_ip}-bttn'].bind("<Button-1>", ip_butn_click)
                ip_butns_dict[f'{local_ip}-bttn'].bind("<Enter>", on_enter)
                ip_butns_dict[f'{local_ip}-bttn'].bind("<Leave>", on_leave)

            if (num_of_temp_items - len(local_ip_list)) > 0:
                for _ in range(num_of_temp_items - len(local_ip_list)):
                    Button(scrollable_frame, bg='white', bd=0, font=('Eras Bold ITC', main_window.calc_size(12)),
                           state='disable').pack(anchor=CENTER, pady=4)

        if len(local_ip_list) > 8:
            canvas.create_window((0, 0), window=scrollable_frame, anchor=S,
                                 width=main_window.calc_size(610))
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollable_frame.bind_all("<MouseWheel>", mouse_wheel)
            scrollbar.pack(side="right", fill="y")
        else:
            canvas.create_window((0, 0), window=scrollable_frame, anchor=S,
                                 width=main_window.calc_size(610))
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
        canvas.yview_moveto('0.0')

    def show_account_ip_list():
        global scrollable_frame, scrollbar, canvas
        scrollbar.destroy()
        scrollable_frame.destroy()
        local_ip_bttn.configure(relief=RAISED)
        account_ip_bttn.configure(relief=SUNKEN)

        scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg='white')
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        scrollable_frame.bind_all("<MouseWheel>", no_action)

        Label(scrollable_frame, height=main_window.calc_size(2), bg='white').pack()

        if ip_dict == {}:
            Label(scrollable_frame, text='No IP Addresses Found', font=('Eras Bold ITC', main_window.calc_size(20)),
                  bg=buttons_bg_color).place(x=main_window.calc_size(155), y=main_window.calc_size(170))
        else:
            Label(scrollable_frame, wraplength=550,
                  text="*The Local IP addresses are only available if you're connected to the same local network as they are",
                  font=('Eras Bold ITC', main_window.calc_size(10)), bg='white').pack()
            for key, value in ip_dict.items():
                ip_butns_dict[f'{key}-{value}'] = Button(scrollable_frame, bd=0, text=f'{value} - {key}',
                                                         cursor='hand2',
                                                         font=('Eras Bold ITC', main_window.calc_size(12)),
                                                         anchor=CENTER, fg='gray20', bg=buttons_bg_color)
                ip_butns_dict[f'{key}-{value}'].pack(anchor=CENTER, pady=4)
                ip_butns_dict[f'{key}-{value}'].bind("<Button-1>", ip_butn_click)
                ip_butns_dict[f'{key}-{value}'].bind("<Enter>", on_enter)
                ip_butns_dict[f'{key}-{value}'].bind("<Leave>", on_leave)

            if (num_of_temp_items - len(ip_dict) - 1) > 0:
                for _ in range(num_of_temp_items - len(ip_dict) - 1):
                    Button(scrollable_frame, bg='white', bd=0, font=('Eras Bold ITC', main_window.calc_size(12)),
                           state='disable').pack(anchor=CENTER, pady=4)

        if len(ip_dict) > 8:
            canvas.create_window((0, 0), window=scrollable_frame, anchor=S,
                                 width=main_window.calc_size(610))
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollable_frame.bind_all("<MouseWheel>", mouse_wheel)
            scrollbar.pack(side="right", fill="y")
        else:
            canvas.create_window((0, 0), window=scrollable_frame, anchor=S,
                                 width=main_window.calc_size(610))
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
        canvas.yview_moveto('0.0')

    num_of_temp_items = max(len(get_network_ip_list()), len(ip_dict))
    canvas = Canvas(frame, bg='white')

    enter_ip_pic = ImageTk.PhotoImage(
        Image.open(f'{ROOT_PROJ_DIR}/assets/entry.png').resize((main_window.calc_size(55), main_window.calc_size(41)),
                                                               Image.ANTIALIAS))
    show_enter_frame_btn = Button(frame, command=create_enter_frame, image=enter_ip_pic, cursor='hand2',
                                  bg=buttons_bg_color, compound=BOTTOM, text='Enter an IP',
                                  font=('Eras Bold ITC', main_window.calc_size(10)))
    show_enter_frame_btn.place(x=main_window.calc_size(490), y=main_window.calc_size(60))

    local_ip_bttn = Button(frame, cursor='hand2', command=show_local_ip_list, bg=buttons_bg_color, borderwidth=3,
                           text='Local Network IPs', font=('Eras Bold ITC', main_window.calc_size(14)))
    local_ip_bttn.place(x=main_window.calc_size(0), y=main_window.calc_size(0), width=main_window.calc_size(305),
                        height=main_window.calc_size(40))

    account_ip_bttn = Button(frame, cursor='hand2', command=show_account_ip_list, bg=buttons_bg_color, borderwidth=3,
                             text='IPs saved to your account', font=('Eras Bold ITC', main_window.calc_size(14)))
    account_ip_bttn.place(x=main_window.calc_size(305), y=main_window.calc_size(0),
                          width=main_window.calc_size(305), height=main_window.calc_size(40))

    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack()
    scrollable_frame = Frame(canvas, bg='white')

    show_local_ip_list()

    canvas.yview_moveto('0.0')

    ip_frame.mainloop()
    return ssh, sftp, username


def check_sshd_service(service_name):
    if SELF_OS_PLATFORM == 'windows':
        service = None
        try:
            service = psutil.win_service_get(service_name)
            service = service.as_dict()
        except Exception:
            pass

        if service:
            if service['status'] == 'running':
                return 'ON'
            else:
                return 'OFF'
        else:
            return 'NOT INSTALLED'
    else:
        return None


def set_be_controlled(be_controlled_frame):
    def close_window():
        sshd_status = check_sshd_service('sshd')
        if sshd_status == 'OFF' or sshd_status == 'NOT INSTALLED' or sshd_status == None:
            close_msg_box = messagebox.askquestion(title='Close', message='Are you sure you want to close the window?')
            if close_msg_box == 'yes':
                root.destroy()
        elif sshd_status == 'ON':
            close_msg_box = messagebox.askquestion(title='Stop Service / Close',
                                                   message='Would you like to Close the window and Stop the SSH Service?\n(Stopping the SSH service will make your computer not available for others to connect to)')
            if close_msg_box == 'yes':
                if run_power_shell('off_cmnd') == 'DONE':
                    root.destroy()
            elif close_msg_box == 'no':
                root.destroy()

    root.protocol("WM_DELETE_WINDOW", close_window)

    def recheck_sshd():
        set_be_controlled(be_controlled_frame)

    def run_power_shell(cmnd):
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

            try:
                shell.ShellExecuteEx(lpVerb='runas', lpFile='powershell.exe', lpParameters='/c ' + install_and_on_cmnd)
                loading_label = Label(frame, text='Installing SSH Service...',
                                      font=('Eras Bold ITC', main_window.calc_size(20)), bg='white')
                loading_label.place(x=0, y=0, width=610, height=392)
                p_bar = ttk.Progressbar(loading_label, orient=HORIZONTAL, length=400, mode='determinate')
                p_bar.pack(pady=100)
                root.update_idletasks()
                start()

                sshd_status = check_sshd_service('sshd')
                if sshd_status == 'ON':
                    root.update_idletasks()
                    time.sleep(1)
                    recheck_sshd()
                else:
                    loading_label.place(x=0, y=0, width=610, height=392)
                    p_bar.pack(pady=100)
                    start()
                return 'DONE'
            except pywintypes.error:
                messagebox.showerror(title='Access Denied',
                                     message=f"The SSH Service can't be Installed & Started without Admin access,\nPlease click 'Yes' in the popup window")
                return 'REJECTED'
            loading_label.destroy()
        elif cmnd == 'on_cmnd':
            try:
                shell.ShellExecuteEx(lpVerb='runas', lpFile='powershell.exe', lpParameters='/c ' + on_cmnd)
                loading_label = Label(frame, text='Starting SSH Service...',
                                      font=('Eras Bold ITC', main_window.calc_size(20)), bg='white')
                loading_label.place(x=0, y=0, width=610, height=392)
                loading_label.after(5000, recheck_sshd)
                return 'DONE'
            except pywintypes.error:
                messagebox.showerror(title='Access Denied',
                                     message=f"The SSH Service can't be Started without Admin access,\nPlease click 'Yes' in the popup window")
                return 'REJECTED'
            loading_label.destroy()
        elif cmnd == 'off_cmnd':
            try:
                shell.ShellExecuteEx(lpVerb='runas', lpFile='powershell.exe', lpParameters='/c ' + off_cmnd)
                loading_label = Label(frame, text='Stopping SSH Service...',
                                      font=('Eras Bold ITC', main_window.calc_size(20)), bg='white')
                loading_label.place(x=0, y=0, width=610, height=392)
                loading_label.after(5000, recheck_sshd)
                return 'DONE'
            except pywintypes.error:
                messagebox.showerror(title='Access Denied',
                                     message=f"The SSH Service can't be Stopped without Admin access,\nPlease click 'Yes' in the popup window")
                return 'REJECTED'
            loading_label.destroy()

    sshd_status = check_sshd_service('sshd')
    main_title = Label(be_controlled_frame, text='Be Controlled:',
                       font=('Eras Bold ITC', main_window.calc_size(35), 'bold'), fg='gray20', bg=label_bg_color)
    main_title.place(x=main_window.calc_size(350), y=main_window.calc_size(25))
    signout_pic = ImageTk.PhotoImage(
        Image.open(f'{ROOT_PROJ_DIR}/assets/signout.png').resize((main_window.calc_size(57), main_window.calc_size(51)), Image.ANTIALIAS))

    signout_bttn = Button(be_controlled_frame, image=signout_pic, cursor='hand2',
                          font=('Eras Bold ITC', main_window.calc_size(12)), fg='gray20', bg=buttons_bg_color,
                          command=acc_signout)
    signout_bttn.place(x=main_window.calc_size(10), y=main_window.calc_size(10))

    frame = Frame(be_controlled_frame, bg='white')
    frame.place(x=main_window.calc_size(231), y=main_window.calc_size(133), width=main_window.calc_size(610),
                height=main_window.calc_size(392))

    if SELF_OS_PLATFORM == 'windows':
        refresh_pic = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}/assets/refresh.png').resize(
            (main_window.calc_size(50), main_window.calc_size(54)), Image.ANTIALIAS))
        refresh_bttn = Button(frame, text='Recheck\nService', font=('Eras Bold ITC', main_window.calc_size(10), 'bold'),
                              command=recheck_sshd, compound=TOP, justify=CENTER, image=refresh_pic, bg=buttons_bg_color)
        refresh_bttn.place(x=10, y=10)
        subtitle = Label(frame, font=('Eras Bold ITC', main_window.calc_size(18), 'bold'), fg='gray20', bg='white')
        v_mark_pic = ImageTk.PhotoImage(
            Image.open(f'{ROOT_PROJ_DIR}/assets/v.png').resize((main_window.calc_size(70), main_window.calc_size(70)),
                                                               Image.ANTIALIAS))
        x_mark_pic = ImageTk.PhotoImage(
            Image.open(f'{ROOT_PROJ_DIR}/assets/x.png').resize((main_window.calc_size(70), main_window.calc_size(70)),
                                                               Image.ANTIALIAS))
        mark_label = Label(frame, font=('Eras Bold ITC', main_window.calc_size(18), 'bold'), compound=LEFT, justify=CENTER,
                           bg='white', padx=20)
        if sshd_status == 'ON':
            mark_label.configure(text='SSH Service is ON', image=v_mark_pic, fg='green')
            mark_label.place(x=main_window.calc_size(110), y=main_window.calc_size(10))
            subtitle.configure(
                text=f"This computer is ready to be connected to,\n\nEnter it's info and connect to it:\nIP: {SELF_IP}\nUsername: {SELF_NAME}")
            subtitle.place(x=main_window.calc_size(0), y=main_window.calc_size(130), width=main_window.calc_size(610))
            off_bttn = Button(frame, text='Stop SSH Service', cursor='hand2',
                              font=('Eras Bold ITC', main_window.calc_size(15)), bg='brown1',
                              command=lambda: run_power_shell('off_cmnd'))
            off_bttn.place(x=main_window.calc_size(200), y=main_window.calc_size(310))

        elif sshd_status == 'OFF':
            start_button = Button(frame, text='Start SSH Service', cursor='hand2',
                                  font=('Eras Bold ITC', main_window.calc_size(15)), bg='dodger blue',
                                  command=lambda: run_power_shell('on_cmnd'))
            start_button.place(x=main_window.calc_size(200), y=main_window.calc_size(300))
            mark_label.configure(text='SSH Service is OFF', image=x_mark_pic, fg='red')
            mark_label.place(x=main_window.calc_size(110), y=main_window.calc_size(10))
            subtitle.configure(font=('Eras Bold ITC', main_window.calc_size(14), 'bold'),
                               text=f"This computer needs to have the SSH service running\nfor other computers to connect to it.\n\nTo turn the service on please click the button bellow\nand approve the window that will popup:")
            subtitle.place(x=main_window.calc_size(0), y=main_window.calc_size(130), width=main_window.calc_size(610))

        elif sshd_status == 'NOT INSTALLED':
            start_button = Button(frame, text='Install & Start SSH Service', cursor='hand2',
                                  font=('Eras Bold ITC', main_window.calc_size(15)), bg='dodger blue',
                                  command=lambda: run_power_shell('install_and_on_cmnd'))
            start_button.place(x=main_window.calc_size(160), y=main_window.calc_size(300))
            mark_label.configure(text='SSH Service is\nNOT INSTALLED', image=x_mark_pic, fg='red')
            mark_label.place(x=main_window.calc_size(130), y=main_window.calc_size(10))
            subtitle.configure(font=('Eras Bold ITC', main_window.calc_size(14), 'bold'),
                               text=f"This computer needs to have the SSH service running\nfor other computers to connect to it.\n\nTo install the service and turn it on\nplease click the button bellow\nand approve the window that will popup:")
            subtitle.place(x=main_window.calc_size(0), y=main_window.calc_size(130), width=main_window.calc_size(610))

    elif SELF_OS_PLATFORM == 'linux':
        subtitle = Label(frame, font=('Eras Bold ITC', main_window.calc_size(18), 'bold'), fg='gray20', bg='white',
                         wraplength=600,
                         text=f"To connect to this computer make sure the SSH Server is enabled:\n\nTo install & start the server, run:\nsudo apt install openssh-server\n\nYour information:\nIP: {SELF_IP}\nUsername: {SELF_NAME}")
        subtitle.place(x=main_window.calc_size(0), y=main_window.calc_size(80), width=main_window.calc_size(610))

        copy_bttn = Button(frame, text='Copy Command', cursor='hand2',
                           font=('Eras Bold ITC', main_window.calc_size(15)), bg=buttons_bg_color,
                           command=lambda: pyperclip.copy('sudo apt install openssh-server'))
        copy_bttn.place(x=main_window.calc_size(10), y=main_window.calc_size(10))

    elif SELF_OS_PLATFORM == 'macos':
        subtitle = Label(frame, font=('Eras Bold ITC', main_window.calc_size(18), 'bold'), fg='gray20', bg='white',
                         wraplength=600,
                         text=f"To connect to this computer make sure the SSH Server is enabled:\n\nTo start the server, run:\nsudo systemsetup -setremotelogin on\n\nYour information:\nIP: {SELF_IP}\nUsername: {SELF_NAME}")
        subtitle.place(x=main_window.calc_size(0), y=main_window.calc_size(80), width=main_window.calc_size(610))

        copy_bttn = Button(frame, text='Copy Command', cursor='hand2',
                           font=('Eras Bold ITC', main_window.calc_size(15)), bg=buttons_bg_color,
                           command=lambda: pyperclip.copy('sudo systemsetup -setremotelogin on'))
        copy_bttn.place(x=main_window.calc_size(10), y=main_window.calc_size(10))

    be_controlled_frame.mainloop()


def start_login_window(main_frame):
    global email, ip_dict, root
    email = None
    ip_dict = None

    def return_button(event):
        login_button.invoke()

    root.bind('<Return>', return_button)

    root.title('Remote File Explorer - Login')

    def submit():
        global email, ip_dict
        email_error_title.place_forget()
        pass_error_title.place_forget()
        if enter_email.get() == '' or enter_password.get() == '':
            if enter_email.get() == '':
                email_error_title.configure(text='Please enter your email')
                email_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(110),
                                        width=main_window.calc_size(500))
            if enter_password.get() == '':
                pass_error_title.configure(text='Please enter your password')
                pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(215),
                                       width=main_window.calc_size(500))

        elif not manageSERVER.check_if_email_exists(enter_email.get()):
            # check if email doesn't exist in the DB
            email_error_title.configure(text="This email address doesn't have an account")
            email_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(110),
                                    width=main_window.calc_size(500))

        elif not manageSERVER.login(enter_email.get(), enter_password.get(), check_var.get()):
            # check if password doesn't match the email
            pass_error_title.configure(text='Email or Password are incorrect, Try again')
            pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(215),
                                   width=main_window.calc_size(500))

        else:
            # email exists and the password matches
            email = enter_email.get()
            ip_dict = manageSERVER.get_ip_dict(email)
            login_frame.destroy()
            main_frame.quit()

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
    login_frame.place(x=main_window.calc_size(231), y=main_window.calc_size(133), width=main_window.calc_size(610),
                      height=main_window.calc_size(392))

    email_error_title = Label(login_frame, text='Please enter your email',
                              font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg='white')
    email_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(110),
                            width=main_window.calc_size(500))
    pass_error_title = Label(login_frame, text='Please enter your password',
                             font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg='white')
    pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(215),
                           width=main_window.calc_size(500))
    email_error_title.place_forget()
    pass_error_title.place_forget()

    main_title = Label(main_frame, text='Remote File Explorer - Login',
                       font=('Eras Bold ITC', main_window.calc_size(35), 'bold'), fg='gray20', bg=label_bg_color)
    main_title.place(x=main_window.calc_size(180), y=main_window.calc_size(25))  # (x=180, y=25)

    # enter email
    Label(login_frame, text='Email:', font=('Eras Bold ITC', main_window.calc_size(20), 'bold'), fg='gray20',
          bg='white').place(x=main_window.calc_size(255), y=main_window.calc_size(35))
    enter_email = Entry(login_frame, font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20', bg='white',
                        justify='center')
    enter_email.place(x=main_window.calc_size(55), y=main_window.calc_size(75), width=main_window.calc_size(500),
                      height=main_window.calc_size(35))

    # enter password
    Label(login_frame, text='Password:', font=('Eras Bold ITC', main_window.calc_size(20), 'bold'), fg='gray20',
          bg='white').place(x=main_window.calc_size(225), y=main_window.calc_size(140))
    enter_password = Entry(login_frame, font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20', bg='white',
                           justify='center', show='•')
    enter_password.place(x=main_window.calc_size(55), y=main_window.calc_size(180),
                         width=main_window.calc_size(500), height=main_window.calc_size(35))

    show_hide_button = Button(login_frame, image=show_icon, cursor='hand2', bg=buttons_bg_color, command=show_hide_pass)
    show_hide_button.place(x=main_window.calc_size(555), y=main_window.calc_size(180),
                           width=main_window.calc_size(35), height=main_window.calc_size(35))

    check_var = IntVar(value=1)
    save_to_acc = Checkbutton(login_frame, cursor='hand2',
                              text="Save this PC's info to your account for future connections", fg='gray20',
                              bg=buttons_bg_color, font=('Eras Bold ITC', main_window.calc_size(10)), onvalue=1,
                              offvalue=0, variable=check_var)
    save_to_acc.place(x=main_window.calc_size(105), y=main_window.calc_size(245))

    login_button = Button(login_frame, text='Login', cursor='hand2', font=('Eras Bold ITC', main_window.calc_size(15)),
                          fg='gray20', bg=buttons_bg_color, command=submit)
    login_button.place(x=main_window.calc_size(255), y=main_window.calc_size(292), width=main_window.calc_size(100),
                       height=main_window.calc_size(35))

    register_button = Button(login_frame, text="Create a new account", cursor='hand2', bd=0,
                             font=('Eras Bold ITC', main_window.calc_size(10)), fg='gray20', bg=buttons_bg_color,
                             command=register)
    register_button.place(x=main_window.calc_size(130), y=main_window.calc_size(350))

    sep_line = ttk.Separator(login_frame, orient=VERTICAL)
    sep_line.place(x=main_window.calc_size(302), y=main_window.calc_size(342), width=main_window.calc_size(1),
                   height=main_window.calc_size(40))

    forgot_button = Button(login_frame, text='Reset your password', cursor='hand2', bd=0,
                           font=('Eras Bold ITC', main_window.calc_size(10)), fg='gray20', bg=buttons_bg_color,
                           command=forgot_pass)
    forgot_button.place(x=main_window.calc_size(320), y=main_window.calc_size(350))

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
        if enter_email.get() == '' or enter_password.get() == '' or re_enter_password.get() == '' or not email_regex(
                enter_email.get()):
            if enter_email.get() == '':
                email_error_title.configure(text='Please enter your email')
                email_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(85),
                                        width=main_window.calc_size(500))
            if enter_password.get() == '':
                pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(180),
                                       width=main_window.calc_size(500))
            if re_enter_password.get() == '':
                re_pass_error_title.configure(text='Please Retype the password')
                re_pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(275),
                                          width=main_window.calc_size(500))
            if not email_regex(enter_email.get()) and enter_email.get() != '':
                # check if email is invalid
                email_error_title.configure(text='Please enter a valid email address')
                email_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(85),
                                        width=main_window.calc_size(500))
        elif enter_password.get() != re_enter_password.get():
            # check if the two passwords aren't the same
            re_pass_error_title.configure(text="The passwords don't match")
            re_pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(275),
                                      width=main_window.calc_size(500))
        elif manageSERVER.check_if_email_exists(enter_email.get()):
            # check if email exists already
            email_error_title.configure(text='This email address already has an account')
            email_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(85),
                                    width=main_window.calc_size(500))
        else:
            email = enter_email.get()
            password = enter_password.get()
            new_user_answr = manageSERVER.create_new_user(email, password)
            if new_user_answr == 'EMAIL NOT SENT':
                error_label = Label(root,
                                    text="The account was created, but we were unable to send a confirmation email to this address")
                error_label.place(x=10, y=10)
            if new_user_answr:
                error_label = Label(root, text="Account created successfully")
                error_label.place(x=10, y=10)
                ip_dict = manageSERVER.get_ip_dict(email)
                register_frame.destroy()
                main_frame.quit()
            elif not new_user_answr:
                re_pass_error_title.configure(text="An error occurred, account wasn't created. Please try again later")
                re_pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(275),
                                          width=main_window.calc_size(500))

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
        re_pass_error_title.place_forget()
        if password1 != password2:
            re_pass_error_title.configure(text="The passwords don't match")
            re_pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(275),
                                      width=main_window.calc_size(500))

    register_frame = Frame(main_frame, bg='white')
    register_frame.place(x=main_window.calc_size(231), y=main_window.calc_size(133),
                         width=main_window.calc_size(610), height=main_window.calc_size(392))

    email_error_title = Label(register_frame, text='Please enter your email',
                              font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg='white')
    email_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(85),
                            width=main_window.calc_size(500))
    pass_error_title = Label(register_frame, text='Please enter a password',
                             font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg='white')
    pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(180),
                           width=main_window.calc_size(500))
    re_pass_error_title = Label(register_frame, text='Please Retype the password',
                                font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg='white')
    re_pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(275),
                              width=main_window.calc_size(500))
    email_error_title.place_forget()
    pass_error_title.place_forget()
    re_pass_error_title.place_forget()

    main_title = Label(root, text='Remote File Explorer - Register',
                       font=('Eras Bold ITC', main_window.calc_size(35), 'bold'), fg='gray20', bg=label_bg_color)
    main_title.place(x=main_window.calc_size(150), y=main_window.calc_size(25))

    # enter email
    Label(register_frame, text='Email:', font=('Eras Bold ITC', main_window.calc_size(20), 'bold'), fg='gray20',
          bg='white').place(x=main_window.calc_size(255), y=main_window.calc_size(10))
    enter_email = Entry(register_frame, font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20', bg='white',
                        justify='center')
    enter_email.place(x=main_window.calc_size(55), y=main_window.calc_size(50), width=main_window.calc_size(500),
                      height=main_window.calc_size(35))

    # enter password
    Label(register_frame, text='Password:', font=('Eras Bold ITC', main_window.calc_size(20), 'bold'), fg='gray20',
          bg='white').place(x=main_window.calc_size(225), y=main_window.calc_size(105))
    enter_password = Entry(register_frame, font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20', bg='white',
                           justify='center', show="•")
    enter_password.place(x=main_window.calc_size(55), y=main_window.calc_size(145),
                         width=main_window.calc_size(500), height=main_window.calc_size(35))

    enter_password.bind("<Key>", key_entered)

    show_hide_button1 = Button(register_frame, image=show_icon, cursor='hand2', bg=buttons_bg_color,
                               command=show_hide_pass1)
    show_hide_button1.place(x=main_window.calc_size(555), y=main_window.calc_size(145),
                            width=main_window.calc_size(35), height=main_window.calc_size(35))

    # re-enter password
    Label(register_frame, text='Retype Password:', font=('Eras Bold ITC', main_window.calc_size(20), 'bold'),
          fg='gray20', bg='white').place(x=main_window.calc_size(180), y=main_window.calc_size(200))
    re_enter_password = Entry(register_frame, font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20',
                              bg='white', justify='center', show="•")
    re_enter_password.place(x=main_window.calc_size(55), y=main_window.calc_size(240),
                            width=main_window.calc_size(500), height=main_window.calc_size(35))

    re_enter_password.bind("<Key>", key_entered)

    show_hide_button2 = Button(register_frame, image=show_icon, cursor='hand2', bg=buttons_bg_color,
                               command=show_hide_pass2)
    show_hide_button2.place(x=main_window.calc_size(555), y=main_window.calc_size(240),
                            width=main_window.calc_size(35), height=main_window.calc_size(35))

    register_button = Button(register_frame, text='Register', cursor='hand2',
                             font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20', bg=buttons_bg_color,
                             command=submit)
    register_button.place(x=main_window.calc_size(255), y=main_window.calc_size(300),
                          width=main_window.calc_size(100), height=main_window.calc_size(35))

    login_button = Button(register_frame, text="Login to your account", cursor='hand2', bd=0,
                          font=('Eras Bold ITC', main_window.calc_size(10)), fg='gray20', bg=buttons_bg_color,
                          command=login)
    login_button.place(x=main_window.calc_size(227), y=main_window.calc_size(350))

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
        if enter_email.get() == '':
            email_error_title.configure(text='Please enter your email', fg='red')
            email_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(205),
                                    width=main_window.calc_size(500))
        elif not manageSERVER.check_if_email_exists(enter_email.get()):
            # check if email doesn't exist
            email_error_title.configure(text="This email address doesn't have an account", fg='red')
            email_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(205),
                                    width=main_window.calc_size(500))
        else:
            # email exists
            email = enter_email.get()
            if manageSERVER.generate_and_send_reset_code(email):
                email_error_title.configure(
                    text='Email Sent!\nCheck your inbox and get back here with the reset code to reset you password',
                    fg='green')
                email_error_title.place(x=main_window.calc_size(305), y=main_window.calc_size(225),
                                        width=main_window.calc_size(610), anchor=CENTER)
            else:
                email_error_title.configure(text='There was an error!\nPlease try again', fg='red')
                email_error_title.place(x=main_window.calc_size(305), y=main_window.calc_size(225),
                                        width=main_window.calc_size(610), anchor=CENTER)

    def login():
        main_title.destroy()
        reset_frame.destroy()
        play_video(mid_video_name)
        start_login_window(main_frame)

    back_pic = ImageTk.PhotoImage(
        Image.open(f'{ROOT_PROJ_DIR}/assets/back.png').resize((main_window.calc_size(46), main_window.calc_size(35)), Image.ANTIALIAS))

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
        enter_code_frame.place(x=main_window.calc_size(231), y=main_window.calc_size(133),
                               width=main_window.calc_size(610), height=main_window.calc_size(392))
        back_bttn = Button(enter_code_frame, image=back_pic, cursor='hand2',
                           font=('Eras Bold ITC', main_window.calc_size(12)), fg='gray20', bg=buttons_bg_color,
                           command=close_code_frame)
        back_bttn.place(x=main_window.calc_size(5), y=main_window.calc_size(5))

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
            re_pass_error_title.place_forget()
            if password1 != password2:
                re_pass_error_title.configure(text="The passwords don't match")
                re_pass_error_title.place(x=main_window.calc_size(305), y=main_window.calc_size(338),
                                          width=main_window.calc_size(610), anchor=CENTER)

        # enter reset code
        Label(enter_code_frame, text='Reset Code:',
              font=('Eras Bold ITC', main_window.calc_size(20), 'bold'), fg='gray20',
              bg='white').place(x=main_window.calc_size(305), y=main_window.calc_size(20),
                                width=main_window.calc_size(300), anchor=CENTER)
        enter_reset_code = Entry(enter_code_frame, font=('Eras Bold ITC', main_window.calc_size(15)),
                                 fg='gray20',
                                 bg='white', justify='center')
        enter_reset_code.place(x=main_window.calc_size(305), y=main_window.calc_size(57),
                               width=main_window.calc_size(300), height=main_window.calc_size(35), anchor=CENTER)

        # enter email
        Label(enter_code_frame, text='Email:',
              font=('Eras Bold ITC', main_window.calc_size(20), 'bold'), fg='gray20',
              bg='white').place(x=main_window.calc_size(255),
                                y=main_window.calc_size(85))
        enter_email = Entry(enter_code_frame, font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20',
                            bg='white', justify='center')
        enter_email.place(x=main_window.calc_size(55), y=main_window.calc_size(122),
                          width=main_window.calc_size(500),
                          height=main_window.calc_size(35))

        # enter password
        Label(enter_code_frame, text='New Password:',
              font=('Eras Bold ITC', main_window.calc_size(20), 'bold'), fg='gray20',
              bg='white').place(x=main_window.calc_size(165), y=main_window.calc_size(167),
                                width=main_window.calc_size(300))
        enter_password = Entry(enter_code_frame, font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20',
                               bg='white', justify='center', show="•")
        enter_password.place(x=main_window.calc_size(55), y=main_window.calc_size(204),
                             width=main_window.calc_size(500),
                             height=main_window.calc_size(35))

        enter_password.bind("<Key>", key_entered)

        show_hide_button1 = Button(enter_code_frame, image=show_icon, cursor='hand2', bg=buttons_bg_color,
                                   command=show_hide_pass1)
        show_hide_button1.place(x=main_window.calc_size(555), y=main_window.calc_size(204),
                                width=main_window.calc_size(35),
                                height=main_window.calc_size(35))

        # re-enter password
        Label(enter_code_frame, text='Retype New Password:',
              font=('Eras Bold ITC', main_window.calc_size(20), 'bold'), fg='gray20',
              bg='white').place(x=main_window.calc_size(140),
                                y=main_window.calc_size(254))
        re_enter_password = Entry(enter_code_frame, font=('Eras Bold ITC', main_window.calc_size(15)),
                                  fg='gray20', bg='white', justify='center', show="•")
        re_enter_password.place(x=main_window.calc_size(55), y=main_window.calc_size(291),
                                width=main_window.calc_size(500),
                                height=main_window.calc_size(35))

        re_enter_password.bind("<Key>", key_entered)

        show_hide_button2 = Button(enter_code_frame, image=show_icon, cursor='hand2', bg=buttons_bg_color,
                                   command=show_hide_pass2)
        show_hide_button2.place(x=main_window.calc_size(555), y=main_window.calc_size(291),
                                width=main_window.calc_size(35), height=main_window.calc_size(35))

        reset_code_error_title = Label(enter_code_frame, text='Please enter the code you received in the email',
                                       font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg='white')
        email_error_title = Label(enter_code_frame, text='Please enter your email',
                                  font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg='white')
        pass_error_title = Label(enter_code_frame, text='Please enter a password',
                                 font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg='white')
        re_pass_error_title = Label(enter_code_frame, text='Please Retype the password',
                                    font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg='white')

        def reset_pass():
            reset_code_error_title.place_forget()
            email_error_title.place_forget()
            pass_error_title.place_forget()
            re_pass_error_title.place_forget()

            if reset_pass_bttn['text'] == 'Reset Password':
                if enter_reset_code.get() == '' or enter_email.get() == '' or enter_password.get() == '' or re_enter_password.get() == '':
                    if enter_reset_code.get() == '':
                        reset_code_error_title.place(x=main_window.calc_size(305), y=main_window.calc_size(83),
                                                     width=main_window.calc_size(610),
                                                     height=main_window.calc_size(16), anchor=CENTER)

                    if enter_email.get() == '':
                        email_error_title.configure(text='Please enter your email')
                        email_error_title.place(x=main_window.calc_size(305), y=main_window.calc_size(167),
                                                width=main_window.calc_size(610), height=main_window.calc_size(16),
                                                anchor=CENTER)

                    if enter_password.get() == '':
                        pass_error_title.place(x=main_window.calc_size(305), y=main_window.calc_size(252),
                                               width=main_window.calc_size(610), anchor=CENTER)

                    if re_enter_password.get() == '':
                        re_pass_error_title.configure(text='Please Retype the password')
                        re_pass_error_title.place(x=main_window.calc_size(305), y=main_window.calc_size(338),
                                                  width=main_window.calc_size(610), anchor=CENTER)

                elif enter_password.get() != re_enter_password.get():
                    # check if the two passwords aren't the same
                    re_pass_error_title.configure(text="The passwords don't match")
                    re_pass_error_title.place(x=main_window.calc_size(305), y=main_window.calc_size(338),
                                              width=main_window.calc_size(610), anchor=CENTER)
                elif not manageSERVER.check_if_email_exists(enter_email.get()):
                    # check if email doesn't exist
                    email_error_title.configure(text="This email address doesn't has an account")
                    email_error_title.place(x=main_window.calc_size(305), y=main_window.calc_size(167),
                                            width=main_window.calc_size(610), height=main_window.calc_size(8),
                                            anchor=CENTER)
                else:
                    email = enter_email.get()
                    reset_code = enter_reset_code.get()
                    new_password = enter_password.get()
                    if not manageSERVER.reset_password(email, reset_code, new_password):
                        re_pass_error_title.configure(
                            text='Some Information is incorrect! Please make sure the code and your email are correct and try again',
                            fg='red')
                        re_pass_error_title.place(x=main_window.calc_size(305), y=main_window.calc_size(338),
                                                  width=main_window.calc_size(610), anchor=CENTER)
                    else:
                        enter_reset_code.configure(text='')
                        enter_email.configure(text='')
                        enter_password.configure(text='')
                        re_enter_password.configure(text='')

                        re_pass_error_title.configure(text='Your password was reset successfully!', fg='green')
                        re_pass_error_title.place(x=main_window.calc_size(305), y=main_window.calc_size(338),
                                                  width=main_window.calc_size(610), anchor=CENTER)
                        reset_pass_bttn.configure(text='Go to Log in')
            elif reset_pass_bttn['text'] == 'Go to Log in':
                main_title.destroy()
                reset_frame.destroy()
                play_video(mid_video_name)
                start_login_window(main_frame)

        reset_pass_bttn = Button(enter_code_frame, text='Reset Password', cursor='hand2',
                                 font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20',
                                 bg=buttons_bg_color, command=reset_pass)
        reset_pass_bttn.place(x=main_window.calc_size(218), y=main_window.calc_size(352),
                              width=main_window.calc_size(174), height=main_window.calc_size(35))
        enter_reset_code.focus()

    reset_frame = Frame(main_frame, bg='white')
    reset_frame.place(x=main_window.calc_size(231), y=main_window.calc_size(133), width=main_window.calc_size(610),
                      height=main_window.calc_size(392))  # (x=231, y=133, width=610, height=392)

    email_error_title = Label(reset_frame, text='Please enter your email',
                              font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg='white')

    email_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(205),
                            width=main_window.calc_size(500))  # (x=55, y=205, width=500)
    email_error_title.place_forget()

    main_title = Label(main_frame, text='Remote File Explorer - Reset Password',
                       font=('Eras Bold ITC', main_window.calc_size(35), 'bold'), fg='gray20',
                       bg=label_bg_color)
    main_title.place(x=main_window.calc_size(59), y=main_window.calc_size(25))

    # enter email
    Label(reset_frame, text='Email:', font=('Eras Bold ITC', main_window.calc_size(20), 'bold'),
          fg='gray20', bg='white').place(x=main_window.calc_size(255),
                                         y=main_window.calc_size(130))
    enter_email = Entry(reset_frame, font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20', bg='white',
                        justify='center')
    enter_email.place(x=main_window.calc_size(55), y=main_window.calc_size(170), width=main_window.calc_size(500),
                      height=main_window.calc_size(35))

    # go to enter code screen (button)
    Label(reset_frame, text='already got a code?', font=('Eras Bold ITC', main_window.calc_size(12)), fg='gray20',
          bg='white').place(x=main_window.calc_size(125), y=main_window.calc_size(15))
    enter_reset_code_bttn = Button(reset_frame, text='Enter reset code', cursor='hand2',
                                   font=('Eras Bold ITC', main_window.calc_size(12)), fg='gray20', bg=buttons_bg_color,
                                   command=new_pass_code)
    enter_reset_code_bttn.place(x=main_window.calc_size(310), y=main_window.calc_size(10),
                                width=main_window.calc_size(150), height=main_window.calc_size(35))

    send_email_button = Button(reset_frame, text='Send Email', cursor='hand2',
                               font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20', bg=buttons_bg_color,
                               command=submit)
    send_email_button.place(x=main_window.calc_size(235), y=main_window.calc_size(270),
                            width=main_window.calc_size(140), height=main_window.calc_size(35))

    login_button = Button(reset_frame, text="Login to your account", cursor='hand2', bd=0,
                          font=('Eras Bold ITC', main_window.calc_size(10)), fg='gray20', bg=buttons_bg_color,
                          command=login)
    login_button.place(x=main_window.calc_size(228), y=main_window.calc_size(350))

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
        if video_name == f'{ROOT_PROJ_DIR}/assets/mid-animation.mp4' and count == 25:
            vid_frame.destroy()
        elif video_name == f'{ROOT_PROJ_DIR}/assets/start-animation.mp4' and count == 20:
            vid_frame.destroy()
        elif video_name == f'{ROOT_PROJ_DIR}/assets/end-animation.mp4' and count == 26:
            vid_frame.destroy()


def server_status(main_frame):
    global email
    status = manageSERVER.get_server_status()
    if status != 'SERVER IS UP':
        email = False
        error_frame = Frame(main_frame, bg='white')
        error_frame.place(x=main_window.calc_size(231), y=main_window.calc_size(133),
                          width=main_window.calc_size(610), height=main_window.calc_size(392))
        error_label = Label(error_frame, text='error', bg='white', font=('Arial', main_window.calc_size(17), 'bold'))
        if status == 'SERVER IS DOWN':
            error_label.configure(
                text='The server is currently DOWN!\n(You may also want to check your internet connection)\nPlease try again later.')
        elif status == 'ERROR':
            error_label.configure(text='There was an error connecting to the server!\nPlease try again later.')
        error_label.place(x=main_window.calc_size(305), y=main_window.calc_size(170),
                          width=main_window.calc_size(610), anchor=CENTER)
        error_frame.mainloop()


def choose_mode_window(email):
    global ssh, sftp, username, answr, host
    answr = None
    host = None

    def create_popup_window(mode, title, label_text, msg_box_text, approve_text):
        global answr
        popup_width = main_window.calc_size(400)
        popup_height = main_window.calc_size(200)
        popup_x = int((screen_width - popup_width) / 2)
        popup_y = int((screen_height - popup_height) / 2)

        def submit():
            global answr
            pass_error_title.place_forget()
            password = enter_password.get()
            if password == '':
                if password == '':
                    pass_error_title.configure(text='Please enter your password')
                    pass_error_title.place(x=main_window.calc_size(0), y=main_window.calc_size(120),
                                           width=main_window.calc_size(400))
            elif not manageSERVER.check_if_email_exists(email):
                # check if email doesn't exist
                pass_error_title.configure(text="This email address doesn't have an account")
                pass_error_title.place(x=main_window.calc_size(0), y=main_window.calc_size(120),
                                       width=main_window.calc_size(400))
            elif not manageSERVER.login(email, password, 0):
                # check if the password doesn't match the email
                pass_error_title.configure(text='Password is incorrect, Try again')
                pass_error_title.place(x=main_window.calc_size(0), y=main_window.calc_size(120),
                                       width=main_window.calc_size(400))
            else:
                # email exists and the password matches
                pass_error_title.place_forget()
                msg_box = messagebox.askquestion(title=title, message=f'{msg_box_text}\nThis action is not reversible!')
                if msg_box == 'yes':
                    if title == 'Reset saved IP list in your account':
                        if manageSERVER.reset_ip_dict(email, password):
                            answr = True
                            messagebox.showinfo(title=title, message=approve_text)
                            popup.quit()
                        else:
                            answr = False
                            messagebox.showerror(title='Error', message="An error occurred")
                            popup.quit()

                    elif title == 'Permanently delete your account':
                        if manageSERVER.delete_account(email, password):
                            answr = True
                            messagebox.showinfo(title=title, message=approve_text)
                            popup.quit()
                        else:
                            answr = False
                            messagebox.showerror(title='Error', message="An error occurred")
                            popup.quit()
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
        popup.iconbitmap('assets/icon.ico')
        popup.resizable(False, False)
        popup.title(title)

        def enter_key(event):
            confirm_button.invoke()

        popup.bind('<Return>', enter_key)

        pass_error_title = Label(popup, text='Please enter your password',
                                 font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg=label_bg_color)
        pass_error_title.place(x=main_window.calc_size(0), y=main_window.calc_size(120),
                               width=main_window.calc_size(400))
        pass_error_title.place_forget()

        Label(popup, text=label_text, wraplength=popup_width, bg=label_bg_color,
              font=('Eras Bold ITC', main_window.calc_size(12))).place(x=main_window.calc_size(0),
                                                                       y=main_window.calc_size(5),
                                                                       width=main_window.calc_size(400))
        Label(popup, text=f'{email}', wraplength=popup_width, bg=label_bg_color,
              font=('Eras Bold ITC', main_window.calc_size(15))).place(x=main_window.calc_size(0),
                                                                       y=main_window.calc_size(50),
                                                                       width=main_window.calc_size(400))
        enter_password = Entry(popup, font=('Eras Bold ITC', main_window.calc_size(15)), bg='white', justify='center',
                               show='•')
        enter_password.place(x=main_window.calc_size(32), y=main_window.calc_size(85),
                             width=main_window.calc_size(300), height=main_window.calc_size(35))
        show_hide_button = Button(popup, image=show_icon, cursor='hand2', bg=buttons_bg_color, command=show_hide_pass)
        show_hide_button.place(x=main_window.calc_size(333), y=main_window.calc_size(85),
                               width=main_window.calc_size(35), height=main_window.calc_size(35))

        confirm_button = Button(popup, text='Confirm', cursor='hand2',
                                font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20', bg=buttons_bg_color,
                                command=submit)
        confirm_button.place(x=main_window.calc_size(150), y=main_window.calc_size(145),
                             width=main_window.calc_size(100), height=main_window.calc_size(32))
        enter_password.focus()
        popup.mainloop()

    def change_password():
        popup_width = main_window.calc_size(610)
        popup_height = main_window.calc_size(392)
        popup_x = int((screen_width - popup_width) / 2)
        popup_y = int((screen_height - popup_height) / 2)

        def submit():
            global email
            cur_pass_error_title.place_forget()
            pass_error_title.place_forget()
            re_pass_error_title.place_forget()
            if enter_cur_password.get() == '' or enter_password.get() == '' or re_enter_password.get() == '':
                if enter_cur_password.get() == '':
                    cur_pass_error_title.configure(text='Please enter your current password')
                    cur_pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(85),
                                               width=main_window.calc_size(500))
                if enter_password.get() == '':
                    pass_error_title.configure(text='Please enter a new password')
                    pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(180),
                                           width=main_window.calc_size(500))
                if re_enter_password.get() == '':
                    re_pass_error_title.configure(text='Please Retype the new password')
                    re_pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(275),
                                              width=main_window.calc_size(500))
            elif not manageSERVER.check_if_email_exists(email):
                # check if email exists
                messagebox.showerror(title='Error', message="This email address doesn't have an account")
                root.destroy()
                main_window.main()
            elif enter_password.get() != re_enter_password.get():
                # check if the two passwords aren't the same
                re_pass_error_title.configure(text="The passwords don't match")
                re_pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(275),
                                          width=main_window.calc_size(500))
            elif not manageSERVER.login(email, enter_cur_password.get(), 0):
                cur_pass_error_title.configure(text='The password is incorrect, Try again')
                cur_pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(85),
                                           width=main_window.calc_size(500))
            elif enter_cur_password.get() == enter_password.get():
                # check if the new password is not the same as the current one
                re_pass_error_title.configure(
                    text="The new password can't be the same as the current one,\nPlease choose a new password")
                re_pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(275),
                                          width=main_window.calc_size(500))

            else:
                password = enter_cur_password.get()
                new_password = enter_password.get()
                change_pass_answr = manageSERVER.change_password(email, password, new_password)
                if change_pass_answr == True:
                    messagebox.showinfo(title='Password changed',
                                        message=f'Password changed successfully, a confirmation email was sent to: {email}')
                    popup.destroy()
                elif change_pass_answr == 'EMAIL NOT SENT':
                    messagebox.showinfo(title='Password changed',
                                        message=f'Password changed, but we were unable to send an email to the address: {email}')
                    popup.destroy()
                elif not change_pass_answr:
                    messagebox.showerror(title='Error', message="An error occurred")
                    root.destroy()
                    main_window.main()

        def show_hide_pass1():
            if enter_cur_password.cget('show') == '':
                enter_cur_password.configure(show='•')
                show_hide_button1.configure(image=show_icon)
            else:
                enter_cur_password.configure(show='')
                show_hide_button1.configure(image=hide_icon)

        def show_hide_pass2():
            if enter_password.cget('show') == '':
                enter_password.configure(show='•')
                show_hide_button2.configure(image=show_icon)
            else:
                enter_password.configure(show='')
                show_hide_button2.configure(image=hide_icon)

        def show_hide_pass3():
            if re_enter_password.cget('show') == '':
                re_enter_password.configure(show='•')
                show_hide_button3.configure(image=show_icon)
            else:
                re_enter_password.configure(show='')
                show_hide_button3.configure(image=hide_icon)

        def key_entered(key):
            password1 = enter_password.get()
            password2 = re_enter_password.get()
            if len(password1) > len(password2):
                password2 = re_enter_password.get() + key.char
            else:
                password1 = enter_password.get() + key.char
            re_pass_error_title.place_forget()
            if password1 != password2:
                re_pass_error_title.configure(text="The passwords don't match")
                re_pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(275),
                                          width=main_window.calc_size(500))

        popup = Toplevel(bg=label_bg_color)
        popup.geometry(f'{popup_width}x{popup_height}+{popup_x}+{popup_y}')
        popup.iconbitmap('assets/icon.ico')
        popup.resizable(False, False)
        popup.title('Change Password')

        def enter_key(event):
            confirm_button.invoke()

        popup.bind('<Return>', enter_key)

        cur_pass_error_title = Label(popup, text='Please enter your current password',
                                     font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg=label_bg_color)
        pass_error_title = Label(popup, text='Please enter a new password',
                                 font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg=label_bg_color)
        pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(180),
                               width=main_window.calc_size(500))
        re_pass_error_title = Label(popup, text='Please Retype the new password',
                                    font=('Eras Bold ITC', main_window.calc_size(10)), fg='red', bg=label_bg_color)
        re_pass_error_title.place(x=main_window.calc_size(55), y=main_window.calc_size(275),
                                  width=main_window.calc_size(500))
        cur_pass_error_title.place_forget()
        pass_error_title.place_forget()
        re_pass_error_title.place_forget()

        Label(popup, text=f"{email}\nCurrent Password:",
              font=('Eras Bold ITC', main_window.calc_size(15), 'bold'), fg='gray20',
              bg=label_bg_color).place(x=main_window.calc_size(0),
                                       y=main_window.calc_size(0), width=main_window.calc_size(610))
        enter_cur_password = Entry(popup, font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20',
                                   bg='white', justify='center', show="•")
        enter_cur_password.place(x=main_window.calc_size(55), y=main_window.calc_size(50),
                                 width=main_window.calc_size(500), height=main_window.calc_size(35))

        show_hide_button1 = Button(popup, image=show_icon, cursor='hand2', bg=buttons_bg_color,
                                   command=show_hide_pass1)
        show_hide_button1.place(x=main_window.calc_size(555), y=main_window.calc_size(50),
                                width=main_window.calc_size(35),
                                height=main_window.calc_size(35))

        Label(popup, text='New Password:',
              font=('Eras Bold ITC', main_window.calc_size(15), 'bold'), fg='gray20',
              bg=label_bg_color).place(x=main_window.calc_size(0),
                                       y=main_window.calc_size(110), width=main_window.calc_size(610))
        enter_password = Entry(popup, font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20',
                               bg='white', justify='center', show="•")
        enter_password.place(x=main_window.calc_size(55), y=main_window.calc_size(145),
                             width=main_window.calc_size(500),
                             height=main_window.calc_size(35))

        enter_password.bind("<Key>", key_entered)

        show_hide_button2 = Button(popup, image=show_icon, cursor='hand2', bg=buttons_bg_color,
                                   command=show_hide_pass2)
        show_hide_button2.place(x=main_window.calc_size(555), y=main_window.calc_size(145),
                                width=main_window.calc_size(35),
                                height=main_window.calc_size(35))

        Label(popup, text='Retype New Password:',
              font=('Eras Bold ITC', main_window.calc_size(15), 'bold'), fg='gray20',
              bg=label_bg_color).place(x=main_window.calc_size(0),
                                       y=main_window.calc_size(205), width=main_window.calc_size(610))
        re_enter_password = Entry(popup, font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20',
                                  bg='white', justify='center', show="•")
        re_enter_password.place(x=main_window.calc_size(55), y=main_window.calc_size(240),
                                width=main_window.calc_size(500),
                                height=main_window.calc_size(35))

        re_enter_password.bind("<Key>", key_entered)

        show_hide_button3 = Button(popup, image=show_icon, cursor='hand2', bg=buttons_bg_color,
                                   command=show_hide_pass3)
        show_hide_button3.place(x=main_window.calc_size(555), y=main_window.calc_size(240),
                                width=main_window.calc_size(35),
                                height=main_window.calc_size(35))

        confirm_button = Button(popup, text='Confirm', cursor='hand2',
                                font=('Eras Bold ITC', main_window.calc_size(15)), fg='gray20', bg=buttons_bg_color,
                                command=submit)
        confirm_button.place(x=main_window.calc_size(255), y=main_window.calc_size(315),
                             width=main_window.calc_size(100), height=main_window.calc_size(35))

        enter_cur_password.focus()
        popup.mainloop()

    def reset_ip_list():
        global answr
        create_popup_window(0, 'Reset saved IP list in your account',
                            "Enter your account's password to delete all the saved IPs in your account:",
                            f'Are you sure you want to delete all the IPs saved to your account: {email}?',
                            'IP list reset successfully')
        if answr:
            root.destroy()
            main_window.main()

    def delete_account():
        global answr
        create_popup_window(0, 'Permanently delete your account',
                            "Enter your account's password to permanently delete it:",
                            f'Are you sure you want to permanently delete your account: {email}?',
                            'Account deleted successfully')
        if answr:
            root.destroy()
            main_window.main()

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
            settings_menu.add_command(label='Change your password', command=change_password,
                                      activebackground='steelblue2', activeforeground='black')
            settings_menu.add_command(label='Reset saved IP list in your account', command=reset_ip_list,
                                      activebackground='steelblue2', activeforeground='black')
            settings_menu.add_command(label='Permanently delete your account', command=delete_account,
                                      activebackground='steelblue2', activeforeground='black')
            account.add_cascade(label='Account Settings', menu=settings_menu, activebackground='steelblue2',
                                activeforeground='black')

            account.add_separator()
            account.add_command(label='Sign Out', command=acc_signout, activebackground='steelblue2',
                                activeforeground='black')
            root.title('Remote File Explorer')
            choose_frame = Frame(root)
            choose_frame.place(x=0, y=0, width=app_width, height=app_height)
            bg = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}/assets/background.png').resize((app_width, app_height), Image.ANTIALIAS))
            Label(choose_frame, image=bg).place(x=0, y=0, relwidth=1, relheight=1)  # background image
            control_pic = ImageTk.PhotoImage(
                Image.open(f'{ROOT_PROJ_DIR}/assets/control-pic.png').resize((main_window.calc_size(160), main_window.calc_size(160)),
                                                                             Image.ANTIALIAS))
            be_controlled_pic = ImageTk.PhotoImage(
                Image.open(f'{ROOT_PROJ_DIR}/assets/be-controlled-pic.png').resize((main_window.calc_size(200), main_window.calc_size(160)),
                                                                                   Image.ANTIALIAS))
            mode = choose_mode(choose_frame, control_pic, be_controlled_pic)
            try:
                choose_frame.destroy()
            except:
                pass

    ssh = None
    sftp = None
    username = None
    if mode == 'control' and email != None:
        root.title('Remote File Explorer')
        ip_frame = Frame(root)
        ip_frame.place(x=0, y=0, width=app_width, height=app_height)
        bg = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}/assets/background.png').resize((app_width, app_height), Image.ANTIALIAS))
        Label(ip_frame, image=bg).place(x=0, y=0, relwidth=1, relheight=1)  # background image
        ssh, sftp, username = login_to_ssh_client(ip_frame, ip_dict)

    elif mode == 'be_controlled' and email != None:
        root.title('Remote File Explorer')
        be_controlled_frame = Frame(root)
        be_controlled_frame.place(x=0, y=0, width=app_width, height=app_height)
        bg = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}/assets/background.png').resize((app_width, app_height), Image.ANTIALIAS))
        Label(be_controlled_frame, image=bg).place(x=0, y=0, relwidth=1, relheight=1)  # background image
        set_be_controlled(be_controlled_frame)

    if email != None and mode != None and ssh != None:
        back_frame = Frame(root, bg=label_bg_color)
        back_frame.place(x=0, y=0, width=app_width, height=app_height)

    return email, mode, ssh, sftp, username, host


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

    if email == None:
        main_frame = Frame(root)
        main_frame.place(x=0, y=0, width=app_width, height=app_height)

        server_status(main_frame)
        if email == False:
            return None, None, None, None, None, None
        bg = ImageTk.PhotoImage(
            Image.open(f'{ROOT_PROJ_DIR}/assets/background.png').resize((app_width, app_height), Image.ANTIALIAS))
        Label(main_frame, image=bg).place(x=0, y=0, relwidth=1, relheight=1)  # background image
        show_icon = ImageTk.PhotoImage(
            Image.open(f'{ROOT_PROJ_DIR}/assets/show.png').resize(
                (main_window.calc_size(30), main_window.calc_size(30)),
                Image.ANTIALIAS))
        hide_icon = ImageTk.PhotoImage(
            Image.open(f'{ROOT_PROJ_DIR}/assets/hide.png').resize(
                (main_window.calc_size(30), main_window.calc_size(30)),
                Image.ANTIALIAS))

        play_video(start_video_name)
        start_login_window(main_frame)
        main_frame.mainloop()

    return choose_mode_window(email)
