"""
author: Hanbing Guo
data: 2019/8/8
"""
import os
import os.path as op

src_root = './contour'

file_names = os.listdir(src_root)
print('Number of file: ', len(file_names))
useful_list = []
del_list = []
for file in file_names:
    if op.getsize(op.join(src_root, file)):
        useful_list.append(file)
    else:
        del_list.append(file)


# useful_list.sort()
# useful_list.reverse()
print('Number of left: ', len(file_names) - len(del_list))

for name in del_list:
    os.remove(op.join(src_root, name))

base_names = [x.split('.')[0] for x in useful_list]
base_names.sort()

with open('file_list.txt', 'w') as fh:
    for name in base_names:
        fh.writelines(name + '\n')



