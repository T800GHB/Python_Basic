"""
author: Hanbing Guo
data: 2020/4/23
"""

from skimage import io, color, transform
import os
import os.path as op

root_path = '/home/hbguo/Pictures/pill/'
good_path = 'good'
bad_path = 'bad'

pill_type = 'green'

name_list = os.listdir(op.join(root_path, bad_path, pill_type))

name_list = [x for x in name_list if x.split('.')[1] == 'bmp']

img = io.imread(op.join(root_path, bad_path, pill_type, name_list[0]))

print(img.shape)
img[200: 600, 300: 700, :] = 0
io.imshow(img)
io.show()
