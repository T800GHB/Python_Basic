"""
author: Hanbing Guo
data: 2020/4/30
"""

import shutil
import os
import os.path as op

src_root = './data/green/'
bad_path = 'bad'
good_path = 'good'
dst_path = './data/test_set'
good_result_path = op.join(dst_path, good_path)
bad_result_path = op.join(dst_path, bad_path)

if os.path.exists(good_result_path):
    shutil.rmtree(good_result_path)
    os.makedirs(good_result_path)
else:
    os.makedirs(good_result_path)


if os.path.exists(bad_result_path):
    shutil.rmtree(bad_result_path)
    os.makedirs(bad_result_path)
else:
    os.makedirs(bad_result_path)

with open(op.join(src_root, 'test.txt'), 'r') as fh:
    test_list = fh.readlines()

good_list = []
bad_list = []
for line in test_list:
    name, label = line.split()
    name = name.split('/')[1]
    if label == '0':
        good_list.append(name)
        shutil.copy(op.join(src_root, good_path, name), op.join(good_result_path, name))
    else:
        bad_list.append(name)
        shutil.copy(op.join(src_root, bad_path, name), op.join(bad_result_path, name))

with open(op.join(dst_path, 'good_test_list.txt'), 'w') as fh:
    for name in good_list:
        fh.writelines(name + '\n')

with open(op.join(dst_path, 'bad_test_list.txt'), 'w') as fh:
    for name in bad_list:
        fh.writelines(name + '\n')

