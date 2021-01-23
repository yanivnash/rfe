# import tkinter
# import threading
# import imageio
# from PIL import Image, ImageTk
#
# # global app_width, app_height
# app_width = 1070
# app_height = 700
# # video_name = r"D:\כיתה יב - D\10 יחידות מחשבים\cyber project\new animation\fin\fin\1.mp4" #This is your video file path
# # video_name = 'start-animation.mp4'
# # video = imageio.get_reader(video_name)
#
# def play_video(video_name):
#     global video
#     video = imageio.get_reader(video_name)
#     vid_frame = tkinter.Frame(root)
#     vid_frame.place(x=0, y=0, width=app_width, height=app_height)
#     vid_label = tkinter.Label(vid_frame)
#     vid_label.place(x=0, y=0, width=app_width, height=app_height)
#     thread = threading.Thread(target=stream, args=(vid_label, vid_frame))
#     thread.daemon = 1
#     thread.start()
#
# count = 0
# def stream(vid_label, vid_frame):
#     global count
#     for image in video.iter_data():
#         frame_image = ImageTk.PhotoImage(Image.fromarray(image).resize((app_width, app_height),Image.ANTIALIAS))
#         vid_label.config(image=frame_image)
#         vid_label.image = frame_image
#         count += 1
#         print(count)
#         if count == 20:
#             vid_frame.destroy()
#
#
# if __name__ == "__main__":
#     root = tkinter.Tk()
#     root.geometry(f'{app_width}x{app_height}')
#     frame2 = tkinter.Frame(root)
#     frame2.place(x=0, y=0, width=app_width, height=app_height)
#     bg = tkinter.PhotoImage(file='background.png')
#     bg_image = tkinter.Label(frame2, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
#     video_name = 'start-animation.mp4'
#     play_video(video_name)
#     # from time import sleep
#     # sleep(5)
#
#
#
#
#     # print(threading.active_count())
#     # if count == 54:
#     #     frame.destroy()
#     root.mainloop()



import tkinter as tk
from tkinter import ttk

root = tk.Tk()
container = ttk.Frame(root)
canvas = tk.Canvas(container)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)
# scrollable_frame = tk.Canvas(canvas)

def mouse_wheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
scrollable_frame.bind_all("<MouseWheel>", mouse_wheel)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

for i in range(50):
    ttk.Label(scrollable_frame, text="Sample scrolling label").pack()

container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

root.mainloop()