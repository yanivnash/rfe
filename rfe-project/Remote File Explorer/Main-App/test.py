import manageSSH
ssh = manageSSH.connect_to_ssh('192.168.1.20', 'yaniv', '911911')
sftp2 = ssh.open_sftp()
item_path = '/home/yaniv/Desktop/test (copy)'
OTHER_OS_PLATFORM = 'Linux'
tree_list = manageSSH.tree_items(sftp2, item_path, [], '', OTHER_OS_PLATFORM)
temp = tree_list  # when removed from temp, it removes also from tree_list
print(tree_list)
print(len(tree_list))
longest_path = 0
for item in tree_list:
    if item.count('/') > longest_path:
        longest_path = item.count('/')
sorted_items_list = []
while temp != [] and longest_path >= 0:
    for item in tree_list:
        if item.count('/') == longest_path:
            sorted_items_list.append(item)
            temp.remove(item)
    longest_path -= 1
print(sorted_items_list)
print(len(sorted_items_list))
