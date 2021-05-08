__author__ = 'Yaniv Nash'

import LoginRegister
import manageSSH  # the file with funcs that connect to the ssh
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, filedialog
from tkinter import simpledialog  # opens the popup for the new folder name input
import paramiko
import socket
import os
import math
from PIL import ImageTk, Image
import pyperclip  # copy to clipboard module
import re
import wx  # get screen resolution
from bs4 import BeautifulSoup
import requests

OTHER_OS_PLATFORM = None

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
cur_path = ''

try:
    os.mkdir('downloaded_icons')
except FileExistsError:
    pass


def calc_size(size):
    """
    Calculates a certain size compared to the size of the app.
    :param size: The size when the app size is default (1070x700).
    :return: The size scaled to match the current app size.
    """
    if size == 0:
        return 0
    else:
        return int(app_width / (1070 / size))


def update_icons_dict(icons_path):
    """
    Updates the global var "icons_dir" to contain all the icons in a folder,
    their name as the key and an image object as the value.
    :param icons_path: The path to the folder that contains the icons you want to update.
    :return: None
    """
    icons_list = os.listdir(icons_path)
    for icon in icons_list:
        icons_dict[icon] = ImageTk.PhotoImage(Image.open(f'{icons_path}/{icon}'))


def download_icon(icon_name):
    """
    Searches google images for an icon and download it.
    :param icon_name: The name of the icon that needs to be downloaded.
    :return: None
    """
    URL = f"https://www.google.com/search?q={icon_name}+logo&newwindow=1&hl=en&sxsrf=ALeKk03_3mH_awXS2UWry7EgXMwViGLtEQ:1619816415283&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjR2aKw7qbwAhVIXRoKHVAkAMwQ_AUoAXoECAEQAw&biw=1920&bih=937"

    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', \
                'Accept-Language': 'en-US, en;q=0.5'})

    webpage = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(webpage.content, "html.parser")

    html_text = str(soup)
    url_start = html_text[html_text.find('src="h') + 5:]
    pic_url = url_start[:url_start.find('"')]

    response = requests.get(pic_url)
    with open(f'downloaded_icons/.lnk.{icon_name}.png', 'wb') as image:
        image.write(response.content)
    image = Image.open(f'downloaded_icons/.lnk.{icon_name}.png')
    image_ratio = image.size[1] / calc_size(60)
    smaller_image = image.resize((int(image.size[0] / image_ratio), calc_size(60)), Image.NEAREST)
    smaller_image.save(f'downloaded_icons/.lnk.{icon_name}.png')


def create_bttn(frame):
    """
    Creates a buttons grid that represents the files and folders on the remote computer.
    :param frame: A tkinter frame object that contains all the buttons
    :return: None
    """
    global icons_dict, bttns_dict, sftp, right_click_file_menu, right_click_dir_menu
    clm = 0
    rw = 2
    sftp = ssh.open_sftp()
    dirs_list, files_list = manageSSH.get_dirs_files_lists(sftp, cur_path)
    items_list = dirs_list + files_list
    items_len = len(items_list)
    if items_len == 0:
        Label(frame, text='This folder is empty', width=calc_size(150), bg='white').pack()
    else:
        if items_len >= 200:
            # extras_list = items_list[200:]
            items_list = items_list[:200] + [f'& {items_len - 200} more.>']
        downloaded_icons_list = os.listdir(f'{ROOT_PROJ_DIR}/downloaded_icons')
        for item in items_list:
            btn_text = item
            if item in dirs_list:
                # if 'item' is a dir
                file_type = 'dir_folder'
                if len(item) > 30:
                    btn_text = item[0:30] + '...'
            elif item in files_list:
                # if 'item' is a file
                file_type = item[item.rfind('.'):].lower()

                if file_type == '.lnk':
                    item_name = item[:item.rfind('.')]
                    file_type = f'.lnk.{item_name}'
                    if file_type + '.png' not in downloaded_icons_list:
                        download_icon(item_name)
                update_icons_dict(f'{ROOT_PROJ_DIR}/downloaded_icons')

                if len(item) > 30:
                    btn_text = item[0:30] + '...' + file_type
                    if file_type.startswith('.lnk.'):
                        btn_text = item[0:30] + '...' + '.lnk'
            else:
                file_type = '.none'
            try:
                icon = icons_dict[file_type + '.png']
            except KeyError:
                icon = icons_dict['.none.png']
            if item.endswith('more.>'):
                icon = ImageTk.PhotoImage(Image.open(f'assets/more.png'))
                btn_text = btn_text[:item.rfind('.')]
            bttns_dict[f'{item}_btn_{items_list.index(item)}'] = Button(frame, bg="gray", wraplength=calc_size(100), text=btn_text,
                                                                        compound=TOP, justify=CENTER, image=icon,
                                                                        height=calc_size(120), width=calc_size(120))

            bttns_dict[f'{item}_btn_{items_list.index(item)}'].image = icon

            bttns_dict[f'{item}_btn_{items_list.index(item)}'].grid(column=clm, row=rw, sticky=N + S + E + W, padx=calc_size(
                9),
                                                                    pady=calc_size(9))
            bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind("<Button-3>", right_click)
            bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind('<Double-Button-1>', double_click)
            clm += 1
            if clm == 7:
                clm = 0
                rw += 1

    if items_list[0].endswith('more.>'):
        items_len = len(items_list) - 1
    else:
        items_len = len(items_list)
    Label(root, text=f'{items_len} items', bg=frame_bg_color, anchor=W).place(x=calc_size(10), y=app_height - 11,
                                                                              width=calc_size(200),
                                                                              height=calc_size(11))


def double_click(event):
    """
    When double clicking one of the folders buttons, goes to the clicked folder and updates the screen.
    :param event: An object that contains info about the clicked button and the action
    :return: None
    """
    global items_list, cur_path, frame, bttns_dict
    if OTHER_OS_PLATFORM == 'windows':
        dir_sign = '\\'
    else:
        dir_sign = '/'
    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    item_name = key_list[val_list.index(event.widget)]
    item_name = item_name[0:item_name.find('_btn_')]
    sftp = ssh.open_sftp()
    if cur_path.count('/') > 1:
        if cur_path.endswith('\\') or cur_path.endswith('/'):
            cur_path = cur_path[:-1]
    temp = cur_path + dir_sign + item_name
    item_type = manageSSH.check_if_item_is_dir(sftp, cur_path, item_name)
    if item_type == 'dir':
        cur_path = temp
        manageSSH.chdir(sftp, cur_path)
        items_list = sftp.listdir()
        if cur_path.startswith('//'):
            cur_path = cur_path[1:]
        update_frame(items_list)
    sftp.close()


def right_click(event):
    """
    Creates a matching menu when right clicking one of the files or folders buttons.
    :param event: An object that contains info about the clicked button and the action
    :return: None
    """
    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    item_name = key_list[val_list.index(event.widget)]
    item_name = item_name[:item_name.find('_btn_')]
    sftp = ssh.open_sftp()
    item_type = manageSSH.check_if_item_is_dir(sftp, cur_path, item_name)

    right_click_dir_menu = Menu(root, tearoff=False)
    right_click_file_menu = Menu(root, tearoff=False)

    if item_type == 'dir':
        right_click_dir_menu.add_command(label='Open Folder', command=lambda: double_click(event))
        right_click_dir_menu.add_command(label='Rename Folder', command=lambda: rename_item(event))
        right_click_dir_menu.add_command(label='Delete Folder', command=lambda: delete_item(event))
        right_click_dir_menu.tk_popup(event.x_root, event.y_root)
    elif item_type == 'file':
        right_click_file_menu.add_command(label='Download File', command=lambda: download_file(event))
        right_click_file_menu.add_command(label='Rename File', command=lambda: rename_item(event))
        right_click_file_menu.add_command(label='Delete File', command=lambda: delete_item(event))
        right_click_file_menu.tk_popup(event.x_root, event.y_root)
    sftp.close()


def download_file(event):
    """
    Downloads a file from the remote computer to the local computer through SFTP.
    :param event: An object that contains info about the clicked button and the action
    :return: None
    """
    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    item_name = key_list[val_list.index(event.widget)]
    file = item_name[:item_name.find('_btn_')]
    file_type = file[file.rfind('.'):]
    local_path = filedialog.asksaveasfilename(defaultextension=file_type, title='Choose where to save the file',
                                              initialfile=file, filetypes=((file_type, file_type),))
    if local_path:
        if OTHER_OS_PLATFORM == 'windows':
            remote_path = cur_path + '\\' + file
        else:
            remote_path = cur_path + '/' + file

        sftp = ssh.open_sftp()
        sftp.get(remote_path, local_path)
        refresh_screen()
        sftp.close()


def rename_item(event):
    """
    Gets a new name for a file or folder as an input, checks it that it's a valid name
    and finally renames said file or folder on the remote computer.
    :param event: An object that contains info about the clicked button and the action
    :return: None
    """
    global sftp
    if OTHER_OS_PLATFORM == 'windows':
        dir_sign = '\\'
    else:
        dir_sign = '/'
    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    old_name = key_list[val_list.index(event.widget)]
    old_name = old_name[0:old_name.find('_btn_')]
    item_type = manageSSH.check_if_item_is_dir(sftp, cur_path, old_name)
    old_path = cur_path + dir_sign + old_name
    new_name = simpledialog.askstring(title='Rename', prompt=f'Enter a new name for "{old_name}":',
                                      initialvalue=old_name, parent=root)
    sftp2 = ssh.open_sftp()
    if new_name is not None and new_name != '' and new_name != old_name:
        new_name = check_new_name(new_name, 'Rename', item_type, old_name, old_name)

        if new_name != False:
            if item_type == 'file':
                file_type = old_name[old_name.rfind('.'):]
                if file_type != new_name[new_name.rfind('.'):]:
                    change_type = messagebox.askquestion(title='Change file extension',
                                                         message='If you change the file extension the file might be unusable.\nAre you sure you want to continue?',
                                                         icon='warning')
                    if change_type == 'no':
                        return

            new_path = cur_path + dir_sign + new_name
            sftp2.rename(old_path, new_path)
            refresh_screen()
    sftp2.close()


def delete_item(event):
    """
    Deletes a specified file or folder on the remote computer.
    :param event: An object that contains info about the clicked button and the action
    :return: None
    """
    global sftp
    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    item_name = key_list[val_list.index(event.widget)]
    item_name = item_name[0:item_name.find('_btn_')]
    item_type = manageSSH.check_if_item_is_dir(sftp, cur_path, item_name)
    if OTHER_OS_PLATFORM == 'windows':
        dir_sign = '\\'
    else:
        dir_sign = '\\'
    item_path = cur_path + dir_sign + item_name
    sftp2 = ssh.open_sftp()
    if item_type == 'dir':
        dlt_msg_box = messagebox.askquestion(title='Delete',
                                             message=f"""Are you sure you want to Permanently Delete the folder:\n"{item_name}"\nand all it's contents?""")
        if dlt_msg_box == 'yes':
            try:
                sftp2.rmdir(item_path)
            except:
                tree_list = manageSSH.search_tree_items(sftp2, item_path, [], '', OTHER_OS_PLATFORM)
                temp = tree_list.copy()
                longest_path = 0
                for item in tree_list:
                    if item.count(dir_sign) > longest_path:
                        longest_path = item.count(dir_sign)
                sorted_items_list = []
                while temp != [] and longest_path >= 0:
                    for item in tree_list:
                        if item.count(dir_sign) == longest_path:
                            sorted_items_list.append(item)
                            temp.remove(item)
                    longest_path -= 1

                for item in sorted_items_list:
                    try:
                        sftp2.rmdir(item)
                    except:
                        try:
                            sftp2.remove(item)
                        except:
                            pass
                try:
                    sftp2.rmdir(item_path)
                except:
                    messagebox.showerror(title="Can't delete this folder",
                                         message="There's an error, Please try again later")
    elif item_type == 'file':
        dlt_msg_box = messagebox.askquestion(title='Delete',
                                             message=f'Are you sure you want to Permanently Delete the File:\n"{item_name}" ?')
        if dlt_msg_box == 'yes':
            try:
                sftp2.remove(item_path)
            except PermissionError:
                messagebox.showerror(title="Can't delete this file",
                                     message="This file is open or being used by another software and can't be deleted at the moment")
    refresh_screen()
    sftp2.close()


def up_button():
    """
    Goes one dir up and updates the screen.
    :return: None
    """
    global cur_path, is_searching
    is_searching = False
    manageSSH.chdir(sftp, '..')
    if OTHER_OS_PLATFORM == 'windows':
        cur_path = sftp.getcwd()[1:].replace('/', '\\')
        while cur_path.endswith('\\'):
            cur_path = cur_path[:len(cur_path) - 1]
    else:
        cur_path = '/' + sftp.getcwd()[1:]
        if cur_path.count('/') > 1:
            while cur_path.endswith('/'):
                cur_path = cur_path[:len(cur_path) - 1]
    items_list = sftp.listdir()
    update_frame(items_list)


def refresh_screen():
    """
    Refreshes the app's screen.
    :return: None
    """
    global is_searching
    is_searching = False
    try:
        sftp2 = ssh.open_sftp()
        manageSSH.chdir(sftp2, cur_path)
        items_list = sftp2.listdir()
        update_frame(items_list)
        sftp2.close()
    except paramiko.ssh_exception.SSHException:
        messagebox.showerror(title='Disconnected',
                             message='The connection was disconnected!\nPlease check the connection and try again')
        manageSSH.disconnect_ssh(ssh)
        root.destroy()
        main()


def drives_box_change(event):
    """
    Goes to the chosen drive.
    :param event: An object that contains info about the clicked button and the action
    :return: None
    """
    global cur_path, is_searching
    is_searching = False
    selected_drive = event.widget.get()
    cur_path = selected_drive
    sftp = ssh.open_sftp()
    manageSSH.chdir(sftp, cur_path)
    items_list = sftp.listdir()
    update_frame(items_list)
    sftp.close()


def close_window():
    """
    Asks for confirmation and if granted, closes the window.
    :return: None
    """
    discon_msg_box = messagebox.askquestion(title='Disconnect & Close',
                                            message='Are you sure you want to close the window and disconnect?')
    if discon_msg_box == 'yes':
        manageSSH.disconnect_ssh(ssh)
        root.destroy()


def copy_path_button(event):
    """
    Copies the current path and shows feedback.
    :param event: An object that contains info about the clicked button and the action
    :return: None
    """
    pyperclip.copy(cur_path)
    event.widget.configure(text='Copied!')
    event.widget.after(3000, lambda: event.widget.configure(text='Copy Path'))


def check_new_name(new_name, input_title, type, old_name, initialv):
    """
    Checks if a new file or folder name is already taken or invalid.
    :param new_name: A new name that needs to be checked
    :param input_title: The title that will be shown on the popup window if a new input is required
    :param type: If the new name belongs to a file or a folder
    :param old_name: The current name of the file or folder
    :param initialv: The popup's initial value when asking for a new input
    :return: False - if the user entered an empty input, clicked "Cancel" or
                    the new name is the same as the current name
            new_name - if the name is valid
    """
    sftp = ssh.open_sftp()
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
            if new_name == None or new_name == '' or new_name == old_name:
                return False

            elif new_name.lower() in lower_items_list:
                new_name = simpledialog.askstring(title=input_title, prompt='This name is already taken, Try again:',
                                                  initialvalue=initialv, parent=root)

            elif new_name.lower() in lowered_invalid_names_list or new_name.__contains__('..'):
                new_name = simpledialog.askstring(title=input_title, prompt='This name is invalid, Try again:',
                                                  initialvalue=initialv, parent=root)

            elif not re.match(r"^[^\\/:*?\"<>|]+$", new_name):
                new_name = simpledialog.askstring(title=input_title,
                                                  prompt="""The name can't contain: \/:*?"<>| Try again:""",
                                                  initialvalue=initialv, parent=root)

            elif new_name.endswith('.') or new_name.endswith(' '):
                new_name = new_name[:-1]
            else:
                return new_name

    elif type == 'file':
        while True:
            if new_name == None or new_name == '' or new_name == old_name:
                return False

            elif new_name.lower() in lower_items_list:
                new_name = simpledialog.askstring(title=input_title, prompt='This name is already taken, Try again:',
                                                  initialvalue=initialv, parent=root)

            elif new_name in invalid_names_list:
                new_name = simpledialog.askstring(title=input_title, prompt='This name is invalid, Try again:',
                                                  initialvalue=initialv, parent=root)

            elif not re.match(r"^[^\\/:*?\"<>|]+$", new_name):
                new_name = simpledialog.askstring(title=input_title,
                                                  prompt="""The name can't contain: \/:*?"<>| Try again:""",
                                                  initialvalue=initialv, parent=root)
            else:
                return new_name
    sftp.close()


def new_dir_button():
    """
    Creates a new folder on the remote computer.
    :return: None
    """
    new_folder_name = simpledialog.askstring(title='New folder', prompt='Enter a name for the folder:',
                                             initialvalue='New folder', parent=root)
    new_folder_name = check_new_name(new_folder_name, 'New folder', 'dir', '', 'New folder')
    if new_folder_name != False:
        sftp.mkdir(new_folder_name)
        items_list = sftp.listdir()
        update_frame(items_list)


def update_frame(items_list):
    """
    Updates the main frame of the app.
    :param items_list: A list with all the items' names in the current remote path
    :return: None
    """
    wrapper1.destroy()
    wrapper2.destroy()
    frame.destroy()
    create_frame(items_list)
    create_bttn(frame)


def create_search_bttn(frame, items_list):
    """
    Creates a buttons grid that represents the files and folders on the remote computer that matched the search key.
    :param frame: A tkinter frame object that contains all the buttons
    :param items_list: A list with all the items' names in the current remote path
    :return:
    """
    global icons_dict, bttns_dict, right_click_dir_search_menu, right_click_file_search_menu
    clm = 0
    rw = 2

    right_click_dir_search_menu = Menu(frame, tearoff=False)
    right_click_file_search_menu = Menu(frame, tearoff=False)

    dirs_list = list()
    files_list = list()
    if OTHER_OS_PLATFORM == 'windows':
        dir_sign = '\\'
    else:
        dir_sign = '/'

    downloaded_icons_list = list()
    if len(items_list) > 0:
        downloaded_icons_list = os.listdir(f'{ROOT_PROJ_DIR}/downloaded_icons')
    items_len = len(items_list)
    if items_len >= 200:
        # extras_list = items_list[200:]
        items_list = items_list[:200] + [f'& {items_len - 200} more.>']
    sftp = ssh.open_sftp()
    for item in items_list:
        end_index = item.rfind(dir_sign)
        item_name = item[end_index + 1:]
        item_path = item[:end_index]
        item_type = manageSSH.check_if_item_is_dir(sftp, item_path, item_name)
        if item_type == 'dir':
            dirs_list.append(item_path + dir_sign + item_name)
        elif item_type == 'file':
            files_list.append(item_path + dir_sign + item_name)
    for item in items_list:
        end_index = item.rfind(dir_sign)
        item_name = item[end_index + 1:]
        btn_text = item_name
        if item in dirs_list:
            # if 'item' is a dir
            file_type = 'dir_folder'
            if len(item_name) > 30:
                btn_text = btn_text[0:30] + '...'
        elif item in files_list:
            # if 'item' is a file
            file_type = item_name[item_name.rfind('.'):].lower()

            if file_type == '.lnk':
                item_name = item_name[:item_name.rfind('.')]
                file_type = f'.lnk.{item_name}'
                if file_type + '.png' not in downloaded_icons_list:
                    download_icon(item_name)
            update_icons_dict(f'{ROOT_PROJ_DIR}/downloaded_icons')

            if len(item_name) > 30:
                btn_text = btn_text[0:30] + '...' + file_type
                if file_type.startswith('.lnk.'):
                    btn_text = item[0:30] + '...' + '.lnk'
        else:
            file_type = '.none'
        try:
            icon = icons_dict[file_type + '.png']
        except KeyError:
            icon = icons_dict['.none.png']
        if item.endswith('more.>'):
            icon = ImageTk.PhotoImage(Image.open(f'assets/more.png'))
            btn_text = btn_text[:item.rfind('.')]
        bttns_dict[f'{item}_btn_{items_list.index(item)}'] = Button(frame, bg="gray", wraplength=calc_size(100), text=btn_text,
                                                                    compound=TOP, justify=CENTER, image=icon,
                                                                    height=calc_size(120), width=calc_size(120))
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].image = icon
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].grid(column=clm, row=rw, sticky=N + S + E + W, padx=9,
                                                                pady=9)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind("<Button-3>", right_click_search)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind('<Double-Button-1>', double_click_search)
        clm += 1
        if clm == 7:
            clm = 0
            rw += 1
        sftp.close()

    if items_list[0].endswith('more.>'):
        items_len = len(items_list) - 1
    else:
        items_len = len(items_list)
    Label(root, text=f'{items_len} items', bg=frame_bg_color, anchor=W).place(x=calc_size(10), y=app_height - 11,
                                                                              width=calc_size(200),
                                                                              height=calc_size(11))


def double_click_search(event):
    """
    When double clicking a file, goes to it's parent dir,
    when double clocking a folder, goes to that folder.
    :param event: An object that contains info about the clicked button and the action
    :return: None
    """
    global items_list, cur_path, frame, bttns_dict, is_searching
    if OTHER_OS_PLATFORM == 'windows':
        dir_sign = '\\'
    else:
        dir_sign = '/'
    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    full_path = key_list[val_list.index(event.widget)]
    full_path = full_path[0:full_path.find('_btn_')]
    end_index = full_path.rfind(dir_sign)
    item_name = full_path[end_index + 1:]
    item_path = full_path[:full_path.rfind(dir_sign)]
    temp = item_path + dir_sign + item_name
    sftp = ssh.open_sftp()
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
        if not item_name.endswith('more.>'):
            print(f'{item_name} - not found')
    else:
        pass
    sftp.close()


def right_click_search(event):
    """
    Creates a matching menu when right clicking one of the files or folders buttons.
    :param event: An object that contains info about the clicked button and the action
    :return: None
    """
    if OTHER_OS_PLATFORM == 'windows':
        dir_sign = '\\'
    else:
        dir_sign = '/'
    sftp = ssh.open_sftp()
    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    item_path = key_list[val_list.index(event.widget)]
    item_path = item_path[:item_path.find('_btn_')]
    item_name = item_path[item_path.rfind(dir_sign) + 1:]
    item_type = manageSSH.check_if_item_is_dir(sftp, item_path[:item_path.index(item_name)], item_name)

    right_click_dir_search_menu = Menu(root, tearoff=False)
    right_click_file_search_menu = Menu(root, tearoff=False)

    if item_type == 'dir':
        right_click_dir_search_menu.add_command(label='Open Folder', command=lambda: double_click_search(event))
        right_click_dir_search_menu.add_command(label='Copy Folder Path', command=lambda: pyperclip.copy(item_path))
        right_click_dir_search_menu.tk_popup(event.x_root, event.y_root)
    elif item_type == 'file':
        end_index = item_path.rfind(dir_sign)
        item_location_path = item_path[:end_index]
        right_click_file_search_menu.add_command(label='Open File Location', command=lambda: double_click_search(event))
        right_click_file_search_menu.add_command(label='Copy File Location Path',
                                                 command=lambda: pyperclip.copy(item_location_path))
        right_click_file_search_menu.tk_popup(event.x_root, event.y_root)
    sftp.close()


def create_frame(items_list):
    """
    Creates the main frame of the app.
    :param items_list: A list with all the items' names in the current remote path
    :return: None
    """
    global frame, wrapper1, wrapper2, count, drives_list, is_searching, cur_path_label

    def f5_refresh(event):
        refresh_screen()
    root.bind('<F5>', f5_refresh)

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

    ip_username_label = Label(wrapper1, text=f'Connected to:\n{username}@{host}', wraplength=450, bg='white')
    ip_username_label.grid(column=5, row=0)

    disconnect_btn = Button(wrapper1, text='Disconnect', bg=buttons_bg_color, command=acc_signout)
    disconnect_btn.grid(column=6, row=0, sticky=W)

    up_btn = Button(wrapper1, image=up_pic, bg=buttons_bg_color, command=up_button)
    up_btn.grid(column=0, row=1)

    if OTHER_OS_PLATFORM == 'windows':
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

    ref_btn = Button(wrapper1, image=ref_pic, bg=buttons_bg_color, command=refresh_screen)

    def search():
        """
        Gets a list with items that contains the search key in their names.
        :return: None
        """
        global is_searching
        root.bind('<Return>', no_action)
        is_searching = True
        temp_list = list()
        search_key = search_bar_entry.get()
        if search_key != '':
            sftp = ssh.open_sftp()
            items_list = manageSSH.search_tree_items(sftp, cur_path, temp_list, search_key, OTHER_OS_PLATFORM)
            sftp.close()
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
        stop_search_btn = Button(wrapper1, text='Stop Search', bg=buttons_bg_color, command=refresh_screen)
        stop_search_btn.grid(column=5, row=1, sticky=E)
        ref_btn.grid(column=3, row=1)
    else:
        ref_btn.grid(column=4, row=1)
        new_dir_btn = Button(wrapper1, text='New folder', compound=TOP, justify=CENTER, image=new_dir_pic,
                             bg=buttons_bg_color, command=new_dir_button)
        new_dir_btn.grid(column=3, row=1)
        search_bar_entry = Entry(wrapper1, text='Search', font=(calc_size(20)))
        search_bar_entry.delete(0, 'end')
        search_bar_entry.insert(0, 'Search')
        search_bar_entry.bind('<FocusIn>', entry_click)
        search_bar_entry.grid(column=5, row=1, sticky=E, ipady=calc_size(1), padx=calc_size(25))
        search_btn = Button(wrapper1, image=search_pic, bg=buttons_bg_color, command=search)
        search_btn.grid(column=5, row=1, sticky=E)

    for x in range(10):
        Grid.columnconfigure(frame, x, weight=1)

    for y in range(5):
        Grid.rowconfigure(frame, y, weight=1)

    for x in range(10):
        Grid.columnconfigure(wrapper1, x, weight=1)


def acc_signout():
    """
    Asks for confirmation and if granted, signs out of the account.
    :return: None
    """
    discon_msg_box = messagebox.askquestion(title='Disconnect & Sign Out',
                                            message='Are you sure you want to disconnect and sign out of your account?')
    if discon_msg_box == 'yes':
        manageSSH.disconnect_ssh(ssh)
        root.destroy()
        main()


def main():
    """
    The main func of the file.
    :return: None
    """
    global cur_path, root, frame, ssh, new_dir_pic, ref_pic, up_pic, search_pic
    global x, y, username, host, account, menubar, email

    SELF_NAME = os.getlogin()
    SELF_IP = socket.gethostbyname(socket.gethostname())

    root = Tk()
    x = int((screen_width - app_width) / 2)
    y = int((screen_height - app_height) / 2)
    root.geometry(f'{app_width}x{app_height}+{x}+{y}')
    root.iconbitmap('assets/icon.ico')
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

    email, mode, ssh, sftp, username, host = LoginRegister.main(root, app_width, app_height, account, ssh_service_menu,
                                                                None)
    if email != None and ssh != None and sftp != None:
        global cur_path, OTHER_OS_PLATFORM
        root.protocol("WM_DELETE_WINDOW", close_window)
        root.geometry(f'{app_width}x{app_height}+{x}+{y}')
        root.title('Remote File Explorer')
        if manageSSH.run_action(ssh, 'systeminfo').read().decode().__contains__('Microsoft Windows'):
            OTHER_OS_PLATFORM = 'windows'
            cur_path = rf'{system_drive}\Users\{username}\Desktop'
        elif manageSSH.run_action(ssh, 'uname').read().decode() == 'Linux\n':
            OTHER_OS_PLATFORM = 'linux'
            cur_path = manageSSH.run_action(ssh, 'pwd').read().decode().replace('\n', '')
        elif manageSSH.run_action(ssh, 'uname').read().decode() == 'Darwin\n':
            OTHER_OS_PLATFORM = 'macos'
            cur_path = manageSSH.run_action(ssh, 'pwd').read().decode().replace('\n', '')
        manageSSH.chdir(sftp, cur_path)
        items_list = sftp.listdir()
        update_icons_dict(f'{ROOT_PROJ_DIR}/icons')
        new_dir_pic = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}/assets/new_dir.png'))
        search_pic = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}/assets/search.png'))
        up_pic = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}/assets/up.png'))
        ref_pic = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}/assets/refresh.png'))

        create_frame(items_list)
        create_bttn(frame)

        def go_to_path():
            global cur_path
            if OTHER_OS_PLATFORM == 'windows':
                dir_sign = '\\'
            else:
                dir_sign = '/'
            new_path = simpledialog.askstring(title='Enter a path', prompt='Enter a valid path to go to:', parent=root)
            if new_path != '' and new_path != None:
                while new_path.startswith('\\') or new_path.startswith('/') or new_path.startswith(' '):
                    new_path = new_path[1:]
                while new_path.endswith('\\') or new_path.endswith('/') or new_path.endswith(' '):
                    new_path = new_path[:-1]
                if OTHER_OS_PLATFORM == 'windows':
                    new_path = new_path[0].upper() + new_path[1:]
                else:
                    new_path = '/' + new_path
                item_type = manageSSH.check_if_item_is_dir(sftp, new_path[:new_path.rfind(dir_sign)],
                                                           new_path[new_path.rfind(dir_sign) + 1:])
                if item_type == 'dir':
                    answr = manageSSH.chdir(sftp, new_path)
                    if answr == 'path not found':
                        messagebox.showerror(title="The specified path doesn't exist",
                                             message=f"{new_path}\ndoesn't exist. Please try a different one")
                    else:
                        cur_path = new_path
                        items_list = sftp.listdir()
                        update_frame(items_list)
                elif item_type == 'file':
                    messagebox.showerror(title="The specified path is a file",
                                         message=f"{new_path}\nis a file. Please try a different one")
                else:
                    messagebox.showerror(title="The specified path doesn't exist",
                                         message=f"{new_path}\ndoesn't exist. Please try a different one")

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
                sftp = ssh.open_sftp()

                _, files_list = manageSSH.get_dirs_files_lists(sftp, cur_path)
                lower_items_list = list()
                for item in files_list:
                    lower_items_list.append(item.lower())
                while file[1:].lower() in lower_items_list:
                    lower_items_list.remove(file[1:].lower())
                    file_name += ' - copy'
                    file = file_name + file_type

                remote_path = cur_path + file
                sftp.put(local_path, remote_path)
                refresh_screen()
                sftp.close()

        def open_cmd_terminal():
            global row, line, list_count, button_count, cur_dir
            if OTHER_OS_PLATFORM == 'windows':
                dir_sign = '\\'
            else:
                dir_sign = '/'

            cur_dir = cur_path

            row = 0
            line = 1.0
            list_count = 0
            button_count = 0
            cmnds_list = list()
            text_box_dict = dict()

            def up_key(event):
                global list_count, button_count
                if abs(list_count) < len(cmnds_list):
                    list_count -= 1
                    text_box_dict[f'{button_count}_input'].delete('1.0', 'end')
                    text_box_dict[f'{button_count}_input'].insert('1.0', cmnds_list[list_count])

            def down_key(event):
                global list_count, button_count
                if list_count < 0:
                    list_count += 1
                    text_box_dict[f'{button_count}_input'].delete('1.0', 'end')
                    text_box_dict[f'{button_count}_input'].insert('1.0', cmnds_list[list_count])
                if list_count == 0:
                    text_box_dict[f'{button_count}_input'].delete('1.0', 'end')

            def enter_key(event):
                global row, line, list_count, cur_dir, button_count
                line += 1.0
                row += 1
                button_count += 1
                list_count = 0
                cmnd = text_box_dict[f'{button_count - 1}_input'].get('1.0', 'end')
                answer_lines = 1
                cmnd_lines = 1
                print_msg = ''
                if cmnd.replace('\n', '') != '':
                    cmnd_lines = math.ceil(len(cmnd) / 59)
                    row += cmnd_lines
                    cmnds_list.append(cmnd)

                    while cmnd.startswith(' '):
                        cmnd = cmnd[1:]
                    if cmnd.startswith('cd '):
                        if cmnd.__contains__('cd ..'):
                            temp = cur_dir[:cur_dir.rfind(dir_sign)]
                        else:
                            temp = cur_dir + dir_sign + cmnd[3:].replace('\n', '')
                        stderr = ''
                        stdout = manageSSH.chdir(sftp, temp)
                        if stdout == 'path not found':
                            stderr = 'The system cannot find the path specified.'
                        else:
                            cur_dir = temp
                        stdout = ''
                    else:
                        cmnd = f"cd {cur_dir} && {cmnd}"

                        stdin, stdout, stderr = manageSSH.cmd_terminal(ssh, cmnd)

                        stdout = stdout.read().decode()

                        stderr = stderr.read().decode()

                    answer_lines = 0
                    if stdout != '':
                        answer_lines += math.ceil(len(stdout) / 72)
                        print_msg += stdout
                    if stderr != '':
                        answer_lines += math.ceil(len(stderr) / 72)
                        print_msg += stderr
                    if stdout != '' and stderr != '':
                        print_msg = f'{stdout}\n{stderr}'

                text_box_dict[f'{button_count - 1}_input'].configure(height=cmnd_lines, state=DISABLED)

                text_box_dict[f'{button_count}_answer'] = Text(sec_frame, bg='black', bd='0', fg='white',
                                                               blockcursor=True,
                                                               insertbackground='white',
                                                               selectforeground='black', selectbackground='white',
                                                               font=('Arial', calc_size(14)),
                                                               width=55,
                                                               height=answer_lines)
                text_box_dict[f'{button_count}_answer'].insert('end', print_msg)
                text_box_dict[f'{button_count}_answer'].configure(state=DISABLED)
                text_box_dict[f'{button_count}_answer'].grid(row=row, column=1, sticky=NW)

                row += answer_lines

                text_box_dict[f'{button_count}_label'] = Label(sec_frame, bg='black', fg='green', text=cur_dir + '>',
                                                               font=('Arial', calc_size(14)))
                text_box_dict[f'{button_count}_label'].grid(row=row, column=0, sticky=NW)

                popup.update()
                text_box_dict[f'{button_count}_input'] = Text(sec_frame, bg='black', bd='0', fg='white',
                                                              blockcursor=True,
                                                              insertbackground='white',
                                                              selectforeground='black', selectbackground='white',
                                                              font=('Arial', calc_size(14)),
                                                              width=math.floor(70 - text_box_dict[
                                                                  f'{button_count - 1}_label'].winfo_width() / 12) - 2,
                                                              height=18, wrap=CHAR)
                text_box_dict[f'{button_count}_input'].grid(row=row, column=1, sticky=W)

                text_box_dict[f'{button_count}_input'].focus()
                text_box_dict[f'{button_count}_input'].bind('<Up>', up_key)
                text_box_dict[f'{button_count}_input'].bind('<Down>', down_key)
                text_box_dict[f'{button_count}_input'].bind('<Return>', enter_key)

                if row > 15:
                    scroll_canvas.yview_moveto('1')

            def close_popup():
                popup.destroy()
                sftp.close()
                refresh_screen()

            sftp = ssh.open_sftp()
            popup_width = calc_size(800)
            popup_height = calc_size(400)
            popup_x = int((screen_width - popup_width) / 2)
            popup_y = int((screen_height - popup_height) / 2)
            popup = Toplevel(bg='black')
            popup.geometry(f'{popup_width}x{popup_height}+{popup_x}+{popup_y}')
            popup.iconbitmap('assets/cmd-terminal.ico')
            popup.resizable(False, False)
            popup.protocol("WM_DELETE_WINDOW", close_popup)

            def on_mousewheel(event):
                scroll_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            main_frame = Frame(popup)
            main_frame.pack(fill=BOTH, expand=1)

            scroll_canvas = Canvas(main_frame, bg='black')
            scroll_canvas.pack(side=LEFT, fill=BOTH, expand=1)

            scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=scroll_canvas.yview, highlightcolor='black',
                                  activebackground='black')
            scrollbar.pack(side=RIGHT, fill=Y)

            scroll_canvas.bind_all("<MouseWheel>", on_mousewheel)

            scroll_canvas.configure(yscrollcommand=scrollbar.set)
            scroll_canvas.bind(
                ('<Configure>', lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))))

            sec_frame = Frame(scroll_canvas, bg='black')
            scroll_canvas.create_window((0, 0), window=sec_frame, anchor=NW)

            def reset_scrollregion(event):
                scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

            sec_frame.bind("<Configure>", reset_scrollregion)

            text_box_dict[f'{button_count}_label'] = Label(sec_frame, bg='black', fg='green', text=cur_dir + '>',
                                                           font=('Arial', calc_size(14)))
            text_box_dict[f'{button_count}_label'].grid(row=row, column=0, sticky=NW)
            popup.update()

            text_box_dict[f'{button_count}_input'] = Text(sec_frame, bg='black', bd='0', fg='white', blockcursor=True,
                                                          insertbackground='white',
                                                          selectforeground='black', selectbackground='white',
                                                          font=('Arial', calc_size(14)),
                                                          width=math.floor(
                                                              70 - text_box_dict[
                                                                  f'{button_count}_label'].winfo_width() / 12) - 2,
                                                          height=18,
                                                          wrap=CHAR)
            text_box_dict[f'{button_count}_input'].grid(row=row, column=1, sticky=NW)

            text_box_dict[f'{button_count}_input'].focus()
            text_box_dict[f'{button_count}_input'].bind('<Up>', up_key)
            text_box_dict[f'{button_count}_input'].bind('<Down>', down_key)
            text_box_dict[f'{button_count}_input'].bind('<Return>', enter_key)

            popup.mainloop()

        go_to = Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Go to...', menu=go_to)
        if OTHER_OS_PLATFORM == 'windows':
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

        cmd_terminal = Menu(menubar, tearoff=0)
        if OTHER_OS_PLATFORM == 'windows':
            menu_name = 'CMD'
        else:
            menu_name = 'Terminal'
        menubar.add_cascade(label=menu_name, menu=cmd_terminal)
        cmd_terminal.add_command(label=f'Open {menu_name}',
                                 command=open_cmd_terminal, activebackground='steelblue2',
                                 activeforeground='black')

        end_video_name = f'{ROOT_PROJ_DIR}/assets/end-animation.mp4'
        LoginRegister.play_video(end_video_name)

        root.mainloop()


if __name__ == '__main__':
    main()
