__author__ = 'Yaniv Nash'

import manageSSH  # the file with funcs that connect to the ssh
import LoginRegister
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
import socket
import os
from PIL import ImageTk, Image
from tkinter import simpledialog  # opens the popup for the new folder name input
import pyperclip  # copy to clipboard module
import re
import wx  # get screen resolution

frame_bg_color = '#e9eed6'
buttons_bg_color = '#d9dcc7'

system_drive = os.getenv("SystemDrive")

MENU_BAR_HEIGHT = 20

app = wx.App(False)
screen_width, screen_height = wx.GetDisplaySize()

if screen_width / screen_height != (1920 / 1080):
    screen_height = screen_width / (1920 / 1080)

if screen_width >= 1070 and screen_height >= 700:
    screen_width = 1920
    screen_height = 1080

app_width = int(screen_width / 1.794)
app_height = int(screen_height / 1.542)

bttns_dict = dict()
icons_dict = dict()

ROOT_PROJ_DIR = os.getcwd()

is_searching = False
cur_path = 'C:\\'


def calc_width(size):
    if size == 0:
        return 0
    else:
        return int(app_width / (1070 / size))


def calc_height(size):
    if size == 0:
        return 0
    else:
        return int(app_height / (700 / size))


def get_icons_dict():
    icons_list = os.listdir(f'{ROOT_PROJ_DIR}\\icons')
    for icon in icons_list:
        icons_dict[icon] = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}\\icons\\{icon}'))
    return icons_dict


def create_bttn(frame):
    global icons_dict, bttns_dict, sftp, right_click_file_menu, right_click_dir_menu
    clm = 0
    rw = 2
    dirs_list, files_list = manageSSH.get_dirs_files_lists(sftp, cur_path)
    items_list = dirs_list + files_list
    for item in items_list:
        btn_text = item
        if item in dirs_list:
            # if 'item' is a dir
            file_type = '.dir_folder'
            if len(item) > 30:
                btn_text = item[0:30] + '...'
        elif item in files_list:
            # if 'item' is a file
            end_index = item.rfind('.')
            file_type = item[end_index:].lower()

            if len(item) > 30:
                btn_text = item[0:30] + '...' + file_type
        else:
            file_type = '.none'
        try:
            icon = icons_dict[file_type + '.png']
        except KeyError:
            icon = icons_dict['.none.png']
        bttns_dict[f'{item}_btn_{items_list.index(item)}'] = Button(frame, bg="gray", wraplength=100, text=btn_text,
                                                                    compound=TOP, justify=CENTER, image=icon,
                                                                    height=120, width=120)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].grid(column=clm, row=rw, sticky=N + S + E + W, padx=9,
                                                                pady=9)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind("<Button-3>", right_click)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind('<Double-Button-1>', double_click)
        clm += 1
        if clm == 7:
            clm = 0
            rw += 1


def double_click(event):
    global items_list, cur_path, frame, bttns_dict
    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    item_name = key_list[val_list.index(event.widget)]
    item_name = item_name[0:item_name.find('_btn_')]
    if cur_path.endswith('\\') or cur_path.endswith('/'):
        cur_path = cur_path[:-1]
    temp = cur_path + '\\' + item_name
    item_type = manageSSH.check_if_item_is_dir(sftp, cur_path, item_name)
    if item_type == 'dir':
        cur_path = temp
        manageSSH.chdir(sftp, cur_path)
        items_list = sftp.listdir()
        update_frame(items_list)


def download_file(event):
    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    item_name = key_list[val_list.index(event.widget)]
    file = item_name[:item_name.find('_btn_')]
    file_type = file[file.rfind('.'):]
    file_name = file[:file.rfind('.')]
    local_path = filedialog.asksaveasfilename(defaultextension=file_type, title='Choose where to save the file',
                                              initialfile=file_name, filetypes=((file_type, file_type),))
    if local_path:
        remote_path = cur_path + '\\' + file
        sftp2 = ssh.open_sftp()
        sftp2.get(remote_path, local_path)
        refresh_button()


def right_click(event):
    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    item_name = key_list[val_list.index(event.widget)]
    item_name = item_name[:item_name.find('_btn_')]
    item_type = manageSSH.check_if_item_is_dir(sftp, cur_path, item_name)

    right_click_dir_menu = Menu(root, tearoff=False)
    right_click_file_menu = Menu(root, tearoff=False)

    if item_type == 'dir':
        right_click_dir_menu.add_command(label='Open Folder', command=lambda: double_click(event))
        right_click_dir_menu.add_command(label='Rename Folder', command=lambda: rename_item(event))
        right_click_dir_menu.add_command(label='Delete Folder', command=lambda: remove_item(event))
        right_click_dir_menu.tk_popup(event.x_root, event.y_root)
    elif item_type == 'file':
        # right_click_file_menu.add_command(label='Open File', command=lambda: double_click(event))
        right_click_file_menu.add_command(label='Download File', command=lambda: download_file(event))
        right_click_file_menu.add_command(label='Rename File', command=lambda: rename_item(event))
        right_click_file_menu.add_command(label='Delete File', command=lambda: remove_item(event))
        right_click_file_menu.tk_popup(event.x_root, event.y_root)


def rename_item(event):
    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    item_name = key_list[val_list.index(event.widget)]
    item_name = item_name[0:item_name.find('_btn_')]
    item_type = manageSSH.check_if_item_is_dir(sftp, cur_path, item_name)
    old_path = cur_path + '\\' + item_name
    file_type = ''
    if item_type == 'file':
        dirs_list, files_list = manageSSH.get_dirs_files_lists(sftp, cur_path)
        items_list = dirs_list + files_list
        for _ in items_list:
            if item_name in files_list:
                end_index = item_name.rfind('.')
                file_type = item_name[end_index:]
                break

    new_name = simpledialog.askstring('Rename', f'Enter a new name for "{item_name}":')
    if new_name != None and new_name != '':
        new_name += file_type
        new_name = check_new_name(new_name, 'Rename', item_type)

        if new_name != False:
            new_path = cur_path + '\\' + new_name
            sftp2 = ssh.open_sftp()
            sftp2.rename(old_path, new_path)
            refresh_button()


def remove_item(event):
    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    item_name = key_list[val_list.index(event.widget)]
    item_name = item_name[0:item_name.find('_btn_')]
    item_type = manageSSH.check_if_item_is_dir(sftp, cur_path, item_name)
    item_path = cur_path + '\\' + item_name
    if item_type == 'dir':
        dlt_msg_box = messagebox.askquestion(title='Delete',
                                             message=f"""Are you sure you want to Permanently Delete the folder:\n"{item_name}"\nand all it's contents?""")
        if dlt_msg_box == 'yes':
            sftp2 = ssh.open_sftp()
            sftp2.rmdir(item_path)
            refresh_button()
    elif item_type == 'file':
        dlt_msg_box = messagebox.askquestion(title='Delete',
                                             message=f'Are you sure you want to Permanently Delete the File:\n"{item_name}" ?')
        if dlt_msg_box == 'yes':
            try:
                sftp2 = ssh.open_sftp()
                sftp2.remove(item_path)
                refresh_button()
            except PermissionError:
                messagebox.showerror(title="Can't delete this file",
                                     message="This file is open or being used by another software and can't be deleted at the moment")


def up_button():
    global cur_path, is_searching
    is_searching = False
    manageSSH.chdir(sftp, '..')
    cur_path = sftp.getcwd()[1:].replace('/', '\\')
    while cur_path.endswith('\\'):
        cur_path = cur_path[:len(cur_path) - 1]
    items_list = sftp.listdir()
    update_frame(items_list)


def refresh_button():
    global is_searching
    is_searching = False
    manageSSH.chdir(sftp, cur_path)
    items_list = sftp.listdir()
    update_frame(items_list)


def drives_box_change(event):
    global cur_path
    selected_drive = event.widget.get()
    cur_path = selected_drive
    manageSSH.chdir(sftp, cur_path)
    items_list = sftp.listdir()
    update_frame(items_list)


def close_window():
    discon_msg_box = messagebox.askquestion(title='Disconnect & Close',
                                            message='Are you sure you want to close the window and disconnect?')
    if discon_msg_box == 'yes':
        manageSSH.disconnect_ssh(ssh)
        root.destroy()


def copy_path_button(event):
    pyperclip.copy(cur_path)
    event.widget.configure(text='Copied!')
    event.widget.after(3000, lambda: event.widget.configure(text='Copy Path'))


def check_new_name(new_name, input_title, type):
    manageSSH.chdir(sftp, cur_path)
    items_list = sftp.listdir()
    lower_items_list = list()
    for item in items_list:
        lower_items_list.append(item.lower())

    invalid_names_list = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8',
                          'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']

    lowered_invalid_names_list = list()
    for invalid_name in invalid_names_list:
        lowered_invalid_names_list.append(invalid_name.lower())
    if type == 'dir':
        while True:
            if new_name == None or new_name == '':
                return False

            elif new_name.lower() in lower_items_list:
                new_name = simpledialog.askstring(input_title, 'This name is already taken, Try again:')

            elif new_name.lower() in lowered_invalid_names_list or new_name.__contains__('..'):
                new_name = simpledialog.askstring(input_title, 'This name is invalid, Try again:')

            elif not re.match(r"^[^\\/:*?\"<>|]+$", new_name):
                new_name = simpledialog.askstring(input_title, """The name can't contain: \/:*?"<>| Try again:""")

            elif new_name.endswith('.') or new_name.endswith(' '):
                new_name = new_name[:-1]
            else:
                return new_name

    elif type == 'file':
        while True:
            if new_name == None or new_name == '':
                return False

            elif new_name.lower() in lower_items_list:
                new_name = simpledialog.askstring(input_title, 'This name is already taken, Try again:')

            elif new_name in invalid_names_list:
                new_name = simpledialog.askstring(input_title, 'This name is invalid, Try again:')

            elif not re.match(r"^[^\\/:*?\"<>|]+$", new_name):
                new_name = simpledialog.askstring(input_title, """The name can't contain: \/:*?"<>| Try again:""")
            else:
                return new_name


def new_dir_button():
    new_folder_name = simpledialog.askstring('New folder', 'Enter a name for the folder:')
    new_folder_name = check_new_name(new_folder_name, 'New folder', 'dir')
    if new_folder_name != False:
        sftp.mkdir(new_folder_name)
        items_list = sftp.listdir()
        update_frame(items_list)


def update_frame(items_list):
    wrapper1.destroy()
    wrapper2.destroy()
    frame.destroy()
    create_frame(items_list)
    create_bttn(frame)


def create_search_bttn(frame, items_list):
    global icons_dict, bttns_dict, sftp, right_click_dir_search_menu, right_click_file_search_menu
    clm = 0
    rw = 2

    right_click_dir_search_menu = Menu(frame, tearoff=False)
    right_click_file_search_menu = Menu(frame, tearoff=False)

    dirs_list = list()
    files_list = list()
    for item in items_list:
        end_index = item.rfind('\\')
        item_name = item[end_index + 1:]
        item_path = item[:end_index]
        sftp2 = ssh.open_sftp()
        item_type = manageSSH.check_if_item_is_dir(sftp2, item_path, item_name)
        if item_type == 'dir':
            dirs_list.append(item_path + '\\' + item_name)
        elif item_type == 'file':
            files_list.append(item_path + '\\' + item_name)
    for item in items_list:
        end_index = item.rfind('\\')
        item_name = item[end_index + 1:]
        btn_text = item_name
        if item in dirs_list:
            # if 'item' is a dir
            file_type = '.dir_folder'
            if len(item_name) > 30:
                btn_text = btn_text[0:30] + '...'
        elif item in files_list:
            # if 'item' is a file
            end_index = item_name.rfind('.')
            file_type = item_name[end_index:].lower()

            if len(item_name) > 30:
                btn_text = btn_text[0:30] + '...' + file_type
        else:
            file_type = '.none'
        try:
            icon = icons_dict[file_type + '.png']
        except KeyError:
            icon = icons_dict['.none.png']
        bttns_dict[f'{item}_btn_{items_list.index(item)}'] = Button(frame, bg="gray", wraplength=100, text=btn_text,
                                                                    compound=TOP, justify=CENTER, image=icon,
                                                                    height=120, width=120)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].grid(column=clm, row=rw, sticky=N + S + E + W, padx=9,
                                                                pady=9)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind("<Button-3>", right_click_search)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind('<Double-Button-1>', double_click_search)
        clm += 1
        if clm == 7:
            clm = 0
            rw += 1


def double_click_search(event):
    global items_list, cur_path, frame, bttns_dict, is_searching
    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    full_path = key_list[val_list.index(event.widget)]
    full_path = full_path[0:full_path.find('_btn_')]
    end_index = full_path.rfind('\\')
    item_name = full_path[end_index + 1:]
    item_path = full_path[:full_path.rfind('\\')]
    temp = item_path + '\\' + item_name
    item_type = manageSSH.check_if_item_is_dir(sftp, item_path, item_name)
    if item_type == 'dir':
        is_searching = False
        cur_path = temp
        manageSSH.chdir(sftp, cur_path)
        items_list = sftp.listdir()
        update_frame(items_list)
    elif item_type == 'file':
        is_searching = False
        cur_path = item_path
        manageSSH.chdir(sftp, cur_path)
        items_list = sftp.listdir()
        update_frame(items_list)

    elif item_type == 'item not found':
        print(f'{item_name} - not found')
    else:
        pass


def right_click_search(event):
    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    item_path = key_list[val_list.index(event.widget)]
    item_path = item_path[:item_path.find('_btn_')]
    item_name = item_path[item_path.rfind('\\') + 1:]
    item_type = manageSSH.check_if_item_is_dir(sftp, item_path[:item_path.index(item_name)], item_name)

    right_click_dir_search_menu = Menu(root, tearoff=False)
    right_click_file_search_menu = Menu(root, tearoff=False)

    if item_type == 'dir':
        right_click_dir_search_menu.add_command(label='Open Folder', command=lambda: double_click_search(event))
        right_click_dir_search_menu.add_command(label='Copy Folder Path', command=lambda: pyperclip.copy(item_path))
        right_click_dir_search_menu.tk_popup(event.x_root, event.y_root)
    elif item_type == 'file':
        end_index = item_path.rfind('\\')
        item_location_path = item_path[:end_index]
        right_click_file_search_menu.add_command(label='Open File Location', command=lambda: double_click_search(event))
        right_click_file_search_menu.add_command(label='Copy File Location Path', command=lambda: pyperclip.copy(item_location_path))
        right_click_file_search_menu.tk_popup(event.x_root, event.y_root)


def create_frame(items_list):
    global frame, wrapper1, wrapper2, count, drives_list, is_searching, cur_path_label

    def f_refresh(event):
        refresh_button()
    root.bind('<F5>', f_refresh)

    count = 0

    def mouse_wheel(event):
        global count
        if len(items_list) > 21:
            if event.num == 5 or event.delta == -120:
                count -= 1
            if event.num == 4 or event.delta == 120:
                count += 1
            mycanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    wrapper1 = LabelFrame(root, height=10, bg='white')
    wrapper2 = LabelFrame(root)

    mycanvas = Canvas(wrapper2, bg='white')
    mycanvas.pack(side=LEFT, fill='both', expand='yes')

    yscrollbar = ttk.Scrollbar(wrapper2, orient='vertical', command=mycanvas.yview)
    yscrollbar.pack(side=RIGHT, fill='y')

    yscrollbar.config(command=mycanvas.yview)

    mycanvas.configure(yscrollcommand=yscrollbar.set)

    mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
    mycanvas.bind_all("<MouseWheel>", mouse_wheel)

    frame = Frame(mycanvas, bg='white')
    mycanvas.create_window((0, 0), window=frame, anchor='nw')

    wrapper1.pack(fill='both', expand='no', padx=10, pady=10)
    wrapper2.pack(fill='both', expand='yes', padx=10, pady=10)

    Grid.columnconfigure(wrapper1, 0, weight=1)
    Grid.rowconfigure(wrapper1, 0, weight=1)

    cur_path_label = Label(wrapper1, text=cur_path, wraplength=450, bg='white')
    cur_path_label.grid(column=3, row=0, sticky=W + E)

    copy_btn = Button(wrapper1, text='Copy Path', bg=buttons_bg_color)
    copy_btn.bind("<Button-1>", copy_path_button)
    copy_btn.grid(column=4, row=0, sticky=W)

    ip_username_label = Label(wrapper1, text=f'Connected to:\n{host} - {username}', wraplength=450, bg='white')
    ip_username_label.grid(column=5, row=0)

    disconnect_btn = Button(wrapper1, text='Disconnect', bg=buttons_bg_color, command=acc_signout)
    disconnect_btn.grid(column=6, row=0, sticky=W)

    up_btn = Button(wrapper1, image=icons_dict['up.png'], bg=buttons_bg_color, command=up_button)
    up_btn.grid(column=0, row=1)

    answr = str(manageSSH.run_action(ssh, 'wmic logicaldisk get caption').read())
    drives_list = answr[answr.find('Caption') + 9:answr.rfind(r'       \r\r\n\r\r\n')].split(r'       \r\r\n')
    drives_list[0] = drives_list[0].replace(r'\r\r\n', '')
    for i in range(len(drives_list)):
        drives_list[i] += '\\'
    drives_combobox = ttk.Combobox(wrapper1, values=drives_list, state='readonly')
    default_value = cur_path[0:3]
    try:
        drives_combobox.current(drives_list.index(default_value))
    except ValueError:
        default_value = cur_path[0:2] + '\\'
        drives_combobox.current(drives_list.index(default_value))
    drives_combobox.current(drives_list.index(default_value))
    drives_combobox.bind("<<ComboboxSelected>>", drives_box_change)
    drives_combobox.grid(column=2, row=1)

    drive_label = Label(wrapper1, text='Drive Select:', bg='white')
    drive_label.grid(column=2, row=0)

    ref_btn = Button(wrapper1, image=icons_dict['refresh.png'], bg=buttons_bg_color, command=refresh_button)

    def search():
        global is_searching
        root.bind('<Return>', no_action)
        root.config(cursor='exchange')
        is_searching = True
        temp_list = list()
        search_key = search_bar_entry.get()
        if search_key != '':
            sftp2 = ssh.open_sftp()
            items_list = manageSSH.tree_items(sftp2, cur_path, temp_list, search_key)
            root.config(cursor='arrow')
            if items_list == []:
                messagebox.showinfo(title='Not Found',
                                    message="Couldn't find any files or folders with this Search Key in the current path!")
            else:
                wrapper1.destroy()
                wrapper2.destroy()
                frame.destroy()
                create_frame(items_list)
                cur_path_label.configure(text=f'Searching for "{search_key}" in "{cur_path}"')
                create_search_bttn(frame, items_list)

    def entry_click(event):
        search_bar_entry.delete(0, 'end')
        def search2(event):
            search()
        root.bind('<Return>', search2)
        search_bar_entry.bind('<FocusOut>', entry_lost)

    def no_action(event):
        pass

    def entry_lost(event):
        search_bar_entry.insert(0, 'Search')
        root.bind('<Return>', no_action)
        search_bar_entry.bind('<FocusIn>', entry_click)
    
    if is_searching:
        stop_search_btn = Button(wrapper1, text='Stop Search', bg=buttons_bg_color, command=refresh_button)
        stop_search_btn.grid(column=5, row=1, sticky=E)
        ref_btn.grid(column=3, row=1)
    else:
        ref_btn.grid(column=4, row=1)
        new_dir_btn = Button(wrapper1, text='New folder', compound=TOP, justify=CENTER, image=icons_dict['new_dir.png'],
                             bg=buttons_bg_color, command=new_dir_button)
        new_dir_btn.grid(column=3, row=1)
        search_bar_entry = Entry(wrapper1, text='Search', font=(calc_width(20)))
        search_bar_entry.delete(0, 'end')
        search_bar_entry.insert(0, 'Search')
        search_bar_entry.bind('<FocusIn>', entry_click)
        search_bar_entry.grid(column=5, row=1, sticky=E, ipady=calc_height(1), padx=calc_width(25))
        search_btn = Button(wrapper1, image=icons_dict['search.png'], bg=buttons_bg_color, command=search)
        search_btn.grid(column=5, row=1, sticky=E)

    for x in range(10):
        Grid.columnconfigure(frame, x, weight=1)

    for y in range(5):
        Grid.rowconfigure(frame, y, weight=1)

    for x in range(10):
        Grid.columnconfigure(wrapper1, x, weight=1)


def acc_signout():
    discon_msg_box = messagebox.askquestion(title='Disconnect & Sign Out',
                                            message='Are you sure you want to disconnect and sign out of your account?')
    if discon_msg_box == 'yes':
        manageSSH.disconnect_ssh(ssh)
        root.destroy()
        main()


def main():
    global cur_path, root, frame, ssh, sftp
    global x, y, username, host, account, menubar, email

    SELF_NAME = os.getlogin()
    SELF_IP = socket.gethostbyname(socket.gethostname())


    root = Tk()
    x = int((screen_width - app_width) / 2)
    y = int((screen_height - app_height) / 2)
    root.geometry(f'{app_width}x{app_height}+{x}+{y}')
    root.iconbitmap('icon.ico')
    menubar = Menu(root)
    account = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Account', menu=account)
    pc_info = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='PC info', menu=pc_info)
    pc_info.add_command(label='Click to copy:', command=None, state='disabled', activebackground='grey90')
    pc_info.add_separator()

    def copy_ip():
        pyperclip.copy(SELF_IP)

    def copy_name():
        pyperclip.copy(SELF_NAME)

    pc_info.add_command(label=f'IP: {SELF_IP}', command=copy_ip, activebackground='steelblue2',
                        activeforeground='black')
    pc_info.add_command(label=f'Username: {SELF_NAME}', command=copy_name, activebackground='steelblue2',
                        activeforeground='black')

    def recheck_ssh_menubar():
        ssh_service_menu.entryconfigure(1, label=LoginRegister.check_sshd_service('sshd'))

    ssh_service_menu = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='SSH Service', menu=ssh_service_menu)
    ssh_service_menu.add_command(label='The SSH Service is:', command=None, state='disabled', activebackground='grey90')
    ssh_service_menu.add_command(label=LoginRegister.check_sshd_service('sshd'), command=None, state='disabled',
                                 activebackground='grey90')
    ssh_service_menu.add_separator()
    ssh_service_menu.add_command(label='Recheck Service', command=recheck_ssh_menubar, activebackground='steelblue2',
                                 activeforeground='black')
    root.config(menu=menubar)
    root.resizable(False, False)

    email, mode, ssh, sftp, username, host = LoginRegister.main(root, app_width, app_height, account, ssh_service_menu, None)
    if email != None and ssh != None and sftp != None:
        global cur_path
        root.protocol("WM_DELETE_WINDOW", close_window)
        root.geometry(f'{app_width}x{app_height}+{x}+{y}')
        root.title('Remote File Explorer')
        cur_path = rf'{system_drive}\Users\{username}\Desktop'
        manageSSH.chdir(sftp, cur_path)
        items_list = sftp.listdir()
        icons_dict = get_icons_dict()
        create_frame(items_list)
        create_bttn(frame)

        def go_to_path():
            global cur_path
            new_path = simpledialog.askstring('Enter a path', 'Enter a valid path to go to:')
            if new_path == '' or new_path == None:
                pass
            else:
                while new_path.startswith('\\') or new_path.startswith('/') or new_path.startswith(' '):
                    new_path = new_path[1:]
                new_path = new_path[0].upper() + new_path[1:]
                answr = manageSSH.chdir(sftp, new_path)
                if answr == 'path not found':
                    messagebox.showerror(title="The specified path doesn't exist",
                                         message=f"{new_path}\ndoesn't exist. Please try a different one")
                else:
                    cur_path = new_path
                    items_list = sftp.listdir()
                    update_frame(items_list)

        account.delete('Sign Out')
        account.add_command(label='Disconnect & Sign Out', command=acc_signout, activebackground='steelblue2',
                            activeforeground='black')

        def go_to_desktop():
            global cur_path
            cur_path = rf'{system_drive}\Users\{username}\Desktop'
            manageSSH.chdir(sftp, cur_path)
            items_list = sftp.listdir()
            update_frame(items_list)

        def go_to_documents():
            global cur_path
            cur_path = rf'{system_drive}\Users\{username}\Documents'
            manageSSH.chdir(sftp, cur_path)
            items_list = sftp.listdir()
            update_frame(items_list)

        def go_to_downloads():
            global cur_path
            cur_path = rf'{system_drive}\Users\{username}\Downloads'
            manageSSH.chdir(sftp, cur_path)
            items_list = sftp.listdir()
            update_frame(items_list)

        def go_to_pictures():
            global cur_path
            cur_path = rf'{system_drive}\Users\{username}\Pictures'
            manageSSH.chdir(sftp, cur_path)
            items_list = sftp.listdir()
            update_frame(items_list)

        def copy_file_to_remote():
            local_path = filedialog.askopenfilename(title='Choose a file to copy', filetypes=(('All Files', '*.*'),))
            if local_path:
                file = local_path[local_path.rfind('/'):]
                file_type = file[file.rfind('.'):]
                file_name = file[:file.rfind('.')]

                _, files_list = manageSSH.get_dirs_files_lists(sftp, cur_path)
                lower_items_list = list()
                for item in files_list:
                    lower_items_list.append(item.lower())
                while file[1:].lower() in lower_items_list:
                    lower_items_list.remove(file[1:].lower())
                    file_name += ' - copy'
                    file = file_name + file_type

                remote_path = cur_path + file
                sftp2 = ssh.open_sftp()
                sftp2.put(local_path, remote_path)
                refresh_button()


        go_to = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Go to...', menu=go_to)
        go_to.add_command(label='Desktop', command=go_to_desktop, activebackground='steelblue2',
                          activeforeground='black')
        go_to.add_command(label='Documents', command=go_to_documents, activebackground='steelblue2',
                          activeforeground='black')
        go_to.add_command(label='Downloads', command=go_to_downloads, activebackground='steelblue2',
                          activeforeground='black')
        go_to.add_command(label='Pictures', command=go_to_pictures, activebackground='steelblue2',
                          activeforeground='black')
        go_to.add_separator()
        go_to.add_command(label='Enter a path', command=go_to_path, activebackground='steelblue2',
                          activeforeground='black')

        file_transfer = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File Transfer', menu=file_transfer)
        file_transfer.add_command(label='Copy a file from this local computer to the remote computer',
                                  command=copy_file_to_remote, activebackground='steelblue2',
                                  activeforeground='black')

        end_video_name = 'end-animation.mp4'
        LoginRegister.play_video(end_video_name)

        root.mainloop()

if __name__ == '__main__':
    main()