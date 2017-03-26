#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 21:17:11 2017

@author: andrew

This file will contain some demostrate about opencv
"""

import cv2
import numpy as np
import pylab as pl
import shutil
import os

def fill_polygon():
    '''
    Fill the area inside the polygon
    '''
    img = np.zeros((1000,1000), dtype = np.uint8)    
    polygon = np.array([(50,80), (100,30), (200,400),
                        (40,450), (140, 220) ,(70, 150)], np.int32)    
    cv2.fillPoly(img, [polygon],(255))
    
    pl.figure('Fill area')
    pl.gray()
    pl.imshow(img)
    
def video2image(video_path, dst_dir):
    '''
    Save frames in video according to the specific interval
    '''
    videoCapture = cv2.VideoCapture(video_path)


    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    
    frame_size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)),
                  int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    
    total_frame_count = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    print('video file: ', video_path,
          '\nframe size: ', frame_size,
          '\ntotal count of frame: ', total_frame_count,
          '\nframes per second: ', fps)
    
    #Statement below can't work
    #cv2.namedWindow('Video frame')    
    
    success, frame = videoCapture.read()
    #Sometimes, cv2 can't work well, so fps and size of frame can't achive
    if frame_size[0] == 0 and frame_size[1] == 0:
        del frame_size
        #height, width, channels
        frame_size = frame.shape
        
    xfile_name = video_path.split('/')[-1]      #Get video name from path
    file_name = xfile_name.split('.')[0]        #Get basename from video name            
    dst_path = os.path.join(dst_dir, file_name) #Establish destnation path
    #Create a new directory or delete orignal files than do it.
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    else:
        shutil.rmtree(dst_path)
        os.makedirs(dst_path)
    
    frame_count = 0
    save_count = 0
    save_name = os.path.join(dst_path, (str(save_count) + '.jpg'))
    cv2.imwrite(save_name, frame)
    
    frame_interval = 7    
    
    while success:
        success, frame = videoCapture.read()
        frame_count += 1
        if frame_count % frame_interval == 0:
            save_count += 1
            save_name = os.path.join(dst_path, (str(save_count) + '.jpg'))
            cv2.imwrite(save_name, frame)
        
    print('Process finished')
    print('Total saved frames is: ', save_count + 1)