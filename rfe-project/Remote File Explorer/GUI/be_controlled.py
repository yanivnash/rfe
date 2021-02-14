import tkinter as tk

def entry_click(event):
    entry.delete(0, 'end')
    print("FocusIn")
    entry.bind("<FocusOut>", entry_lost)

def entry_lost(event):
    entry.insert(0, 'Search')
    print("FocusOut")
    entry.bind("<FocusIn>", entry_click)

root = tk.Tk()
entry = tk.Entry(root)
entry.insert(0, 'Search')
entry.pack(fill="x")
tk.Button(root).pack()
entry1 = tk.Entry(root)
entry1.pack(fill="x")

entry.bind("<FocusIn>", entry_click)

root.mainloop()