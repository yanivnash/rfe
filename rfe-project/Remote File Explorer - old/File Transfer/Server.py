import socket
import os.path


# s = socket.socket()
# IP = socket.gethostbyname(socket.gethostname())
# PORT = 5050
FORMAT = 'utf-8'
# s.bind((IP, PORT))
# s.listen(5)

file_path = input("Enter the file's path: ")
print([file_path])
file_path = file_path.replace(r'\\', '\\')
print(r'\\')
print('\\')
print([file_path])
if os.path.isfile(file_path):
    end_index = file_path.rfind('.')
    file_ending = file_path[end_index:]
    if file_ending[-1] == r'\\':
        file_ending = file_ending[:len(file_ending) - 2]
    print(file_ending)
else:
    file_path = file_path.replace('\\\\', '\\')
    os.chdir(file_path)
    print('Enter one file from the list:')
    files_list = os.listdir()
    print(*files_list, sep='\n')
    file_selected = input('')

# print('Listening for connections...')
# conn, addr = s.accept()
# conn.send(file_ending.encode(FORMAT))
#
# with open('testing.docx', 'rb') as video:
#     vid_info = video.read()
#     print(vid_info)
#     conn.sendall(vid_info)
#
# s.close()