"""
author: Hanbing Guo
data: 2020/5/4
"""

import os
import os.path as op
import shutil
from tqdm import tqdm
from numpy import fliplr, flipud
import random
from utils import gen_file_name

dst_path = './mix_test'
root_path = '/home/hbguo/Pictures/pill/'
good_path = 'good/'
bad_path = 'bad/'

pill_type = 'green'

mix_test_path = op.join(dst_path, pill_type)

if os.path.exists(mix_test_path):
    shutil.rmtree(mix_test_path)
    os.makedirs(mix_test_path)
else:
    os.makedirs(mix_test_path)

good_name_list = os.listdir(op.join(root_path, good_path, pill_type))

good_name_list = [x for x in good_name_list if x.split('.')[1] == 'bmp']

bad_name_list = os.listdir(op.join(root_path, bad_path, pill_type))

bad_name_list = [x for x in bad_name_list if x.split('.')[1] == 'bmp']

count = 0

random.shuffle(good_name_list)
random.shuffle(bad_name_list)

for name in good_name_list:
    out_name, count = gen_file_name(count)
    shutil.copy(op.join(root_path, good_path, pill_type, name), op.join(mix_test_path, 'good_' + out_name))
    if count > 100:
        break

count = 0
for name in bad_name_list:
    out_name, count = gen_file_name(count)
    shutil.copy(op.join(root_path, bad_path, pill_type, name), op.join(mix_test_path, 'bad_' + out_name))
    if count > 100:
        break

