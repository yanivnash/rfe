import manageSSH
host = "192.168.1.20"
username = 'yaniv'
password = 'Yanivn911911'  # DELETE
ssh = manageSSH.connect_to_ssh(host, username, password)
print('ok0')
sftp = ssh.open_sftp()

print('ok1')

cur_path = r'C:\Users\yaniv\Desktop'
tree_list = list()
search_key = 'WhatsApp Video 2021-03-15 at 14.45.08.mp4'
list1 = manageSSH.tree_items(sftp, cur_path, tree_list, search_key)

print('ok2')

print(list1)
print(len(list1))