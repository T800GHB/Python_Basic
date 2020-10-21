#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 25 19:04:20 2017

@author: andrew

This script will decompress tar files in 'tar_set_path' to 
the destination directory 'result_path'

"""

import os 
import shutil

tar_set_path = './tar_set'
tar_set_list = os.listdir(tar_set_path)
tar_set_names = [x.split('.')[0] for x in tar_set_list]
result_path = './result'

#If result_path does not exist, create otherwise empty it
if os.path.exists(result_path):
    shutil.rmtree(result_path)
    os.mkdir(result_path)
else:
    os.mkdir(result_path)
    
for i in tar_set_names:
    dst_path = os.path.join(result_path, i)
    os.mkdir(dst_path)
    os.system('tar -xvf ' + os.path.join(tar_set_path, i + '.tar') 
                + ' -C ' + dst_path)