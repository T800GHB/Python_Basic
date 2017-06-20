#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:25:14 2017

@author: andrew

This model will provide some helpful function or class
"""

import numpy as np
import sys
from collections import namedtuple

rgb_palette = {'background': (0,0,0),
               'road': (0,255,0),
               'car': (255,255,0),
               'person': (255,0,0),                
               'obstacle': (0,0,255),
               'parkinglots': (255,0,255),
               'bump': (0,255,255),
               'ignore': (255,255,255)}                 
gray_palette = {'background': (0,),
                'road': (1,), 
                'car': (2,), 
                'person': (3,),
                'obstacle': (4,),
                'parkinglots': (5,),
                'bump': (6,), 
                'ignore': (255,)}
label_palette = {0: (0,0,0),
                 1: (0,255,0),
                 2: (255,255,0),
                 3: (255,0,0),                
                 4: (0,0,255),                 
                 5: (255,0,255),
                 6: (0,255,255),
                 255: (255,255,255)}

collect_list = ['car','person','obstacle']

bbox = namedtuple('bbox',['name', 'xmin','ymin','xmax','ymax'])

polygon = namedtuple('polygon', ['name', 'pts'])

class process_bar(object):
    def __init__(self, num_items, bar_length = 50, init_count = 0.0):
        self.__process_bar_length = bar_length
        #The factor of percent must be not integer
        self.__num_files = float(num_items)
        self.__file_count = float(init_count)
    def update(self):
        self.__file_count += 1
        percent = self.__file_count / self.__num_files
        has_done = '#' * int(percent * self.__process_bar_length)
        spaces = ' ' * (self.__process_bar_length - len(has_done))
        sys.stdout.write("\rPercent: [%s] %d%%"%(has_done + spaces, percent * 100))
        sys.stdout.flush()
        
def randomPalette(length, min, max):  
    return [ np.random.randint(min, max) for x in range(length)]

def create_png_palette():
    png_palette = np.empty((256,3), dtype = np.uint8)
    png_palette.fill(128)
    for i in label_palette:
        png_palette[i,:] = label_palette[i]

    assign_palette = list(png_palette.flatten())
    
    assert len(assign_palette) == 768

    return assign_palette
