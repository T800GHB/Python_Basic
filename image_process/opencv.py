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