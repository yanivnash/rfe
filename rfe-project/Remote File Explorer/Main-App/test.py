from tkinter import *
import wx
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
    global line
    line = 2.0
    def up_key(event):
        print('up_key')
        # print(text_box.get(text_box.index('linestart'), 'end'))

    def enter_key(event):
        global line, cur_dir
        line += 1.0
        # text_box.mark_set('insert', line - 1)
        print(f'line={line}')
        print('enter_key')
        p = str(float(text_box.index('end')) - 1.0)
        print(p)
        cmnd = text_box.get('end-1l', 'end')
        cmnd = cmnd[cmnd.find('>') + 1:].replace('\n', '')
        print(f'cmnd={cmnd}')
        # if cmnd != '':
        #     stdin, stdout, stderr = manageSSH.cmd_terminal(ssh, cmnd)#.read().decode().replace('\n', '')
        #
        #     stdout = stdout.read().decode()
        #     # stdout.replace('\n', '')
        #
        #     stderr = stderr.read().decode()
        #     # stderr.replace('\n', '')
        #
        #     text_box.insert('end', stdout)
        #     text_box.insert('end', stderr)
        text_box.insert('end', 'answer')  # TEMP

        if OTHER_OS_PLATFORM == 'windows':
            _, cur_dir, _ = manageSSH.cmd_terminal(ssh, 'cd')
        else:
            _, cur_dir, _ = manageSSH.cmd_terminal(ssh, 'pwd')
        cur_dir = cur_dir.read().decode().replace('\n', '')
        # text_box.mark_set('insert', line)

        text_box.insert(line + 1, f'{cur_dir}>')
        text_box.mark_set('insert', f'{line} lineend')

        # text_box.insert(line, f'{cur_dir}>')
        # text_box.mark_set('insert', f'{line}-1c')

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
    # popup.resizable(False, False)
    text_box = Text(popup, bg='black', bd='0', fg='white', blockcursor=True, insertbackground='white',
                    selectforeground='black', selectbackground='white', font=('Arial', calc_width(14)))
    text_box.place(x=0, y=0, width=calc_width(800), height=calc_height(400))
    manageSSH.chdir(sftp, cur_path)
    cur_dir = sftp.getcwd()

    text_box.focus()
    text_box.bind('<Up>', up_key)
    text_box.bind('<Return>', enter_key)
    text_box.bind('<Control-c>', ctrl_c)
    if OTHER_OS_PLATFORM == 'windows':
        popup.title('CMD')
    else:
        popup.title('Terminal')
    text_box.insert(line, f'\n{cur_dir}>')
    text_box.mark_set('insert', f'{line} lineend')
    text_box.tag_add('green-text', line, f'{line} lineend')
    text_box.tag_configure('green-text', foreground='green')

    # print(text_box.index('end'))
    # p = str(float(text_box.index('end')) - 1)
    # print(p)
    # print(text_box.get(text_box.index('end'), 'end'))

    popup.mainloop()
    sftp.close()


open_cmd_terminal()
