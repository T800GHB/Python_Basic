"""
Created on Tue Jun  6 14:55:53 2017

@author: andrew

Compress a set of images to a video
"""

import cv2
import os
import os.path as op
import shutil
import assist_util

####Initialization
src_dir = './frame/ces'
dst_dir = './video'
video_name = src_dir.split('/')[-1] + '.avi'
dirlist = os.listdir(src_dir)

if op.exists(dst_dir):
    shutil.rmtree(dst_dir)
    os.makedirs(dst_dir)
else:
    os.makedirs(dst_dir)

files = [x for x in dirlist if op.isfile(op.join(src_dir,x))]
files.sort()
num_files = len(files)

frame = cv2.imread(op.join(src_dir, files[0]))

frame_size = (frame.shape[1], frame.shape[0])

####Process
fps = 30
bar_worker = assist_util.process_bar(num_items= len(files))

try:
    writer = cv2.VideoWriter(op.join(dst_dir, video_name), cv2.VideoWriter_fourcc('M','J','P','G') , fps, frame_size)
    
    for f in files:
        bar_worker.update()
        frame = cv2.imread(op.join(src_dir,f))
        writer.write(frame)
except Exception as e:
    print('Something wrong happened ', e)
finally:
    writer.release()

print('\nProcess finished')
