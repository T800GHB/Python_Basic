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
    gray_img.shape = img_size
    """Calculating frequency for every gray level"""
    for i in range(img_size):
        histogram[gray_img[i]] += 1
        
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
    he_img.shape = img_size
    for i in range(img_size):
        he_img[i] = pdf[gray_img[i]] * interval + min_val
    """Generate equalized histogram"""
    he_his = np.zeros((256,))
    for i in range(img_size):
        he_his[he_img[i]] += 1
        
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
    
def mean_filter(filter_w = 5, filter_h  = 5):
    """
    This block code will demostrate how to use integral image to 
    execute mean filter operation
    """
    src_img = np.array(Image.open('./image_process/scenery.jpg').convert('L'))
    height = src_img.shape[0]
    width = src_img.shape[1]
    if ((filter_w < 2) or (filter_h < 2) or
        (height / 2 < filter_h) or (width / 2 < filter_w)):
        print('Filter parameter set failure!' )
        return
    '''Set filter radius for two direction'''
    if filter_w % 2 == 0:
        filter_rw = int(filter_w / 2)
    else:
        filter_rw = int((filter_w - 1) / 2)
    if filter_h % 2 == 0:
        filter_rh = int(filter_h / 2)
    else:
        filter_rh = int((filter_h - 1) / 2)
    '''Calculate filter size as pixel'''
    filter_size = (filter_rw * 2 + 1) * (filter_rh * 2 + 1)
    '''Estabilsh integral image for orignal image'''
    integral = np.empty(src_img.shape)
    integral[0,0] = src_img[0,0]
    '''Initialize first row of integral image'''
    for i in range(1,width):
        integral[0,i] = integral[0, i - 1] + src_img[0,i]
    '''Initialize first col of integral image'''
    for i in range(1,height):
        integral[i,0] = integral[i - 1,0] + src_img[i,0]
    '''Initialize rest part of integral image'''
    for i in range(1,height):
        for j in range(1,width):
            integral[i,j] = (src_img[i,j] + integral[i - 1,j] 
            + integral[i,j - 1] - integral[i - 1, j - 1])
    
    '''Mean filter process for 4 corner'''
    dst_img = np.empty(src_img.shape)
    '''Up left corner'''    
    for i in range(filter_rh + 1):
        for j in range(filter_rw + 1):
            dst_img[i,j] = (integral[i + filter_rh, j + filter_rw] 
            / ((i + filter_rh + 1) * (j + filter_rw + 1)))
    '''Up right corner'''
    for i in range(filter_rh + 1):
        for j in range(width - filter_rw - 1, width):
            dst_img[i,j] = ((integral[i + filter_rh,width - 1]
            - integral[i + filter_rh, j - filter_rw - 1])
             / ((i + filter_rh + 1) * (width - j + filter_rw)))
    '''Down left corner'''
    for i in range(height - filter_rh - 1, height):
        for j in range(filter_rw + 1):
            dst_img[i,j] = ((integral[height - 1, j + filter_rw]
            -integral[i - filter_rh - 1, j + filter_rw])
            /((height - i + filter_rh) * (j + filter_rw + 1)))
    '''Down right corner'''
    for i in range(height - filter_rh - 1, height):
        for j in range(width - filter_rw - 1, width):
            dst_img[i,j] = ((integral[height- 1, width - 1] 
            + integral[i - filter_rh - 1, j - filter_rw -1]
            - integral[height - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, width - 1])
            /((height - i + filter_rh) * (width -j + filter_rw)))
    '''Left edge'''
    for i in range(filter_rh + 1, height - filter_rh - 1):
        for j in range(filter_rw + 1):
            dst_img[i,j] = ((integral[i + filter_rh, j + filter_rw]
            - integral[i - filter_rh - 1, j + filter_rw])
            /((filter_rh * 2 + 1) * (j + filter_rw + 1)))
    '''Right edge'''
    for i in range(filter_rh + 1, height - filter_rh - 1):
        for j in range(width - filter_rw - 1, width):
            dst_img[i,j] = ((integral[i + filter_rh, width -1] 
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, width -1]
            - integral[i + filter_rh, j - filter_rw -1])
            /((filter_rh * 2 + 1) * (width - j + filter_rw)))
    '''Up edge'''
    for i in range(filter_rh + 1):
        for j in range(filter_rw + 1, width - filter_rw -1):
            dst_img[i,j] = ((integral[i + filter_rh, j + filter_rw]
            - integral[i + filter_rh, j - filter_rw - 1])
            /((filter_rw * 2 + 1) * (i + filter_rh + 1)))
    '''Down edge'''
    for i in range(height- filter_rh -1, height):
        for j in range(filter_rw + 1, width - filter_rw -1):
            dst_img[i,j] = ((integral[height -1, j + filter_rw]
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, j + filter_rw]
            - integral[height - 1, j - filter_rw -1])
            /((filter_rw * 2 + 1)*(height - i + filter_rh)))
    '''Centeral part'''
    for i in range(filter_rh + 1, height - filter_rh -1):
        for j in range(filter_rw + 1, width - filter_rw -1):
            dst_img[i,j] = ((integral[i + filter_rh, j + filter_rw]
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, j + filter_rw]
            - integral[i + filter_rh, j - filter_rw -1])
            / filter_size)
    '''Display result'''
    pl.figure('Mean filter process')
    pl.gray()
    pl.subplot(1,2,1)
    pl.title('Orignal image')
    pl.imshow(src_img)
    pl.axis('off')
    pl.subplot(1,2,2)
    pl.title('Processed image')
    pl.imshow(dst_img)
    pl.axis('off')
    pl.show()
        
def filter_process(integral, shape, filter_h = 5, filter_w = 5):
    '''Use integral to execute mean filter'''
    
    height = shape[0]
    width = shape[1]
    
    if ((filter_w < 2) or (filter_h < 2) or
        (height / 2 < filter_h) or (width / 2 < filter_w)):
        print('Filter parameter set failure!' )
    '''Set filter radius for two direction'''
    if filter_w % 2 == 0:
        filter_rw = int(filter_w / 2)
    else:
        filter_rw = int((filter_w - 1) / 2)
    if filter_h % 2 == 0:
        filter_rh = int(filter_h / 2)
    else:
        filter_rh = int((filter_h - 1) / 2)
    '''Calculate filter size as pixel'''
    filter_size = (filter_rw * 2 + 1) * (filter_rh * 2 + 1)
    
   
    '''Mean filter process for 4 corner'''
    dst_img = np.empty(shape, dtype = int)
    '''Up left corner'''    
    for i in range(filter_rh + 1):
        for j in range(filter_rw + 1):
            dst_img[i,j] = (integral[i + filter_rh, j + filter_rw] 
            / ((i + filter_rh + 1) * (j + filter_rw + 1)))
    '''Up right corner'''
    for i in range(filter_rh + 1):
        for j in range(width - filter_rw - 1, width):
            dst_img[i,j] = ((integral[i + filter_rh,width - 1]
            - integral[i + filter_rh, j - filter_rw - 1])
             / ((i + filter_rh + 1) * (width - j + filter_rw)))
    '''Down left corner'''
    for i in range(height - filter_rh - 1, height):
        for j in range(filter_rw + 1):
            dst_img[i,j] = ((integral[height - 1, j + filter_rw]
            -integral[i - filter_rh - 1, j + filter_rw])
            /((height - i + filter_rh) * (j + filter_rw + 1)))
    '''Down right corner'''
    for i in range(height - filter_rh - 1, height):
        for j in range(width - filter_rw - 1, width):
            dst_img[i,j] = ((integral[height- 1, width - 1] 
            + integral[i - filter_rh - 1, j - filter_rw -1]
            - integral[height - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, width - 1])
            /((height - i + filter_rh) * (width -j + filter_rw)))
    '''Left edge'''
    for i in range(filter_rh + 1, height - filter_rh - 1):
        for j in range(filter_rw + 1):
            dst_img[i,j] = ((integral[i + filter_rh, j + filter_rw]
            - integral[i - filter_rh - 1, j + filter_rw])
            /((filter_rh * 2 + 1) * (j + filter_rw + 1)))
    '''Right edge'''
    for i in range(filter_rh + 1, height - filter_rh - 1):
        for j in range(width - filter_rw - 1, width):
            dst_img[i,j] = ((integral[i + filter_rh, width -1] 
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, width -1]
            - integral[i + filter_rh, j - filter_rw -1])
            /((filter_rh * 2 + 1) * (width - j + filter_rw)))
    '''Up edge'''
    for i in range(filter_rh + 1):
        for j in range(filter_rw + 1, width - filter_rw -1):
            dst_img[i,j] = ((integral[i + filter_rh, j + filter_rw]
            - integral[i + filter_rh, j - filter_rw - 1])
            /((filter_rw * 2 + 1) * (i + filter_rh + 1)))
    '''Down edge'''
    for i in range(height- filter_rh -1, height):
        for j in range(filter_rw + 1, width - filter_rw -1):
            dst_img[i,j] = ((integral[height -1, j + filter_rw]
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, j + filter_rw]
            - integral[height - 1, j - filter_rw -1])
            /((filter_rw * 2 + 1)*(height - i + filter_rh)))
    '''Centeral part'''
    for i in range(filter_rh + 1, height - filter_rh -1):
        for j in range(filter_rw + 1, width - filter_rw -1):
            dst_img[i,j] = ((integral[i + filter_rh, j + filter_rw]
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, j + filter_rw]
            - integral[i + filter_rh, j - filter_rw -1])
            / filter_size)
            
    return dst_img
    
def diff_filter():
    '''
    Multiscale filter by mean filter
    Get results of image which processed by two different size mean filter.
    Then, use filtered image of small size minus big one procedure final reslut.
    '''
    src_img = np.array(Image.open('./image_process/tire.bmp').convert('L'))
    height = src_img.shape[0]
    width = src_img.shape[1]
    
    '''Estabilsh integral image for orignal image'''
    integral = np.empty(src_img.shape, dtype = int)
    integral[0,0] = src_img[0,0]
    '''Initialize first row of integral image'''
    for i in range(1,width):
        integral[0,i] = integral[0, i - 1] + src_img[0,i]
    '''Initialize first col of integral image'''
    for i in range(1,height):
        integral[i,0] = integral[i - 1,0] + src_img[i,0]
    '''Initialize rest part of integral image'''
    for i in range(1,height):
        for j in range(1,width):
            integral[i,j] = (src_img[i,j] + integral[i - 1,j] 
            + integral[i,j - 1] - integral[i - 1, j - 1])
    '''Get mean filter result'''
    dst_big = filter_process(integral, src_img.shape, 9,9)
    dst_small = filter_process(integral, src_img.shape,  3,3)
    '''Small minus big could reserve high frequency information'''
    multiscale = dst_small - dst_big
    '''Make all negitive element to be zeros'''
    musk = multiscale < 0
    multiscale[musk] = 0
    '''Display result'''
    pl.figure('Multiscale filter by mean')
    pl.gray()
    pl.subplot(2,2,1)
    pl.title('Orignal image')
    pl.imshow(src_img)
    pl.axis('off')    
    pl.subplot(2,2,2)
    pl.title('Big filter')
    pl.imshow(dst_big)
    pl.axis('off')
    pl.subplot(2,2,3)
    pl.title('Small filter')
    pl.imshow(dst_small)
    pl.axis('off')
    pl.subplot(2,2,4)
    pl.title('Multiscale Reslult')
    pl.imshow(multiscale)
    pl.axis('off')
    pl.show()