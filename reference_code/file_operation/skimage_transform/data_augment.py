#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 23:54:08 2020

@author: hbguo
"""

from skimage import io, color, transform, exposure, img_as_ubyte
import os
import os.path as op
import shutil
from tqdm import tqdm
from numpy import fliplr, flipud
import random
from utils import gen_file_name

dst_path = './data'
root_path = '/home/hbguo/Pictures/pill/'
good_path = 'good/'
bad_path = 'bad/'

pill_type = 'green'

good_result_path = op.join(dst_path, pill_type, good_path)

if os.path.exists(good_result_path):
    shutil.rmtree(good_result_path)
    os.makedirs(good_result_path)
else:
    os.makedirs(good_result_path) 
    
bad_result_path = op.join(dst_path, pill_type, bad_path)

if os.path.exists(bad_result_path):
    shutil.rmtree(bad_result_path)
    os.makedirs(bad_result_path)
else:
    os.makedirs(bad_result_path) 


good_name_list = os.listdir(op.join(root_path, good_path, pill_type))

good_name_list = [x for x in good_name_list if x.split('.')[1] == 'bmp']

bad_name_list = os.listdir(op.join(root_path, bad_path, pill_type))

bad_name_list = [x for x in bad_name_list if x.split('.')[1] == 'bmp']


resize_shape = (224, 224, 3)
rotate_degree = 5
brightness_range = 0.2

good_sample_name = []
count = 0
for name in tqdm(good_name_list):
    out_name, count = gen_file_name(count)
    good_sample_name.append(out_name)
    img = io.imread(op.join(root_path, good_path, pill_type, name))
    simg = transform.resize(img, resize_shape)
    io.imsave(op.join(good_result_path, out_name), img_as_ubyte(simg))

    out_name, count = gen_file_name(count)
    good_sample_name.append(out_name)
    io.imsave(op.join(good_result_path, out_name), img_as_ubyte(fliplr(simg)))

    out_name, count = gen_file_name(count)
    good_sample_name.append(out_name)
    io.imsave(op.join(good_result_path, out_name), img_as_ubyte(flipud(simg)))

    out_name, count = gen_file_name(count)
    good_sample_name.append(out_name)
    io.imsave(op.join(good_result_path, out_name), img_as_ubyte(flipud(fliplr(simg))))

    out_name, count = gen_file_name(count)
    good_sample_name.append(out_name)
    io.imsave(op.join(good_result_path, out_name), img_as_ubyte(transform.rotate(simg, rotate_degree)))

    out_name, count = gen_file_name(count)
    good_sample_name.append(out_name)
    io.imsave(op.join(good_result_path, out_name), img_as_ubyte(transform.rotate(simg, -rotate_degree)))

    out_name, count = gen_file_name(count)
    good_sample_name.append(out_name)
    io.imsave(op.join(good_result_path, out_name), img_as_ubyte(exposure.adjust_gamma(simg, 1 + brightness_range)))

    out_name, count = gen_file_name(count)
    good_sample_name.append(out_name)
    io.imsave(op.join(good_result_path, out_name), img_as_ubyte(exposure.adjust_gamma(simg, 1 - brightness_range)))

random.shuffle(good_sample_name)
with open(op.join(dst_path, pill_type, 'good_label.txt'), 'w') as fh:
    for name in good_sample_name:
        fh.writelines(good_path + name + ' 0\n')

count = 0
bad_sample_name = []
for name in tqdm(bad_name_list):
    out_name, count = gen_file_name(count)
    bad_sample_name.append(out_name)
    img = io.imread(op.join(root_path, bad_path, pill_type, name))
    simg = transform.resize(img, resize_shape)
    io.imsave(op.join(bad_result_path, out_name), img_as_ubyte(simg))

    out_name, count = gen_file_name(count)
    bad_sample_name.append(out_name)
    io.imsave(op.join(bad_result_path, out_name), img_as_ubyte(fliplr(simg)))

    out_name, count = gen_file_name(count)
    bad_sample_name.append(out_name)
    io.imsave(op.join(bad_result_path, out_name), img_as_ubyte(flipud(simg)))

    out_name, count = gen_file_name(count)
    bad_sample_name.append(out_name)
    io.imsave(op.join(bad_result_path, out_name), img_as_ubyte(flipud(fliplr(simg))))

    out_name, count = gen_file_name(count)
    bad_sample_name.append(out_name)
    io.imsave(op.join(bad_result_path, out_name), img_as_ubyte(transform.rotate(simg, rotate_degree)))

    out_name, count = gen_file_name(count)
    bad_sample_name.append(out_name)
    io.imsave(op.join(bad_result_path, out_name), img_as_ubyte(transform.rotate(simg, -rotate_degree)))

    out_name, count = gen_file_name(count)
    bad_sample_name.append(out_name)
    io.imsave(op.join(bad_result_path, out_name), img_as_ubyte(exposure.adjust_gamma(simg, 1 + brightness_range)))

    out_name, count = gen_file_name(count)
    bad_sample_name.append(out_name)
    io.imsave(op.join(bad_result_path, out_name), img_as_ubyte(exposure.adjust_gamma(simg, 1 - brightness_range)))

random.shuffle(bad_sample_name)
with open(op.join(dst_path, pill_type, 'bad_label.txt'), 'w') as fh:
    for name in bad_sample_name:
        fh.writelines(bad_path + name + ' 1\n')
    
# fimg = transform.rescale(img, [0.2, 0.2, 1])
# io.imsave('1.bmp', simg)
# io.imsave('2.jpg', fimg)
# img1 = io.imread('1.bmp')
# io.imshow(fimg)
# io.show()

