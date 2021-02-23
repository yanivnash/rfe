import tkinter
from tkinter import ttk
import os
from PIL import ImageTk, Image
import tkinter.messagebox
from tkinter import simpledialog  # opens the popup for the new folder name input
import pyperclip # copy to clipboard module
import win32api  # a module that shows the drives that are connected to the PC

global cur_path, ROOT_PROJ_DIR, bttns_dict, icons_dict

bttns_dict = dict()
icons_dict = dict()

ROOT_PROJ_DIR = os.path.dirname(os.path.abspath(__file__))

# cur_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# cur_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\apple')
# cur_path = r'C:\Users\yaniv\Desktop\כיתה יב\10 יחידות מחשבים\cyber project'
# cur_path = r'D:\Program Files\obs-studio\screen records'
cur_path = r'C:\Users\yaniv\Desktop\Remote File Explorer'

def create_icons_dict():
    icons_list = os.listdir(f'{ROOT_PROJ_DIR}\\icons')
    for icon in icons_list:
        icons_dict[icon] = ImageTk.PhotoImage(Image.open(f'{ROOT_PROJ_DIR}\\icons\\{icon}'))#.resize((61, 50),Image.ANTIALIAS))

def set_imgs():
    # DELETE - NOT GOOD
    imgs_list = os.listdir(r'files icons')
    # os.chdir(r'files icons')
    imgs_dict = dict()
    for img in imgs_list:
        end_index = img.rfind('.png')
        img_name = img[:end_index]
        imgs_dict[img_name] = ImageTk.PhotoImage(Image.open(img).resize((61, 50), Image.ANTIALIAS))
    return imgs_dict

def sort_files_list(items_list):
    i = 0
    # items_list.sort() # not sorted when going back
    for item in items_list:
        if os.path.isdir(item):
            items_list.insert(i, items_list.pop(items_list.index(item)))
            i += 1
    return items_list

def create_bttn(frame, items_list):
    global icons_dict, bttns_dict
    clm = 0
    rw = 2
    # os.chdir(r'D:\PycharmProjects\School\Remote File Explorer\GUI\files icons')
    for item in items_list:
        btn_text = item
        if os.path.isdir(item):
            # if 'item' is a directory
            file_type = '.dir_folder' #.png'
            if len(item) > 40:
                btn_text = item[0:41] + '...'

        else:
            # if 'item' is a file
            end_index = item.rfind('.')
            file_type = item[end_index:]# + '.png'

            if len(item) > 40:
                btn_text = item[0:36] + file_type

        # img = ImageTk.PhotoImage(Image.open(ROOT_PROJ_DIR + '\\' + file_type).resize((61, 50), Image.ANTIALIAS))

        # img = imgs_dict[file_ending]
        # photo = ImageTk.PhotoImage(Image.open(r'D:\PycharmProjects\School\Remote File Explorer\GUI\files icons\.dir_folder.png').resize((61, 50), Image.ANTIALIAS))
        # photo.resize((61, 50), Image.ANTIALIAS))

        # photo = icons_dict['.dir_folder.png'] # worked

        try:
            icon = icons_dict[file_type + '.png']
        except KeyError:
            icon = icons_dict['.none.png']
        bttns_dict[f'{item}_btn_{items_list.index(item)}'] = tkinter.Button(frame, bg="gray", wraplength=100, text=btn_text, compound=tkinter.TOP, justify=tkinter.CENTER, image=icon, height=100, width=100)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].grid(column=clm, row=rw, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W, padx=10, pady=10)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind("<Button-1>", left_click)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind("<Button-2>", right_click)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind("<Button-3>", right_click)
        bttns_dict[f'{item}_btn_{items_list.index(item)}'].bind('<Double-Button-1>', handler)
        clm += 1
        if clm == 8:
            clm = 0
            rw += 1

        # for i in range(len(items_list) - 1):
        #     # for item in items_list:
        #     end_index = items_list[i].rfind('.')
        #     file_ending = items_list[i][end_index:]
        #     # button = tkinter.Label(root, background="gray", text=items_list[i])
        #     button = tkinter.Label(frame, background="gray", text=items_list[i])
        #     button.grid(column=clm, row=rw, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W, padx=10, pady=10)
        #     button.bind("<Button-1>", left_click)
        #     button.bind("<Button-2>", right_click)
        #     button.bind("<Button-3>", right_click)
        #     clm += 1
        #     if clm == 8:
        #         clm = 0
        #         rw += 1
        #     i += 1

def handler(event):
    event.widget.configure(bg="yellow")  # DEL
    global items_list, cur_path, frame, bttns_dict

    key_list = list(bttns_dict.keys())
    val_list = list(bttns_dict.values())
    item_name = key_list[val_list.index(event.widget)]
    item_name = item_name[0:item_name.find('_btn_')]

    temp = cur_path + '\\' + item_name
    if os.path.isdir(temp):
        cur_path = temp
        os.chdir(cur_path)
        items_list = os.listdir(cur_path)
        update_frame(items_list)
    if os.path.isfile(temp):
        os.chdir(cur_path)
        os.popen(item_name)

def left_click(event):
    # DELETE THIS FUNC - NO NEED
    event.widget.configure(bg="green")

def right_click(event):
    event.widget.configure(bg="blue")

def dscon_bttn():
    discon_msg_box = tkinter.messagebox.askquestion(title='Disconnect',message='Are you sure you want to disconnect?')
    if discon_msg_box == 'yes':
        pass# add disconnecting form the machine (SSH)

def DELE():
    # DELETE THIS FUNC AND BUTTON
    root.destroy()

def up_button():
    global items_list, cur_path, frame
    cur_path = os.path.dirname(os.getcwd())
    root.title(cur_path)
    if os.path.isdir(cur_path):
        os.chdir(cur_path)
        items_list = os.listdir(cur_path)
        update_frame(items_list)

def forward_button():
    # wrapper2.update() # not working - maybe wont use update()
    # save the current folder when back is pressed then go back to that folder when forward is clicked
    # new_button = tkinter.Button(frame, bg="gray", wraplength=100, compound=tkinter.TOP, justify=tkinter.CENTER, height=100, width=100)
    new_button = tkinter.Button(frame, bg="gray", height=100, width=100)
    new_button.grid(column=5, row=3)#, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W, padx=10, pady=10)
    # entry_in_button = tkinter.Entry(new_button)#, text='New folder')
    # entry_in_button.insert(tkinter.END, 'New folder')
    # entry_in_button.pack()

def refresh_button():
    root.title(cur_path) # temp
    os.chdir(cur_path)
    items_list = os.listdir(cur_path)
    update_frame(items_list)

def drives_box_change(event):
    root.title(event.widget.get())

def close_window():
    discon_msg_box = tkinter.messagebox.askquestion(title='Disconnect & Close', message='Are you sure you want to close the window and disconnect?')
    if discon_msg_box == 'yes':
        root.destroy() # add disconnecting form the machine (SSH)

def copy_path_button(event):
    # import time
    pyperclip.copy(cur_path)

    # doesnt work
    # event.widget.configure(text='Copied!')
    # time.sleep(1)
    # event.widget.configure(text='Copy Path2')

def new_dir_button():
    # Get the name of the folder with entry
    items_list = os.listdir(cur_path)
    lower_list = list()
    for item in items_list:
        lower_list.append(item.lower())

    # while True:
    #     new_folder_name = simpledialog.askstring('input string', 'please enter your name')
    #     if new_folder_name == None:
    #         break
    #     try:
    #         os.mkdir(f'{cur_path}\\{new_folder_name}')
    #     except FileExistsError:
    #         if new_folder_name # contains only dots (.) maybe use regex
    #     msg = os.system(f'mkdir "{cur_path}\\{new_folder_name}"')



    new_folder_name = simpledialog.askstring('input string', 'please enter a name')

    msg = 1
    while msg == 1:
        # new_folder_name = input('Enter a name for the folder: ')
        if new_folder_name == None:
            break
        msg = os.system(f'mkdir "{cur_path}\\{new_folder_name}"')
        if msg == 0:
            break
        new_folder_name = simpledialog.askstring('input string', 'please enter your name')

    while new_folder_name.lower() in lower_list:
        if new_folder_name.endswith(')'):
            if new_folder_name[new_folder_name.index(')')].isdigit():
                count = new_folder_name[new_folder_name.index(')')]
                count += 1
                old_folder_name = new_folder_name[0:(new_folder_name.index(f'({count})')) - 1]
                new_folder_name = f'{old_folder_name} ({str(count)})'
            else:
                new_folder_name = f'{new_folder_name} ({count})'



    # os.mkdir(cur_path + '\\' + new_folder_name)

    # do these two lines only if the name is fine and the name isn't None
    # (the window was closed = the user doesn't want to create a new folder)
    items_list = os.listdir(cur_path)
    update_frame(items_list)
    # these 2 lines above

def update_frame(items_list):
    # global back_img, forw_img, ref_img
    items_list = sort_files_list(items_list)
    wrapper1.destroy()
    wrapper2.destroy()
    frame.destroy()
    create_frame()#back_img, forw_img, ref_img)
    create_bttn(frame, items_list)

def create_frame():#back_img, forw_img, ref_img):
    global frame, wrapper1, wrapper2, count

    count = 0
    def mouse_wheel(event):
        global count
        # respond to Linux or Windows wheel event
        if event.num == 5 or event.delta == -120:
            count -= 1
        if event.num == 4 or event.delta == 120:
            count += 1
        mycanvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    wrapper1 = tkinter.LabelFrame(root, height=10)
    wrapper2 = tkinter.LabelFrame(root)

    # tkinter.Grid.columnconfigure(wrapper1, 5, weight=1)
    # tkinter.Grid.rowconfigure(wrapper1, 5, weight=1)

    mycanvas = tkinter.Canvas(wrapper2)
    mycanvas.pack(side=tkinter.LEFT, fill='both', expand='yes')

    yscrollbar = ttk.Scrollbar(wrapper2, orient='vertical', command=mycanvas.yview)
    yscrollbar.pack(side=tkinter.RIGHT, fill='y')

    yscrollbar.config(command=mycanvas.yview)

    mycanvas.configure(yscrollcommand=yscrollbar.set)

    mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
    mycanvas.bind_all("<MouseWheel>", mouse_wheel)
    # mycanvas.bind('<Configure>', lambda e: mycanvas.configure(scrollregion=mycanvas.bbox('all')))
    # yscrollbar.bind('<Configure>', lambda e: yscrollbar.configure(scrollregion=yscrollbar.bbox('all')))

    # scrollbar = tkinter.Scrollbar(root)
    # scrollbar.grid(column=0, row=1, sticky=tkinter.W)#, fill=tkinter.Y)#, side=tkinter.RIGHT)
    # scrollbar.bind("<MouseWheel>", on_mouse_wheel)

    # frame = tkinter.Frame(mycanvas)
    # mycanvas.create_window((0, 0), window=frame, anchor='nw')

    frame = tkinter.Frame(mycanvas)
    mycanvas.create_window((0, 0), window=frame, anchor='nw')

    wrapper1.pack(fill='both', expand='no', padx=10, pady=10)
    wrapper2.pack(fill='both', expand='yes', padx=10, pady=10)
    # wrapper1.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
    # wrapper2.grid(column=0, row=1, padx=10, pady=10, sticky='nsew')

    # good
    tkinter.Grid.columnconfigure(wrapper1, 0, weight=1)
    tkinter.Grid.rowconfigure(wrapper1, 0, weight=1)
    # good

    # wrapper1.grid(padx=10, pady=10, rowspan=50)
    # wrapper2.grid(padx=10, pady=10, rowspan=50)

    # good
    # frame = tkinter.Frame(mycanvas)# old had 'root'
    # tkinter.Grid.rowconfigure(root, 1, weight=1)
    # tkinter.Grid.columnconfigure(root, 0, weight=1)
    # frame.grid(column=0, row=1, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
    # grid = tkinter.Frame(frame)
    # grid.grid(sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W, column=0, row=7, columnspan=2)
    # tkinter.Grid.rowconfigure(frame, 7, weight=1)
    # tkinter.Grid.columnconfigure(frame, 0, weight=1)


    # scrollbar.config(command=frame.yview)

    # f1 = tkinter.Frame(root, height=50)
    # f1.grid(column=0, row=0)#, columnspan=100)

    # # set to be scrollable (change buttons to be in the new frame)
    # # https://blog.tecladocode.com/tkinter-scrollable-frames/
    # canvas = tkinter.Canvas(frame)
    # scrollbar = tkinter.ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    # scrollable_frame = ttk.Frame(canvas)



    menu_window = wrapper1 # f1

    cur_path_label = tkinter.Label(menu_window, text=cur_path)
    cur_path_label.grid(column=3, row=0, sticky=tkinter.W + tkinter.E)

    copy_btn = tkinter.Button(menu_window, text='Copy Path')
    copy_btn.bind("<Button-1>", copy_path_button)
    copy_btn.grid(column=4, row=0, sticky=tkinter.W)# + tkinter.E)

    up_btn = tkinter.Button(menu_window, image=icons_dict['up.png'], command=up_button)
    up_btn.grid(column=0, row=1)

    # forw_btn = tkinter.Button(menu_window, image=icons_dict['forward.png'], command=forward_button)
    # forw_btn.grid(column=1, row=1)

    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    drivers_combobox = ttk.Combobox(menu_window, values=drives)
    default_value = cur_path[0:3]
    drivers_combobox.current(drives.index(default_value))
    drivers_combobox.bind("<<ComboboxSelected>>", drives_box_change)
    drivers_combobox.grid(column=2, row=1)

    new_dir_btn = tkinter.Button(menu_window, text='New folder', compound=tkinter.TOP, justify=tkinter.CENTER, image=icons_dict['new_dir.png'], command=new_dir_button)
    # new_dir_btn = tkinter.Button(menu_window, image=icons_dict['new_dir.png'], text='New folder', command=new_dir_button, height=100, width=100)
    new_dir_btn.grid(column=3, row=1)

    ref_btn = tkinter.Button(menu_window, image=icons_dict['refresh.png'], command=refresh_button)
    ref_btn.grid(column=4, row=1)

    ds_btn = tkinter.Button(menu_window, text='Disconnect', command=dscon_bttn)
    ds_btn.grid(column=5, row=1, sticky=tkinter.E, padx=50, columnspan=4)

    # DEL
    DEL = tkinter.Button(menu_window, text='DELETE', command=DELE)
    DEL.grid(column=6, row=1, sticky=tkinter.E, padx=25, columnspan=5)
    # DEL

    for x in range(10):
        tkinter.Grid.columnconfigure(frame, x, weight=1)

    for y in range(5):
        tkinter.Grid.rowconfigure(frame, y, weight=1)

    for x in range(10):
        tkinter.Grid.columnconfigure(wrapper1, x, weight=1)

    # for y in range(3):
    #     tkinter.Grid.rowconfigure(wrapper1, y, weight=1)

    # return frame

if __name__ == '__main__':
    global frame
    root = tkinter.Tk()
    root.protocol("WM_DELETE_WINDOW", close_window)
    root.geometry('1070x700')
    root.minsize(width=1070, height=700)

    # root.resizable(False, False)

    # # open a new window and close the old one
    # root.destroy()
    # window2 = tkinter.Tk()
    # window2.geometry('1000x700')
    # window2.mainloop()

    create_icons_dict()

    # back_img = ImageTk.PhotoImage(Image.open(ROOT_PROJ_DIR + '\\' + 'icons' + '\\' + 'back.png'))#.resize((57, 44), Image.ANTIALIAS))
    # forw_img = ImageTk.PhotoImage(Image.open(ROOT_PROJ_DIR + '\\' + 'icons' + '\\' + 'forward.png'))#.resize((57, 44), Image.ANTIALIAS))
    # ref_img = ImageTk.PhotoImage(Image.open(ROOT_PROJ_DIR + '\\' + 'icons' + '\\' + 'refresh.png'))#.resize((50, 50), Image.ANTIALIAS))
    create_frame()#back_img, forw_img, ref_img)

    # IN A FUNC
    # frame = tkinter.Frame(root)
    # tkinter.Grid.rowconfigure(root, 0, weight=1)
    # tkinter.Grid.columnconfigure(root, 0, weight=1)
    # frame.grid(row=0, column=0, sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W)
    # grid = tkinter.Frame(frame)
    # grid.grid(sticky=tkinter.N + tkinter.S + tkinter.E + tkinter.W, column=0, row=7, columnspan=2)
    # tkinter.Grid.rowconfigure(frame, 7, weight=1)
    # tkinter.Grid.columnconfigure(frame, 0, weight=1)


    # v = tkinter.Scrollbar(root)
    # v.config(command=frame.yview)  # for vertical scrollbar

    root.title('Remote File Explorer')
    root.iconbitmap('icon.ico')
    # img = ImageTk.PhotoImage(Image.open('icon.png').resize((61, 50), Image.ANTIALIAS))
    # pic = tkinter.Label(root, image=img, text='test')
    # pic.grid(column=0, row=0)

    # imgs_dict = set_imgs()


    # # os.chdir('files icons')
    # back_img = ImageTk.PhotoImage(Image.open(ROOT_PROJ_DIR + '\\' + 'back.png').resize((57, 44), Image.ANTIALIAS))
    # back_btn = tkinter.Button(frame, image=back_img, padx=100, pady=100, command=back_btn)
    # back_btn.grid(column=0, row=0)
    #
    # forw_img = ImageTk.PhotoImage(Image.open(ROOT_PROJ_DIR + '\\' + 'forward.png').resize((57, 44), Image.ANTIALIAS))
    # forw_btn = tkinter.Button(frame, image=forw_img, padx=100)
    # forw_btn.grid(column=1, row=0)
    #
    # ref_img = ImageTk.PhotoImage(Image.open(ROOT_PROJ_DIR + '\\' + 'refresh.png').resize((50, 50), Image.ANTIALIAS))
    # ref_btn = tkinter.Button(frame, image=ref_img, command=refresh_btn)
    # ref_btn.grid(column=2, row=0)
    #
    # ds_btn = tkinter.Button(frame, text='Disconnect', command=dscon_bttn)
    # ds_btn.grid(column=3, row=0)
    #
    # # DEL
    # DEL = tkinter.Button(frame, text='DELETE', command=DELE)
    # DEL.grid(column=4, row=0)
    # # DEL


    # cur_path = r'C:\Users\yaniv\Desktop\כיתה יב\10 יחידות מחשבים\cyber project'

    # cur_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    if cur_path.startswith(os.getenv("SystemDrive")):
        os.chdir(cur_path)
    else:
        os.popen(cur_path[0:2])
        os.chdir(cur_path)
    items_list = os.listdir(cur_path)

    # items_list = items_list * 2 # make screen scrollable

    # items_list = ['dir1', 'dir2', 'word.docx', 'pic.png', 'text.txt']

    items_list = sort_files_list(items_list)
    create_bttn(frame, items_list)

    # #IN THE FUNC
    # for x in range(10):
    #     tkinter.Grid.columnconfigure(frame, x, weight=1)
    #
    # for y in range(5):
    #     tkinter.Grid.rowconfigure(frame, y, weight=1)

    root.mainloop()