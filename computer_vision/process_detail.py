# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 22:51:19 2016

@author: andrew

This file will implement a part of basic image processing by operating pixel.
Detail about process will demostrate, through those implementation.
"""

from PIL import Image
import numpy as np
import pylab as pl
import matplotlib.cm as cm

def image_histo():
    """
    This block code will describe how to calculate histogram for gray image,
    and use histogram to do histogram equalization.
    """
    src_img = np.array(Image.open('./computer_vision/scenery.jpg'))
    """Make image gray"""
    if np.size(src_img.shape) == 3:
        gray_img = src_img[...,0]* 0.3 + src_img[...,1]* 0.59 + src_img[...,2]* 0.11
    else:
        gray_img = src_img
    
    """Achive height and width"""
    height = gray_img.shape[0]
    width = gray_img.shape[1]
    print('Image height : %d, width : %d.\n' %(height, width))
    """Establish a bins for histogram"""
    histogram = np.zeros((256,))
    img_size = gray_img.size
    gray_img.shape = (1,img_size)
    """Calculating frequency for every gray level"""
    for i in range(img_size):
        histogram[gray_img[0,i]] += 1
        
    """Establish a bins for probability density function"""
    pdf = np.zeros((256,))
    """Add up all the frequency smaller than current gray level"""
    pdf[0] = histogram[0]
    for i in range(255):
        pdf[i + 1] = pdf[i] + histogram[i + 1]
    """Divide total number of pixels to generate probability"""
    pdf = pdf / img_size
    
    """Histogram equalized image"""
    he_img = np.zeros((img_size))
    """Achive max and min gray value in orignal image"""
    max_val = np.max(gray_img)
    min_val = np.min(gray_img)
    interval = max_val - min_val
    
    """Map gray level in orignal image to equalized histogram"""
    he_img.shape = (1,img_size)
    for i in range(img_size):
        he_img[0,i] = pdf[gray_img[0,i]] * interval + min_val
    """Generate equalized histogram"""
    he_his = np.zeros((256,))
    for i in range(img_size):
        he_his[he_img[0,i]] += 1
        
    """Display result"""
    pl.figure('Histogram process')
    gray_img.shape = (height, width)
    he_img.shape = (height, width)
    pl.subplot(2,2,1)
    pl.gray()
    pl.title('Orignal image')
    pl.axis('off')
    pl.imshow(gray_img)
    pl.subplot(2,2,2)
    pl.title('Orignal histogram')
    pl.xlim(0, 256)
    pl.xticks([])
    pl.bar(range(256), histogram, color = 'green')
    pl.subplot(2,2,3)    
    pl.title('Equalized image')
    pl.axis('off')
    pl.imshow(he_img, cmap = cm.gray)
    pl.subplot(2,2,4)
    pl.title('Equalized histogram')
    pl.xlim(0, 256)
    pl.xticks([])
    pl.bar(range(256), he_his, color = (1,0,0))
    pl.show()
    