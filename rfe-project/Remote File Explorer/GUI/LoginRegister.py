import threading
import tkinter
from tkinter import messagebox, ttk
import imageio
import wx
import re
from PIL import ImageTk, Image
import os
import socket
import manageSERVER
from time import sleep


lable_bg_color = '#e9eed6'
buttons_bg_color = '#d9dcc7'
start_video_name = 'start-animation.mp4'
mid_video_name = 'mid-animation.mp4'
end_video_name = 'end-animation.mp4'
ROOT_PROJ_DIR = os.path.dirname(os.path.abspath(__file__))

def email_regex(email):
    regex = r"""^[a-zA-Z]+(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    if re.match(regex, email):
        return True
    else:
        return False

def choose_is_control(choose_frame, control_pic, be_controlled_pic):#, old_frame):
    global mode, root
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
    main_title = tkinter.Label(choose_frame, text='Remote File Explorer', font=('Eras Bold ITC', 35, 'bold'), fg='gray20', bg=lable_bg_color)  # fg='goldenrod2'
    main_title.place(x=270, y=25)
    frame = tkinter.Frame(choose_frame, bg='white')
    frame.place(x=229, y=132, width=610, height=392)
    choose_label = tkinter.Label(frame, text='Choose an action for this PC:', font=('Eras Bold ITC', 25, 'bold underline'), fg='gray20', bg='white')
    choose_label.place(x=55, y=25)
    control_button = tkinter.Button(frame, cursor='hand2', command=control_bttn, image=control_pic, bd=0, bg='white')  # bg=buttons_bg_color)
    # control_button.place(x=100, y=140)
    control_button.place(x=70, y=142)
    control_label = tkinter.Label(frame, text='CONTROL', font=('Eras Bold ITC', 20, 'bold'), fg='gray20', bg='white')
    control_label.place(x=75, y=100)
    be_controlled_button = tkinter.Button(frame, cursor='hand2', command=be_controlled_bttn, image=be_controlled_pic, bd=0, bg='white')  # bg=buttons_bg_color)
    # be_controlled_button.place(x=350, y=140)
    be_controlled_button.place(x=360, y=140)
    control_label = tkinter.Label(frame, text='BE CONTROLLED', font=('Eras Bold ITC', 20, 'bold'), fg='gray20', bg='white')
    control_label.place(x=320, y=100)

    choose_frame.mainloop()
    return mode

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
        global email
        email_error_title.place_forget()
        pass_error_title.place_forget()
        # while True:
        #  add notification if server is down
        if enter_email.get() == '' or enter_password.get() == '':
            if enter_email.get() == '':
                email_error_title.configure(text='Please enter your email')
                email_error_title.place(x=55, y=110, width=500)
            if enter_password.get() == '':
                pass_error_title.place(x=55, y=215, width=500)
            # break
        elif manageSERVER.check_if_email_exists(enter_email.get()) == False:  # check if email doesn't exist in the DB
            email_error_title.configure(text="This email address doesn't have an account")
            email_error_title.place(x=55, y=110, width=500)
            # break
        elif manageSERVER.login(enter_email.get(), enter_password.get(), check_var.get()) == False:  # check if password doesn't match the email
            pass_error_title.configure(text='Email or Password are incorrect, Try again')
            pass_error_title.place(x=55, y=215, width=500)
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

    login_frame = tkinter.Frame(main_frame, bg='white')
    login_frame.place(x=229, y=132, width=610, height=392)

    email_error_title = tkinter.Label(login_frame, text='Please enter your email', font=('Eras Bold ITC', 10), fg='red', bg='white')
    email_error_title.place(x=55, y=110, width=500)
    pass_error_title = tkinter.Label(login_frame, text='Please enter your password', font=('Eras Bold ITC', 10), fg='red', bg='white')
    pass_error_title.place(x=55, y=215, width=500)
    email_error_title.place_forget()
    pass_error_title.place_forget()

    main_title = tkinter.Label(main_frame, text='Remote File Explorer - Login', font=('Eras Bold ITC', 35, 'bold'), fg='gray20', bg=lable_bg_color)  # fg='goldenrod2'
    main_title.place(x=180, y=25)

    email_title = tkinter.Label(login_frame, text='Email:', font=('Eras Bold ITC', 20, 'bold'), fg='gray20', bg='white').place(x=255, y=35)
    enter_email = tkinter.Entry(login_frame, font=('Eras Bold ITC', 15), fg='gray20', bg='white', justify='center')
    enter_email.place(x=55, y=75, width=500, height=35)

    password_title = tkinter.Label(login_frame, text='Password:', font=('Eras Bold ITC', 20, 'bold'), fg='gray20', bg='white').place(x=225, y=140)
    enter_password = tkinter.Entry(login_frame, font=('Eras Bold ITC', 15), fg='gray20', bg='white', justify='center', show='•')
    enter_password.place(x=55, y=180, width=500, height=35)

    show_hide_button = tkinter.Button(login_frame, image=show_icon, cursor='hand2', bg=buttons_bg_color, command=show_hide_pass)
    show_hide_button.place(x=555, y=180, width=35, height=35)

    check_var = tkinter.IntVar(value=1)
    save_to_acc = tkinter.Checkbutton(login_frame, cursor='hand2',
                                      text="Save this PC's info to your account for future connections", fg='gray20',
                                      bg=buttons_bg_color, font=('Eras Bold ITC', 10), onvalue=1, offvalue=0, variable=check_var)
    save_to_acc.place(x=105, y=245)

    login_button = tkinter.Button(login_frame, text='Login', cursor='arrow', font=('Eras Bold ITC', 15), fg='gray20', bg=buttons_bg_color, command=submit)
    login_button.place(x=255, y=292, width=100, height=35)

    register_button = tkinter.Button(login_frame, text="Create a new account", cursor='hand2', bd=0, font=('Eras Bold ITC', 10), fg='gray20', bg=buttons_bg_color, command=register)
    register_button.place(x=130, y=350)

    sep_line = ttk.Separator(login_frame, orient=tkinter.VERTICAL)
    sep_line.place(x=302, y=342, width=1, height=40)

    forgot_button = tkinter.Button(login_frame, text='Reset your password', cursor='hand2', bd=0, font=('Eras Bold ITC', 10), fg='gray20', bg=buttons_bg_color, command=forgot_pass)
    # forgot_button.place(x=320, y=350)

    # main_frame.mainloop()
    # return email

    forgot_button.place(x=320, y=350)

def start_register_window(main_frame):
    global email, ip_dict, root
    email = None
    ip_dict = None

    def return_button(event):
        register_button.invoke()
    root.bind('<Return>', return_button)

    root.title('Remote File Explorer - Register')
    def submit():
        global email
        email_error_title.place_forget()
        pass_error_title.place_forget()
        re_pass_error_title.place_forget()
        # while True:
        if enter_email.get() == '' or enter_password.get() == '' or re_enter_password.get() == '' or not email_regex(enter_email.get()):
            if enter_email.get() == '':
                email_error_title.configure(text='Please enter your email')
                email_error_title.place(x=55, y=85, width=500)
            if enter_password.get() == '':
                pass_error_title.place(x=55, y=180, width=500)
            if re_enter_password.get() == '':
                re_pass_error_title.configure(text='Please Retype the password')
                re_pass_error_title.place(x=55, y=275, width=500)
            if not email_regex(enter_email.get()) and enter_email.get() != '':  # check if email is invalid
                email_error_title.configure(text='Please enter a valid email address')
                email_error_title.place(x=55, y=85, width=500)
            # break
        elif enter_password.get() != re_enter_password.get():  # check if the two passwords aren't the same
            re_pass_error_title.configure(text="The passwords don't match")
            re_pass_error_title.place(x=55, y=275, width=500)
            # break
        elif manageSERVER.check_if_email_exists(enter_email.get()):  # check if email exists already
            email_error_title.configure(text='This email address already has an account')
            email_error_title.place(x=55, y=85, width=500)
            # break
        else:
            email = enter_email.get()
            password = enter_password.get()
            # ip_dict = dict()  # maybe add a tic box as well
            manageSERVER.create_new_user(email, password)
            ip_dict = manageSERVER.get_ip_dict(email)
            # is_control = choose_is_control(root, register_frame)
            register_frame.destroy()
            main_frame.quit()
            # break

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

    register_frame = tkinter.Frame(main_frame, bg='white')
    register_frame.place(x=229, y=132, width=610, height=392)

    email_error_title = tkinter.Label(register_frame, text='Please enter your email', font=('Eras Bold ITC', 10), fg='red', bg='white')
    email_error_title.place(x=55, y=85, width=500)
    pass_error_title = tkinter.Label(register_frame, text='Please enter a password', font=('Eras Bold ITC', 10), fg='red', bg='white')
    pass_error_title.place(x=55, y=180, width=500)
    re_pass_error_title = tkinter.Label(register_frame, text='Please Retype the password', font=('Eras Bold ITC', 10), fg='red', bg='white')
    re_pass_error_title.place(x=55, y=275, width=500)
    email_error_title.place_forget()
    pass_error_title.place_forget()
    re_pass_error_title.place_forget()

    main_title = tkinter.Label(root, text='Remote File Explorer - Register', font=('Eras Bold ITC', 35, 'bold'), fg='gray20', bg=lable_bg_color)  # fg='goldenrod2'
    main_title.place(x=150, y=25)

    email_title = tkinter.Label(register_frame, text='Email:', font=('Eras Bold ITC', 20, 'bold'), fg='gray20', bg='white').place(x=255, y=10)
    enter_email = tkinter.Entry(register_frame, font=('Eras Bold ITC', 15), fg='gray20', bg='white', justify='center')
    enter_email.place(x=55, y=50, width=500, height=35)

    password_title = tkinter.Label(register_frame, text='Password:', font=('Eras Bold ITC', 20, 'bold'), fg='gray20', bg='white').place(x=225, y=105)
    enter_password = tkinter.Entry(register_frame, font=('Eras Bold ITC', 15), fg='gray20', bg='white', justify='center', show="•")
    enter_password.place(x=55, y=145, width=500, height=35)

    show_hide_button1 = tkinter.Button(register_frame, image=show_icon, cursor='hand2', bg=buttons_bg_color, command=show_hide_pass1)
    show_hide_button1.place(x=555, y=145, width=35, height=35)

    re_password_title = tkinter.Label(register_frame, text='Retype Password:', font=('Eras Bold ITC', 20, 'bold'), fg='gray20', bg='white').place(x=180, y=200)
    re_enter_password = tkinter.Entry(register_frame, font=('Eras Bold ITC', 15), fg='gray20', bg='white', justify='center', show="•")
    re_enter_password.place(x=55, y=240, width=500, height=35)

    show_hide_button2 = tkinter.Button(register_frame, image=show_icon, cursor='hand2', bg=buttons_bg_color, command=show_hide_pass2)
    show_hide_button2.place(x=555, y=240, width=35, height=35)

    register_button = tkinter.Button(register_frame, text='Register', cursor='hand2', font=('Eras Bold ITC', 15), fg='gray20', bg=buttons_bg_color, command=submit)
    register_button.place(x=255, y=300, width=100, height=35)

    login_button = tkinter.Button(register_frame, text="Login to your account", cursor='hand2', bd=0, font=('Eras Bold ITC', 10), fg='gray20', bg=buttons_bg_color, command=login)
    # login_button.place(x=227, y=350)

    # main_frame.mainloop()
    # return email

    login_button.place(x=227, y=350)

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
            email_error_title.place(x=55, y=205, width=500)
            # break
        elif manageSERVER.check_if_email_exists(enter_email.get()) == False:  # check if email doesn't exist
            email_error_title.configure(text="This email address doesn't have an account", fg='red')
            email_error_title.place(x=55, y=205, width=500)
            # break
        else:  # email exists
            email = enter_email.get()
            email_error_title.configure(text='Email Sent! Check your inbox', fg='green')
            email_error_title.place(x=55, y=205, width=500)
            # sleep(2)
            login()

            # send reset email
            # main_frame.destroy()
            # break

    def login():
        main_title.destroy()
        reset_frame.destroy()
        play_video(mid_video_name)
        start_login_window(main_frame)

    reset_frame = tkinter.Frame(main_frame, bg='white')
    reset_frame.place(x=229, y=132, width=610, height=392)

    email_error_title = tkinter.Label(reset_frame, text='Please enter your email', font=('Eras Bold ITC', 10), fg='red', bg='white')
    email_error_title.place(x=55, y=205, width=500)
    email_error_title.place_forget()

    main_title = tkinter.Label(main_frame, text='Remote File Explorer - Reset Password', font=('Eras Bold ITC', 35, 'bold'), fg='gray20', bg=lable_bg_color)  # fg='goldenrod2'
    main_title.place(x=59, y=25)

    email_title = tkinter.Label(reset_frame, text='Email:', font=('Eras Bold ITC', 20, 'bold'), fg='gray20', bg='white').place(x=255, y=130)
    enter_email = tkinter.Entry(reset_frame, font=('Eras Bold ITC', 15), fg='gray20', bg='white', justify='center')
    enter_email.place(x=55, y=170, width=500, height=35)

    send_email_button = tkinter.Button(reset_frame, text='Send Email', cursor='hand2', font=('Eras Bold ITC', 15), fg='gray20', bg=buttons_bg_color, command=submit)
    send_email_button.place(x=235, y=270, width=140, height=35)

    login_button = tkinter.Button(reset_frame, text="Login to your account", cursor='hand2', bd=0, font=('Eras Bold ITC', 10), fg='gray20', bg=buttons_bg_color, command=login)
    # login_button.place(x=228, y=350)

    # main_frame.mainloop()
    # return email

    login_button.place(x=228, y=350)

def close_window():
    discon_msg_box = tkinter.messagebox.askquestion(title='Exit the app', message='Are you sure you want to exit the app?')
    if discon_msg_box == 'yes':
        root.destroy()

def play_video(video_name):
    global video, app_width, app_height, count
    count = 0
    video = imageio.get_reader(video_name)
    vid_frame = tkinter.Frame(root)
    vid_frame.place(x=0, y=0, width=app_width, height=app_height)
    vid_label = tkinter.Label(vid_frame)
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

def main(r):
    global main_frame, show_icon, hide_icon, mode, email, root, app_width, app_height, ip_dict
    # root = tkinter.Tk()
    root = r
    root.protocol("WM_DELETE_WINDOW", close_window)
    app = wx.App(False)
    screen_width, screen_height = wx.GetDisplaySize()

    # testing
    # app = tkinter.Toplevel()
    # app.geometry('1280x720')
    # app2 = tkinter.Toplevel()
    # app2.geometry('1070x700')

    # # screen_width = 1280
    # screen_height = 720
    # testing

    print(f'screen_width: {screen_width}')
    print(f'screen_height: {screen_height}')
    # x = int(screen_width/2 - 1200/2)
    # y = int(screen_height/2 - 700/2)
    app_width = int(screen_width / 1.794)
    app_height = int(screen_height / 1.542)
    print(f'app_width: {app_width}')
    print(f'app_height: {app_height}')
    x = int((screen_width - app_width) / 2)
    y = int((screen_height - app_height) / 2)
    root.geometry(f'{app_width}x{app_height}+{x}+{y}')
    # root.geometry(f'1070x700+{x}+{y}')
    root.iconbitmap('icon.ico')
    root.resizable(False, False)


    # good
    main_frame = tkinter.Frame(root)
    main_frame.place(x=0, y=0, width=app_width, height=app_height)

    # bg = tkinter.PhotoImage(file='background.png')
    bg = ImageTk.PhotoImage(Image.open('background.png').resize((app_width, app_height), Image.ANTIALIAS))
    bg_image = tkinter.Label(main_frame, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    show_icon = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}/show.png'))
    hide_icon = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}/hide.png'))
    play_video(start_video_name)
    # email = start_login_window(main_frame)

    start_login_window(main_frame)
    main_frame.mainloop()

    print(email)  # DELETE
    # good


    # while response == 'forgot' or response == 'login' or response == 'register':
    #     print(response)
    #     if response == 'forgot':
    #         response = start_forgot_window(root)
    #     if response == 'login':
    #         response = start_login_window(root)
    #     if response == 'register':
    #         response = start_register_window(root)

    email = 'yaniv'  # test

    mode = None
    if email != None:
        root.title('Remote File Explorer')
        choose_frame = tkinter.Frame(root)
        choose_frame.place(x=0, y=0, width=app_width, height=app_height)
        bg = ImageTk.PhotoImage(Image.open('background.png').resize((app_width, app_height), Image.ANTIALIAS))
        bg_image = tkinter.Label(choose_frame, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
        control_pic = ImageTk.PhotoImage(Image.open('control-pic.png').resize((160, 160), Image.ANTIALIAS))
        be_controlled_pic = ImageTk.PhotoImage(Image.open('be-controlled-pic.png').resize((200, 160), Image.ANTIALIAS))
        mode = choose_is_control(choose_frame, control_pic, be_controlled_pic)
        # if email == 'yaniv2':
        #     choose_frame.destroy()
        # choose_frame.mainloop()

    # if email != None:
    #     root = tkinter.Tk()
    #     root.protocol("WM_DELETE_WINDOW", close_window)
    #     root.geometry(f'{app_width}x{app_height}+{x}+{y}')
    #     root.geometry(f'1070x700+{x}+{y}')
    #     root.iconbitmap('icon.ico')
    #     root.resizable(False, False)
    #     bg = tkinter.PhotoImage(file='background.png')
    #     bg_image = tkinter.Label(root, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    #     # mode = choose_is_control(root)
    #     frame = tkinter.Frame(root, bg='black')
    #     frame.place(x=229, y=132, width=610, height=392)
    #     if email == 'yaniv2':
    #         frame.destroy()
    #     frame.mainloop()

    print(mode)
    # root.mainloop()
    # if email != None and mode != None:
    #     play_video(end_video_name)

    return email, mode, ip_dict

    # start_register_window(root)
    # start_forgot_window(root)


if __name__ == '__main__':
    root = tkinter.Tk()
    main(root)