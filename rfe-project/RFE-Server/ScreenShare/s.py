from vidstream import StreamingServer
import threading

receiver = StreamingServer('192.168.1.20', 9999, 8, 'e')

t = threading.Thread(target=receiver.start_server)
t.start()

while input('') != 'STOP':
    continue

receiver.start_server()