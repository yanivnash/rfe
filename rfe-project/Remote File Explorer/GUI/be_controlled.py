from tkinter import *
from tkinter import ttk
import time

root = Tk()
root.geometry('500x500')

def start():
    for x in range(20):
        p_bar['value'] += 1
        root.update_idletasks()
        time.sleep(0.1)
    root.update_idletasks()
    time.sleep(2)
    for x in range(200):
        p_bar['value'] += 0.1
        root.update_idletasks()
        time.sleep(0.01)


p_bar = ttk.Progressbar(root, orient=HORIZONTAL, length=400, mode='determinate')
p_bar.pack(pady=20)

bttn = Button(root, text='Start', command=start)
bttn.pack(pady=20)

root.mainloop()