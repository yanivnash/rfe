# make a popup screen with an entry

import tkinter
from tkinter import simpledialog

def get_me():
    s = simpledialog.askstring('input string', 'please enter your name')
    if s == None:
        print('out')
    else:
        print(s)
root = tkinter.Tk()

button = tkinter.Button(root, text='popup', command=get_me)
button.pack()

root.geometry('300x300')
root.mainloop()