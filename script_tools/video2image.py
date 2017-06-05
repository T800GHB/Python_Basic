#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:25:14 2017

@author: andrew

Install opencv by this mean
$conda install opencv
version 3.1.0
"""

import cv2
import os
import shutil
import assist_util
import argparse

#Crop region: left, up, right, down
bbox = (0,168, 1280, 520)

def initialization(args):
    '''
    Initialization for video process
    '''
    video_path = args.src
    dst_prefix = args.dst    
    
    if not os.path.isfile(video_path) :
        raise IOError('This is not a video file: ', video_path)    
    
    videoCapture = cv2.VideoCapture(video_path)
    
    height = int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH))    
    total_frame_count = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    
    print('video file: ', video_path,
          '\nframe height: ', height,
          '\nframe width: ', width,
          '\ntotal count of frame: ', total_frame_count,
          '\nframe per second: ', fps)
    
    #Seperate video name from path and postfix
    file_name = video_path.split('/')[-1]
    base_name = file_name.split('.')[0]
    #Create or clean destination
    dst_path = os.path.join(dst_prefix, base_name)
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    else:
        shutil.rmtree(dst_path)
        os.makedirs(dst_path)
    
    return videoCapture, dst_path, total_frame_count, height, width

def video_process(args): 
    '''
    Read video frame and do some image process
    '''
    videoCapture, dst_path, total_frame_count,  height, width = initialization(args)
    frame_interval = args.interval
    ratio = args.ratio
    
    name_length = len(str(total_frame_count))
    pad_char = '0'

    success, frame = videoCapture.read()
    #Sometimes, width and height of frame could not be achived correctly
    if height == 0 and width == 0:
        #height, width, channels
        height = frame.shape[0]
        width = frame.shape[1]
    
    frame_count = 0
    save_count = 0    
    
    bar_worker = assist_util.process_bar(num_items= total_frame_count)
    
    while success:       
        
        bar_worker.update()
        if frame_count % frame_interval == 0:         
            num_str = str(save_count)        
            save_name = os.path.join(dst_path, (pad_char * (name_length - len(num_str)) + num_str + '.jpg'))
            if ratio != 1.0:
                frame = cv2.resize(frame, (int(width * ratio), int(height * ratio)), cv2.INTER_CUBIC)
            if args.crop:
                frame = frame[bbox[1]: bbox[3], bbox[0]: bbox[2]]
            save_count += 1            
            cv2.imwrite(save_name, frame)
            
        frame_count += 1
        success, frame = videoCapture.read()
        
    print('\nProcess finished')
    print('Total saved frames is: ', save_count + 1)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(                                     
    description= '''
                Extract frame from video and do some image process
                 ''',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s','--src', type = str, default = None,
                        help = 'The directory that contain video')
    parser.add_argument('-d','--dst', type = str, default = './frame/',
                        help = 'The directory that store frames')
    parser.add_argument('-r','--ratio', type = float, default = 1.0,
                        help = 'Resize ratio of frame boundary length')
    parser.add_argument('-c','--crop', type = int, default = 0,
                        help = 'Wether crop a region from orginal image')
    parser.add_argument('-i','--interval', type = int, default = 1,
                        help = 'Skip interval for extracting frames')
    args = parser.parse_args()
    video_process(args)


    
