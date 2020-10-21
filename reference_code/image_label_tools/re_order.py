"""
Created on Wed Apr 26 16:46:24 2017

@author: andrew
"""

import os
import os.path as op
import shutil

src_root = './left'
dst_root = 'reorder_images'


if op.exists(dst_root):
    shutil.rmtree(dst_root)
    os.makedirs(dst_root)
else:
    os.makedirs(dst_root)
    
list_images = os.listdir(src_root)
list_images = [x for x in list_images if op.isfile(op.join(src_root,x))]

extension = list_images[0].split('.')[1]

num_images = len(list_images)
pad_char = '0'
count = 0


max_name_length = len(str(num_images))
for f in list_images:
    num_pad = max_name_length - len(str(count))
    new_name = num_pad * pad_char + str(count) + '.' +  extension
    os.rename(op.join(src_root, f), op.join(dst_root, new_name))
    count += 1
