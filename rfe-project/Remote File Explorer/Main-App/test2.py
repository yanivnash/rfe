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


# OTHER_OS_PLATFORM = 'linux'
OTHER_OS_PLATFORM = 'windows'

username = 'yaniv'
ssh = manageSSH.connect_to_ssh('192.168.1.20', username, 'Yanivn911911')

# cur_path = '/home/yaniv'
cur_path = r'C:\Users\yaniv'

def open_cmd_terminal():
    global row, line, count
    row = 0
    line = 1.0
    count = 0
    cmnds_list = list()
    def up_key(event):
        global count
        print('up_key')
        count -= 1
        # print(text_box.get(text_box.index('linestart'), 'end'))

    def enter_key(event):
        global row, line, count, cur_dir
        line += 1.0
        row += 1
        count = 0
        print(f'line={line}')
        print('enter_key')
        p = str(float(text_box.index('end')) - 1.0)
        print(p)
        cmnd = text_box.get('end-1l', 'end')
        cmnd = cmnd[cmnd.find('>') + 1:].replace('\n', '')
        print(f'cmnd={cmnd}')
        if cmnd != '':
            cmnd_lines = math.ceil(len(cmnd) / 59)
            row += cmnd_lines
            event.widget.configure(height=cmnd_lines, state=DISABLED)
            cmnds_list.append(cmnd)

            # stdin, stdout, stderr = manageSSH.cmd_terminal(ssh, cmnd)#.read().decode().replace('\n', '')
            #
            # stdout = stdout.read().decode()
            # # stdout.replace('\n', '')
            #
            # stderr = stderr.read().decode()
            # # stderr.replace('\n', '')

            stdout = 'gggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggLGGGGGL'
            stderr = ''#'error'
            answer_lines = 0
            if stdout != '':
                answer_lines += math.ceil(len(stdout) / 72)
            if stderr != '':
                answer_lines += math.ceil(len(stderr) / 72)

            answer_text = Text(popup, bg='grey', bd='0', fg='white', blockcursor=True, insertbackground='white',
                     selectforeground='black', selectbackground='white', font=('Arial', calc_width(14)),
                     width=65, height=answer_lines)
            answer_text.insert('end', f'{stdout}\n{stderr}')
            answer_text.configure(state=DISABLED)
            answer_text.grid(row=row, column=0, sticky=NW)

            row += answer_lines

        if OTHER_OS_PLATFORM == 'windows':
            _, cur_dir, _ = manageSSH.cmd_terminal(ssh, 'cd')
        else:
            _, cur_dir, _ = manageSSH.cmd_terminal(ssh, 'pwd')
        cur_dir = cur_dir.read().decode().replace('\n', '') + '>'
        t = Text(popup, bg='black', bd='0', fg='green', blockcursor=True, insertbackground='white',
                 selectforeground='black', selectbackground='white', font=('Arial', calc_width(14)),
                 width=len(cur_dir) - 3, height=1)
        t.insert('end', cur_dir)
        t.configure(state=DISABLED)
        t.grid(row=row, column=0, sticky=NW)

        text = Text(popup, bg='grey90', bd='0', fg='white', blockcursor=True, insertbackground='white',
                    selectforeground='black', selectbackground='white', font=('Arial', calc_width(14)),
                    width=78 - len(cur_dir) - 3, height=18, wrap=CHAR)
        text.grid(row=row, column=1, sticky=NW)

        text.focus()
        text.bind('<Up>', up_key)
        text.bind('<Return>', enter_key)
        text.bind('<Control-c>', ctrl_c)

    def ctrl_c(event):
        print('ctrl_c')

    sftp = ssh.open_sftp()
    popup_width = calc_width(800)
    popup_height = calc_height(400)
    popup_x = int((screen_width - popup_width) / 2)
    popup_y = int((screen_height - popup_height) / 2)
    popup = Toplevel(bg='black')
    popup.geometry(f'{popup_width}x{popup_height}+{popup_x}+{popup_y}')
    popup.iconbitmap('icon.ico')
    popup.resizable(False, False)

    if OTHER_OS_PLATFORM == 'windows':
        popup.title('CMD')
        _, cur_dir, _ = manageSSH.cmd_terminal(ssh, 'cd')
    else:
        popup.title('Terminal')
        _, cur_dir, _ = manageSSH.cmd_terminal(ssh, 'pwd')
    cur_dir = cur_dir.read().decode().replace('\n', '') + '>'

    # manageSSH.chdir(sftp, cur_path)
    # cur_dir = sftp.getcwd() + '>'

    t = Text(popup, bg='black', bd='0', fg='green', blockcursor=True, insertbackground='white',
                    selectforeground='black', selectbackground='white', font=('Arial', calc_width(14)), width=len(cur_dir) - 3, height=1)
    t.insert('end', cur_dir)
    t.configure(state=DISABLED)
    t.grid(row=row, column=0, sticky=NW)


    text_box = Text(popup, bg='grey90', bd='0', fg='white', blockcursor=True, insertbackground='white',
                    selectforeground='black', selectbackground='white', font=('Arial', calc_width(14)), width=78 - len(cur_dir) - 3, height=18, wrap=CHAR)
    text_box.grid(row=row, column=1, sticky=NW)

    # manageSSH.chdir(sftp, cur_path)
    # cur_dir = sftp.getcwd()

    text_box.focus()
    text_box.bind('<Up>', up_key)
    text_box.bind('<Return>', enter_key)
    text_box.bind('<Control-c>', ctrl_c)

    # text_box.insert(line, f'{cur_dir}>\n')
    # text_box.mark_set('insert', f'{line} lineend')
    # text_box.tag_add('green-text', line, f'{line} lineend')
    # text_box.tag_configure('green-text', foreground='green')

    # print(text_box.index('end'))
    # p = str(float(text_box.index('end')) - 1)
    # print(p)
    # print(text_box.get(text_box.index('end'), 'end'))

    popup.mainloop()
    sftp.close()


open_cmd_terminal()
