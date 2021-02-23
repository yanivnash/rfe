import socket

s = socket.socket()
IP = socket.gethostbyname(socket.gethostname()) # DEL
# IP = input("Enter the server's ip: ")
PORT = 5050
FORMAT = 'utf-8'
MSG_LEN = 1024

s.connect((IP, PORT))

file_ending = s.recv(MSG_LEN).decode(FORMAT)
print("Receiving video..")

try:
    print("Starting to read bytes..")
    vid_info = s.recv(1024)

    with open('new' + file_ending, 'wb') as video:
        while vid_info:
            video.write(vid_info)
            vid_info = s.recv(MSG_LEN)

    print('Done reading bytes..')
    s.close()

except KeyboardInterrupt:
    if s:
        s.close()

print("Done..")
s.close()