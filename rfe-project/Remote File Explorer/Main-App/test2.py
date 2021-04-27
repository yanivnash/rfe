from tkinter import *
import wx
import math
import manageSSH

app = wx.App(False)
screen_width, screen_height = wx.GetDisplaySize()

if screen_width / screen_height != (1920 / 1080):
    screen_height = screen_width / (1920 / 1080)

if screen_width >= 1070 and screen_height >= 700:
    screen_width = 1920
    screen_height = 1080

app_width = int(screen_width / 1.794)
app_height = int(screen_height / 1.542)


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


username = 'yaniv'
ssh = manageSSH.connect_to_ssh('192.168.1.20', username, 'Yanivn911911')


system_drive = 'C:'


if manageSSH.run_action(ssh, 'systeminfo').read().decode().__contains__('Microsoft Windows'):
    OTHER_OS_PLATFORM = 'windows'
    cur_path = rf'{system_drive}\Users\{username}\Desktop'
elif manageSSH.run_action(ssh, 'uname').read().decode() == 'Linux\n':
    OTHER_OS_PLATFORM = 'linux'
    cur_path = manageSSH.run_action(ssh, 'pwd').read().decode().replace('\n', '')
elif manageSSH.run_action(ssh, 'uname').read().decode() == 'Darwin\n':
    OTHER_OS_PLATFORM = 'macos'
    cur_path = manageSSH.run_action(ssh, 'pwd').read().decode().replace('\n', '')
else:
    OTHER_OS_PLATFORM = 'else'


# cur_path = '/home/yaniv'
# cur_path = r'C:\Users\yaniv'

if OTHER_OS_PLATFORM == 'windows':
    _, cur_dir, _ = manageSSH.cmd_terminal(ssh, 'cd')
    dir_sign = '\\'
else:
    _, cur_dir, _ = manageSSH.cmd_terminal(ssh, 'pwd')
    dir_sign = '/'
cur_dir = cur_dir.read().decode().replace('\n', '').replace('\r', '') + '>'


def open_cmd_terminal():
    global row, line, list_count, button_count
    row = 0
    line = 1.0
    list_count = 0
    button_count = 0
    cmnds_list = list()
    text_box_dict = dict()

    def up_key(event):
        global list_count, button_count
        print('up_key')
        if abs(list_count) < len(cmnds_list):
            print('yes')
            list_count -= 1
            text_box_dict[f'{button_count}_input'].delete('1.0', 'end')
            text_box_dict[f'{button_count}_input'].insert('1.0', cmnds_list[list_count])

    def down_key(event):
        global list_count, button_count
        print('up_key')
        if abs(list_count) < len(cmnds_list):
            print('yes')
            list_count += 1
            text_box_dict[f'{button_count}_input'].delete('1.0', 'end')
            text_box_dict[f'{button_count}_input'].insert('1.0', cmnds_list[list_count])

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
        if cmnd != '':
            cmnd_lines = math.ceil(len(cmnd) / 59)
            row += cmnd_lines
            cmnds_list.append(cmnd)

            while cmnd.startswith(' '):
                cmnd = cmnd[1:]
            if cmnd.startswith('cd '):
                stderr = ''
                stdout = manageSSH.chdir(sftp, cur_dir.replace('>', '') + dir_sign + cmnd[3:].replace('\n', ''))
                if stdout == 'path not found':
                    stderr = 'The system cannot find the path specified.'
                stdout = ''
            else:
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

        text_box_dict[f'{button_count}_answer'] = Text(sec_frame, bg='grey', bd='0', fg='white', blockcursor=True,
                                                       insertbackground='white',
                                                       selectforeground='black', selectbackground='white',
                                                       font=('Arial', calc_width(14)),
                                                       width=55,
                                                       height=answer_lines)
        text_box_dict[f'{button_count}_answer'].insert('end', print_msg)
        text_box_dict[f'{button_count}_answer'].configure(state=DISABLED)
        text_box_dict[f'{button_count}_answer'].grid(row=row, column=1, sticky=NW)

        row += answer_lines

        if OTHER_OS_PLATFORM == 'windows':
            _, cur_dir, _ = manageSSH.cmd_terminal(ssh, 'cd')
        else:
            _, cur_dir, _ = manageSSH.cmd_terminal(ssh, 'pwd')

        cur_dir = cur_dir.read().decode().replace('\n', '').replace('\r', '') + '>'

        text_box_dict[f'{button_count}_label'] = Label(sec_frame, bg='black', fg='green', text=cur_dir,
                                                       font=('Arial', calc_width(14)))
        text_box_dict[f'{button_count}_label'].grid(row=row, column=0, sticky=NW)

        popup.update()
        text_box_dict[f'{button_count}_input'] = Text(sec_frame, bg='black', bd='0', fg='white', blockcursor=True,
                                                      insertbackground='white',
                                                      selectforeground='black', selectbackground='white',
                                                      font=('Arial', calc_width(14)),
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

    sftp = ssh.open_sftp()
    popup_width = calc_width(800)
    popup_height = calc_height(400)
    popup_x = int((screen_width - popup_width) / 2)
    popup_y = int((screen_height - popup_height) / 2)
    popup = Toplevel(bg='black')
    popup.geometry(f'{popup_width}x{popup_height}+{popup_x}+{popup_y}')
    popup.iconbitmap('icon.ico')
    popup.resizable(False, False)

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
    scroll_canvas.bind(('<Configure>', lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))))

    sec_frame = Frame(scroll_canvas, bg='black')
    scroll_canvas.create_window((0, 0), window=sec_frame, anchor=NW)

    def reset_scrollregion(event):
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))

    sec_frame.bind("<Configure>", reset_scrollregion)


    if OTHER_OS_PLATFORM == 'windows':
        popup.title('CMD')
        _, cur_dir, _ = manageSSH.cmd_terminal(ssh, 'cd')
    else:
        popup.title('Terminal')
        _, cur_dir, _ = manageSSH.cmd_terminal(ssh, 'pwd')
    cur_dir = cur_dir.read().decode().replace('\n', '').replace('\r', '') + '>'

    text_box_dict[f'{button_count}_label'] = Label(sec_frame, bg='black', fg='green', text=cur_dir,
                                                   font=('Arial', calc_width(14)))
    text_box_dict[f'{button_count}_label'].grid(row=row, column=0, sticky=NW)
    popup.update()

    text_box_dict[f'{button_count}_input'] = Text(sec_frame, bg='black', bd='0', fg='white', blockcursor=True,
                                                  insertbackground='white',
                                                  selectforeground='black', selectbackground='white',
                                                  font=('Arial', calc_width(14)), width=math.floor(
            70 - text_box_dict[f'{button_count}_label'].winfo_width() / 12) - 2, height=18,
                                                  wrap=CHAR)
    text_box_dict[f'{button_count}_input'].grid(row=row, column=1, sticky=NW)

    text_box_dict[f'{button_count}_input'].focus()
    text_box_dict[f'{button_count}_input'].bind('<Up>', up_key)
    text_box_dict[f'{button_count}_input'].bind('<Down>', down_key)
    text_box_dict[f'{button_count}_input'].bind('<Return>', enter_key)


    popup.mainloop()

    sftp.close()


open_cmd_terminal()
