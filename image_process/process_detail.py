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
from skimage import io
from skimage import color
from skimage import img_as_ubyte

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
    
def mean_filter(filter_h = 5, filter_w  = 5):
    """
    This block code will demostrate how to use integral image to 
    execute mean filter operation
    """
    src_img = np.array(Image.open('./image_process/scenery.jpg').convert('L'))
    
    '''Calculate integral image'''
    integral = integral_image(src_img)
    '''Mean filter process'''
    dst_img = filter_process(integral, filter_h, filter_w)
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
    
def filter_centerout(filter_bh = 9, filter_bw = 9, filter_sh = 3, filter_sw = 3):
    """
    This block code will demostrate how to process a  image by mean filter
    and multiscale filter without centeral part.
    """
    src_img = np.array(Image.open('./image_process/scenery.jpg').convert('L'))
    
    '''Calculate integral image'''
    integral = integral_image(src_img)
    
    img_data_diff = src_img.copy()
    '''Mean filter process'''
    filter_result = filter_process_centerout(img_data_diff, integral, filter_sh, filter_sw,
                        up = 250, down = 500, left = 250, right = 600)
    
    filter_result_small = filter_result.copy()
    diff_result = diff_process_centerout(filter_result, integral, filter_bh,filter_bw,
                        up = 250, down = 500, left = 250, right = 600)
    
    img_data_alone = src_img.copy()
    filter_result_big = filter_process_centerout(img_data_alone, integral, filter_bh, filter_bw,
                        up = 250, down = 500, left = 250, right = 600)
    '''Display result'''
    pl.figure('Center out filter process')
    pl.gray()
    pl.subplot(2,2,1)
    pl.title('Orignal image')
    pl.imshow(src_img)  
    pl.axis('off')
    pl.subplot(2,2,2)
    pl.title('Multiscale filter process')
    pl.imshow(diff_result)
    pl.axis('off')
    pl.subplot(2,2,3)
    pl.title('Small mean filter result')
    pl.imshow(filter_result_small)
    pl.axis('off')
    pl.subplot(2,2,4)
    pl.title('Big mean filter result')
    pl.imshow(filter_result_big)
    pl.axis('off')
    pl.show()
    
def integral_image(src_img):    
    '''Estabilsh integral image for orignal image'''
    height = src_img.shape[0]
    width = src_img.shape[1]
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
    
    return integral
        
def filter_process(integral, filter_h = 5, filter_w = 5):
    '''Use integral to execute mean filter'''
    
    height = integral.shape[0]
    width = integral.shape[1]
    
    if ((filter_w < 2) or (filter_h < 2) or
        (height / 2 < filter_h) or (width / 2 < filter_w)):
        raise ValueError('Filter parameter set failure!' )
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
    dst_img = np.empty(integral.shape, dtype = np.int)
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
    
def filter_process_centerout(dst_img, integral, filter_h = 5, filter_w = 5,
                             up = 250, down = 500, left = 250, right = 600):
    '''Use integral to execute mean filter without center part'''
    height = integral.shape[0]
    width = integral.shape[1]
    
    if ((filter_w < 2) or (filter_h < 2) or
        (height / 2 < filter_h) or (width / 2 < filter_w) or
        (up < filter_h) or (left < filter_w) or
        (height - down < filter_h) or (width - right < filter_w)):
        raise ValueError('Filter parameter set failure!' )
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
    '''Process big block use full filter'''
    '''Up block'''
    for i in range(filter_rh + 1, up - filter_rh + 1):
        for j in range(filter_rw + 1, width - filter_rw - 1):
            dst_img[i,j] = ((integral[i + filter_rh, j + filter_rw]
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, j + filter_rw]
            - integral[i + filter_rh, j - filter_rw -1])
            / filter_size)
    '''Left an right block'''
    for i in range(up - filter_rh + 1, down + filter_rh):
        for j in range(filter_rw + 1, left - filter_rw + 1):
            dst_img[i,j] = ((integral[i + filter_rh, j + filter_rw]
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, j + filter_rw]
            - integral[i + filter_rh, j - filter_rw -1])
            / filter_size)
        for j in range(right + filter_rw, width - filter_rw - 1):
            dst_img[i,j] = ((integral[i + filter_rh, j + filter_rw]
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, j + filter_rw]
            - integral[i + filter_rh, j - filter_rw -1])
            / filter_size)
    '''Down block'''
    for i in range(down + filter_rh, height - filter_rh - 1):
        for j in range(filter_rw + 1, width - filter_rw - 1):
            dst_img[i,j] = ((integral[i + filter_rh, j + filter_rw]
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, j + filter_rw]
            - integral[i + filter_rh, j - filter_rw -1])
            / filter_size)
    '''Process cross boundary with invalid region'''
    '''Up left corner'''
    for i in range(up - filter_rh + 1, up + 1):
        for j in range(left - filter_rw + 1, left + filter_rw + 1):
            diff_val = (integral[i - filter_rh - 1, j - filter_rw - 1]
                         - integral[i - filter_rh - 1, j + filter_rw]
                         - integral[i + filter_rh, j - filter_rw - 1]
                         - integral[up, left]
                         + integral[i + filter_rh, left]
                         + integral[up, j + filter_rw])
               
            area = filter_size - (i + filter_rh - up) * (j + filter_rw - left)
            dst_img[i,j] = diff_val / area
    for i in range(up + 1, up + filter_rh + 1):
        for j in range(left - filter_rw + 1, left + 1):
            diff_val = (integral[i - filter_rh - 1, j - filter_rw - 1]
                         - integral[i - filter_rh - 1, j + filter_rw]
                         - integral[i + filter_rh, j - filter_rw - 1]
                         - integral[up, left]
                         + integral[i + filter_rh, left]
                         + integral[up, j + filter_rw])
            
            area = filter_size - (i + filter_rh - up) * (j + filter_rw - left)
            dst_img[i,j] = diff_val / area
    '''Up edge'''
    for i in range(up - filter_rh + 1, up + 1):
        for j in range(left + filter_rw + 1, right - filter_rw):
            sum_big = (integral[up, j + filter_rw]
                       + integral[i - filter_rh - 1, j - filter_rw - 1]
                       - integral[i - filter_rh - 1, j + filter_rw]
                       - integral[up , j - filter_rw - 1])
            
            area = (up - i + filter_rh + 1) * filter_w
            dst_img[i,j] = sum_big / area
    '''Up right corner'''
    for i in range(up - filter_rh + 1, up + 1):
        for j in range(right - filter_rw, right + filter_rw):
            diff_val = (integral[i + filter_rh, j + filter_rw]
                        + integral[i - filter_rh - 1, j - filter_rw - 1]
                        - integral[i - filter_rh - 1, j + filter_rw]
                        - integral[i + filter_rh, right - 1]
                        - integral[up, j - filter_rw - 1]
                        + integral[up, right - 1])
            area = filter_size - (i + filter_rh - up) * (right - j + filter_rw)
            dst_img[i,j] = diff_val / area
    for i in range(up, up + filter_rh + 1):
        for j in range(right, right + filter_rw):
            diff_val = (integral[i + filter_rh, j + filter_rw]
                        + integral[i - filter_rh - 1, j - filter_rw - 1]
                        - integral[i - filter_rh - 1, j + filter_rw]
                        - integral[i + filter_rh, right - 1]
                        - integral[up, j - filter_rw - 1]
                        + integral[up, right - 1])
            
            area = filter_size - (i + filter_rh - up) * (right - j + filter_rw)
            dst_img[i,j] = diff_val / area
    '''Right edge'''
    for i in range(up + filter_rh + 1, down - filter_rh):
        for j in range(right, right + filter_rw):
            sum_big = (integral[i + filter_rh, j + filter_rw]
                       + integral[i - filter_rh - 1, right - 1]
                       - integral[i - filter_rh - 1, j + filter_rw]
                       - integral[i + filter_rh, right - 1])
            
            area = filter_h * (j + filter_rw - right + 1)
            dst_img[i,j] = sum_big / area
    '''Down right corner'''
    for i in range(down - filter_rh, down + filter_rh):
        for j in range(right, right + filter_rw):
            diff_val = (integral[i + filter_rh, j + filter_rw]
                        - integral[i - filter_rh - 1, j + filter_rw]
                        - integral[i + filter_rh, j - filter_rw - 1]
                        - integral[down - 1, right - 1]
                        + integral[down - 1, j - filter_rw - 1]
                        + integral[i - filter_rh - 1, right -1])
            
            area = filter_size - (down - i + filter_rh) * (right - j + filter_rw)
            dst_img[i,j] = diff_val / area
    for i in range(down, down + filter_rh):
        for j in range(right - filter_rw, right):
            diff_val = (integral[i + filter_rh, j + filter_rw]
                        - integral[i - filter_rh - 1, j + filter_rw]
                        - integral[i + filter_rh, j - filter_rw - 1]
                        - integral[down - 1, right - 1]
                        + integral[down - 1, j - filter_rw - 1]
                        + integral[i - filter_rh - 1, right -1])
            
            area = filter_size - (down - i + filter_rh) * (right - j + filter_rw)
            dst_img[i,j] = diff_val / area
    '''Down edge'''
    for i in range(down, down + filter_rh):
        for j in range(left + filter_rw + 1, right - filter_rw):
            sum_big = (integral[i + filter_rh, j + filter_rw]
                       + integral[down - 1, j - filter_rw -1]
                       - integral[down - 1, j + filter_rw]
                       - integral[i + filter_rh, j - filter_rw - 1])
            
            area = (i + filter_rh - down + 1) * filter_w
            dst_img[i,j] = sum_big / area
    '''Down left corner'''
    for i in range(down, down + filter_rh):
        for j in range(left - filter_rw + 1, left + filter_rw + 1):
            diff_val = (integral[i + filter_rh, j + filter_rw]
                        + integral[i - filter_rh - 1, j - filter_rw - 1]
                        - integral[i + filter_rh, j - filter_rw - 1]
                        - integral[down - 1, j + filter_rw]
                        - integral[i - filter_rh - 1, left]
                        + integral[down - 1, left])
            
            area = filter_size - (down - i + filter_rh) * (j + filter_rw - left)
            dst_img[i,j] = diff_val / area
    for i in range(down - filter_rh, down):
        for j in range(left - filter_rw + 1, left + 1):
            diff_val = (integral[i + filter_rh, j + filter_rw]
                        + integral[i - filter_rh - 1, j - filter_rw - 1]
                        - integral[i + filter_rh, j - filter_rw - 1]
                        - integral[down - 1, j + filter_rw]
                        - integral[i - filter_rh - 1, left]
                        + integral[down - 1, left])
            
            area = filter_size - (down - i + filter_rh) *(j + filter_rw - left)
            dst_img[i,j] = diff_val / area
    '''Left edge'''
    for i in range(up + filter_rh + 1, down - filter_rh):
        for j in range(left - filter_rw + 1, left + 1):
            sum_big = (integral[i + filter_rh, left]
                       + integral[i - filter_rh - 1, j - filter_rw - 1]
                       - integral[i - filter_rh - 1, left]
                       - integral[i + filter_rh, j - filter_rw - 1])
            
            area = filter_h * (left - j + filter_rw + 1)
            dst_img[i,j] = sum_big / area
    
    return dst_img

def diff_process_centerout(dst_img, integral, filter_h = 5, filter_w = 5,
                             up = 250, down = 500, left = 250, right = 600):
    '''Use integral to execute mean filter without center part'''
    height = integral.shape[0]
    width = integral.shape[1]
    
    if ((filter_w < 2) or (filter_h < 2) or
        (height / 2 < filter_h) or (width / 2 < filter_w) or
        (up < filter_h) or (left < filter_w) or
        (height - down < filter_h) or (width - right < filter_w)):
        raise ValueError('Filter parameter set failure!' )
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
    dst_img = np.array(dst_img, dtype = np.int)
    '''Up left corner'''    
    for i in range(filter_rh + 1):
        for j in range(filter_rw + 1):
            dst_img[i,j] -= (integral[i + filter_rh, j + filter_rw] 
            / ((i + filter_rh + 1) * (j + filter_rw + 1)))
            
            if dst_img[i,j] < 0 : dst_img[i,j] = 0
    '''Up right corner'''
    for i in range(filter_rh + 1):
        for j in range(width - filter_rw - 1, width):
            dst_img[i,j] -= ((integral[i + filter_rh,width - 1]
            - integral[i + filter_rh, j - filter_rw - 1])
             / ((i + filter_rh + 1) * (width - j + filter_rw)))
                
            if dst_img[i,j] < 0 : dst_img[i,j] = 0
    '''Down left corner'''
    for i in range(height - filter_rh - 1, height):
        for j in range(filter_rw + 1):
            dst_img[i,j] -= ((integral[height - 1, j + filter_rw]
            -integral[i - filter_rh - 1, j + filter_rw])
            /((height - i + filter_rh) * (j + filter_rw + 1)))
            
            if dst_img[i,j] < 0 : dst_img[i,j] = 0
    '''Down right corner'''
    for i in range(height - filter_rh - 1, height):
        for j in range(width - filter_rw - 1, width):
            dst_img[i,j] -= ((integral[height- 1, width - 1] 
            + integral[i - filter_rh - 1, j - filter_rw -1]
            - integral[height - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, width - 1])
            /((height - i + filter_rh) * (width -j + filter_rw)))
                
            if dst_img[i,j] < 0 : dst_img[i,j] = 0
    '''Left edge'''
    for i in range(filter_rh + 1, height - filter_rh - 1):
        for j in range(filter_rw + 1):
            dst_img[i,j] -= ((integral[i + filter_rh, j + filter_rw]
            - integral[i - filter_rh - 1, j + filter_rw])
            /((filter_rh * 2 + 1) * (j + filter_rw + 1)))
            
            if dst_img[i,j] < 0 : dst_img[i,j] = 0
    '''Right edge'''
    for i in range(filter_rh + 1, height - filter_rh - 1):
        for j in range(width - filter_rw - 1, width):
            dst_img[i,j] -= ((integral[i + filter_rh, width -1] 
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, width -1]
            - integral[i + filter_rh, j - filter_rw -1])
            /((filter_rh * 2 + 1) * (width - j + filter_rw)))
                
            if dst_img[i,j] < 0 : dst_img[i,j] = 0
    '''Up edge'''
    for i in range(filter_rh + 1):
        for j in range(filter_rw + 1, width - filter_rw -1):
            dst_img[i,j] -= ((integral[i + filter_rh, j + filter_rw]
            - integral[i + filter_rh, j - filter_rw - 1])
            /((filter_rw * 2 + 1) * (i + filter_rh + 1)))
            
            if dst_img[i,j] < 0 : dst_img[i,j] = 0
    '''Down edge'''
    for i in range(height- filter_rh -1, height):
        for j in range(filter_rw + 1, width - filter_rw -1):
            dst_img[i,j] -= ((integral[height -1, j + filter_rw]
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, j + filter_rw]
            - integral[height - 1, j - filter_rw -1])
            /((filter_rw * 2 + 1)*(height - i + filter_rh)))
                
            if dst_img[i,j] < 0 : dst_img[i,j] = 0
    '''Process big block use full filter'''
    '''Up block'''
    for i in range(filter_rh + 1, up - filter_rh + 1):
        for j in range(filter_rw + 1, width - filter_rw - 1):
            dst_img[i,j] -= ((integral[i + filter_rh, j + filter_rw]
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, j + filter_rw]
            - integral[i + filter_rh, j - filter_rw -1])
            / filter_size)
                
            if dst_img[i,j] < 0 : dst_img[i,j] = 0
    '''Left an right block'''
    for i in range(up - filter_rh + 1, down + filter_rh):
        for j in range(filter_rw + 1, left - filter_rw + 1):
            dst_img[i,j] -= ((integral[i + filter_rh, j + filter_rw]
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, j + filter_rw]
            - integral[i + filter_rh, j - filter_rw -1])
            / filter_size)
                
            if dst_img[i,j] < 0 : dst_img[i,j] = 0

        for j in range(right + filter_rw, width - filter_rw - 1):
            dst_img[i,j] -= ((integral[i + filter_rh, j + filter_rw]
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, j + filter_rw]
            - integral[i + filter_rh, j - filter_rw -1])
            / filter_size)
                
            if dst_img[i,j] < 0 : dst_img[i,j] = 0
    '''Down block'''
    for i in range(down + filter_rh, height - filter_rh - 1):
        for j in range(filter_rw + 1, width - filter_rw - 1):
            dst_img[i,j] -= ((integral[i + filter_rh, j + filter_rw]
            + integral[i - filter_rh - 1, j - filter_rw - 1]
            - integral[i - filter_rh - 1, j + filter_rw]
            - integral[i + filter_rh, j - filter_rw -1])
            / filter_size)
                
            if dst_img[i,j] < 0 : dst_img[i,j] = 0
    '''Process cross boundary with invalid region'''
    '''Up left corner'''
    for i in range(up - filter_rh + 1, up + 1):
        for j in range(left - filter_rw + 1, left + filter_rw + 1):
            diff_val = (integral[i - filter_rh - 1, j - filter_rw - 1]
                         - integral[i - filter_rh - 1, j + filter_rw]
                         - integral[i + filter_rh, j - filter_rw - 1]
                         - integral[up, left]
                         + integral[i + filter_rh, left]
                         + integral[up, j + filter_rw])
               
            area = filter_size - (i + filter_rh - up) * (j + filter_rw - left)
            dst_img[i,j] -= diff_val / area
            if dst_img[i,j] < 0 : dst_img[i,j] = 0

    for i in range(up + 1, up + filter_rh + 1):
        for j in range(left - filter_rw + 1, left + 1):
            diff_val = (integral[i - filter_rh - 1, j - filter_rw - 1]
                         - integral[i - filter_rh - 1, j + filter_rw]
                         - integral[i + filter_rh, j - filter_rw - 1]
                         - integral[up, left]
                         + integral[i + filter_rh, left]
                         + integral[up, j + filter_rw])
            
            area = filter_size - (i + filter_rh - up) * (j + filter_rw - left)
            dst_img[i,j] -= diff_val / area
            if dst_img[i,j] < 0 : dst_img[i,j] = 0

    '''Up edge'''
    for i in range(up - filter_rh + 1, up + 1):
        for j in range(left + filter_rw + 1, right - filter_rw):
            sum_big = (integral[up, j + filter_rw]
                       + integral[i - filter_rh - 1, j - filter_rw - 1]
                       - integral[i - filter_rh - 1, j + filter_rw]
                       - integral[up , j - filter_rw - 1])
            
            area = (up - i + filter_rh + 1) * filter_w
            dst_img[i,j] -= sum_big / area
            if dst_img[i,j] < 0 : dst_img[i,j] = 0

    '''Up right corner'''
    for i in range(up - filter_rh + 1, up + 1):
        for j in range(right - filter_rw, right + filter_rw):
            diff_val = (integral[i + filter_rh, j + filter_rw]
                        + integral[i - filter_rh - 1, j - filter_rw - 1]
                        - integral[i - filter_rh - 1, j + filter_rw]
                        - integral[i + filter_rh, right - 1]
                        - integral[up, j - filter_rw - 1]
                        + integral[up, right - 1])
            area = filter_size - (i + filter_rh - up) * (right - j + filter_rw)
            dst_img[i,j] -= diff_val / area
            if dst_img[i,j] < 0 : dst_img[i,j] = 0

    for i in range(up, up + filter_rh + 1):
        for j in range(right, right + filter_rw):
            diff_val = (integral[i + filter_rh, j + filter_rw]
                        + integral[i - filter_rh - 1, j - filter_rw - 1]
                        - integral[i - filter_rh - 1, j + filter_rw]
                        - integral[i + filter_rh, right - 1]
                        - integral[up, j - filter_rw - 1]
                        + integral[up, right - 1])
            
            area = filter_size - (i + filter_rh - up) * (right - j + filter_rw)
            dst_img[i,j] -= diff_val / area
            if dst_img[i,j] < 0 : dst_img[i,j] = 0
    '''Right edge'''
    for i in range(up + filter_rh + 1, down - filter_rh):
        for j in range(right, right + filter_rw):
            sum_big = (integral[i + filter_rh, j + filter_rw]
                       + integral[i - filter_rh - 1, right - 1]
                       - integral[i - filter_rh - 1, j + filter_rw]
                       - integral[i + filter_rh, right - 1])
            
            area = filter_h * (j + filter_rw - right + 1)
            dst_img[i,j] -= sum_big / area
            if dst_img[i,j] < 0 : dst_img[i,j] = 0

    '''Down right corner'''
    for i in range(down - filter_rh, down + filter_rh):
        for j in range(right, right + filter_rw):
            diff_val = (integral[i + filter_rh, j + filter_rw]
                        - integral[i - filter_rh - 1, j + filter_rw]
                        - integral[i + filter_rh, j - filter_rw - 1]
                        - integral[down - 1, right - 1]
                        + integral[down - 1, j - filter_rw - 1]
                        + integral[i - filter_rh - 1, right -1])
            
            area = filter_size - (down - i + filter_rh) * (right - j + filter_rw)
            dst_img[i,j] -= diff_val / area
            if dst_img[i,j] < 0 : dst_img[i,j] = 0

    for i in range(down, down + filter_rh):
        for j in range(right - filter_rw, right):
            diff_val = (integral[i + filter_rh, j + filter_rw]
                        - integral[i - filter_rh - 1, j + filter_rw]
                        - integral[i + filter_rh, j - filter_rw - 1]
                        - integral[down - 1, right - 1]
                        + integral[down - 1, j - filter_rw - 1]
                        + integral[i - filter_rh - 1, right -1])
            
            area = filter_size - (down - i + filter_rh) * (right - j + filter_rw)
            dst_img[i,j] -= diff_val / area
            if dst_img[i,j] < 0 : dst_img[i,j] = 0

    '''Down edge'''
    for i in range(down, down + filter_rh):
        for j in range(left + filter_rw + 1, right - filter_rw):
            sum_big = (integral[i + filter_rh, j + filter_rw]
                       + integral[down - 1, j - filter_rw -1]
                       - integral[down - 1, j + filter_rw]
                       - integral[i + filter_rh, j - filter_rw - 1])
            
            area = (i + filter_rh - down + 1) * filter_w
            dst_img[i,j] -= sum_big / area
            if dst_img[i,j] < 0 : dst_img[i,j] = 0

    '''Down left corner'''
    for i in range(down, down + filter_rh):
        for j in range(left - filter_rw + 1, left + filter_rw + 1):
            diff_val = (integral[i + filter_rh, j + filter_rw]
                        + integral[i - filter_rh - 1, j - filter_rw - 1]
                        - integral[i + filter_rh, j - filter_rw - 1]
                        - integral[down - 1, j + filter_rw]
                        - integral[i - filter_rh - 1, left]
                        + integral[down - 1, left])
            
            area = filter_size - (down - i + filter_rh) * (j + filter_rw - left)
            dst_img[i,j] -= diff_val / area
            if dst_img[i,j] < 0 : dst_img[i,j] = 0

    for i in range(down - filter_rh, down):
        for j in range(left - filter_rw + 1, left + 1):
            diff_val = (integral[i + filter_rh, j + filter_rw]
                        + integral[i - filter_rh - 1, j - filter_rw - 1]
                        - integral[i + filter_rh, j - filter_rw - 1]
                        - integral[down - 1, j + filter_rw]
                        - integral[i - filter_rh - 1, left]
                        + integral[down - 1, left])
            
            area = filter_size - (down - i + filter_rh) *(j + filter_rw - left)
            dst_img[i,j] -= diff_val / area
            if dst_img[i,j] < 0 : dst_img[i,j] = 0

    '''Left edge'''
    for i in range(up + filter_rh + 1, down - filter_rh):
        for j in range(left - filter_rw + 1, left + 1):
            sum_big = (integral[i + filter_rh, left]
                       + integral[i - filter_rh - 1, j - filter_rw - 1]
                       - integral[i - filter_rh - 1, left]
                       - integral[i + filter_rh, j - filter_rw - 1])
            
            area = filter_h * (left - j + filter_rw + 1)
            dst_img[i,j] -= sum_big / area
            if dst_img[i,j] < 0 : dst_img[i,j] = 0
    
    return np.array(dst_img, dtype = np.uint8)
    

    
def diff_filter(filter_bh = 9, filter_bw = 9, filter_sh = 3, filter_sw = 3):
    '''
    Multiscale filter by mean filter
    Get results of image which processed by two different size mean filter.
    Then, use filtered image of small size minus big one procedure final reslut.
    '''
    src_img = np.array(Image.open('./image_process/tire.bmp').convert('L'))         
    
    '''Calculate integral image'''
    integral = integral_image(src_img)
    '''Get mean filter result'''
    dst_big = filter_process(integral, filter_bh,filter_bw)
    dst_small = filter_process(integral, filter_sh,filter_sw)
    '''Small minus big could reserve high frequency information'''
    multiscale = dst_small - dst_big
    '''Make all negitive element to be zeros'''
    musk = multiscale < 0
    multiscale[musk] = 0
    multiscale = np.array(multiscale, dtype = np.uint8)
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
    
class object_info(object):
    def __init__(self, up = 10000, left = 10000, down = 0, right = 0, area = 0):
        '''constructer'''
        self.__up = up
        self.__left = left
        self.__down = down
        self.__right = right
        self.__area = area
    
    @property
    def up(self):
        return self.__up
    @up.setter
    def up(self, up):
        if up < 0:
            raise ValueError('Location in image should not less than 0')
        self.__up = up
    @property
    def left(self):
        return self.__left
    @left.setter
    def left(self, left):
        if left < 0:
            raise ValueError('Location in image should not less than 0')
        self.__left = left
    @property
    def down(self):
        return self.__down
    @down.setter
    def down(self, down):
        if down < 0:
            raise ValueError('Location in image should not less than 0')
        self.__down = down
    @property
    def right(self):
        return self.__right
    @right.setter
    def right(self, right):
        if right < 0:
            raise ValueError('Location in iamge should not less than 0')
        self.__right = right
    @property
    def area(self):
        return self.__area
    @area.setter
    def area(self, area):
        if area < 0:
            raise ValueError('Area calculation failure')
        elif area == 0:
            self.__area = 1
        else:
            self.__area = area
    @property
    def width(self):
        if self.__right < self.__left:
            return 0
        else:
            return self.__right - self.__left + 1
    @property
    def height(self):
        if self.__down < self.__up:
            return 0
        else:
            return self.__down - self.__up + 1
    
    
    
def connection_label(thre = 128, direction = 8):
    '''
    This function will find a set of connection regions.
    Parameter of input is: threshold used for getting binary image, 
    number of connection adjacent pixel(4 or 8)
    run block means a independent foreground piexls set in a row.
    '''
    src_img = np.array(Image.open('./image_process/tire.bmp').convert('L'))
    height = src_img.shape[0]
    width = src_img.shape[1]
    '''Achive binary image'''
    bindata = src_img >= thre
    '''
    Establish a container to store a set of indices that indicate start and end
    foreground pixel in its row.
    Because of unknow quantity should be recoreded, so list will be more convenient.
    '''
    run_start = []
    run_end = []
    '''Record the rows that run block belonging'''
    run_row = []
    '''Last index in a row'''
    border = width - 1
    '''Scan the full image to record run block'''
    for i in range(height): 
        '''First element in this row is foreground pixel'''
        if bindata[i,0] == True:
            run_row.append(i)
            run_start.append(0)
        for j in range(1, width):
            '''Find b-f switch location that will be treated as start index'''
            if bindata[i,j - 1] == False and bindata[i, j]== True:
                run_row.append(i)
                run_start.append(j)
            '''Record run block end index'''
            if bindata[i,j - 1] == True and bindata[i, j] == False:
                run_end.append(j - 1)
            '''Maybe the end index is the last one in this row'''
            if bindata[i,j] == True and j == border:
                run_end.append(border)
    assert(len(run_row) == len(run_start) == len(run_end)),\
    'Recoud unequal %d, %d, %d' %(len(run_row), len(run_start), len(run_end))
    run_count = len((run_start))
    '''
    Establish container to record run block label.
    This array will be used as indices, so int data type needed.
    '''
    run_label = np.zeros(run_count, dtype = int)
    '''Record pairs of equal label, unknow quantity, use list'''
    label_pair = []
    '''Assistant index to help scan run block record'''    
    per_start = 0       #Indicate the start index in perious row
    per_end = 0         #Indicate the end index in preious row
    cur_index = 0       #Record the row that is scanning
    label_value = 1     #Label generator
    '''Set the number of adjcent pixel that belong to same connection region'''
    if direction == 8:
        offset = 1
    elif direction == 4:
        offset = 0
    else:
        raise ValueError('Connection parameter setting limited only 4 or 8')
    '''
    Scanning run block record and assign labels to the unlabel ones.
    If run block in adjacent two rows overlaped with columns, use same label.
    If the overlaped ones already have different labels, record as equal pair
    '''
    for i in range(run_count):
        '''Update index information, when the current row has scanned.'''
        if cur_index != run_row[i]:
            cur_index = run_row[i]
            per_start = per_end
            per_end = i            
        '''Search overlap'''
        for j in range(per_start, per_end):
            if ((run_start[i] <= run_end[j] + offset) 
            and (run_start[j] <= run_end[i] + offset) 
            and (run_row[j] + 1 == run_row[i])):
                if run_label[i] == 0:
                    run_label[i] = run_label[j]
                elif (run_label[i] != 0 and run_label[i] != run_label[j]):
                    label_pair.append([run_label[i], run_label[j]])                    
        '''If this run block does not overlap with other, assign a new label'''
        if run_label[i] == 0:            
            run_label[i] = label_value
            label_value += 1
    pair_count = len(label_pair)            #Total number of equal pair
    '''Delete repeat element in equal pair record'''
    for i in range(1,pair_count):
        for j in range(i):
            if label_pair[j][0] != 0:
                if ((label_pair[j][0] == label_pair[i][0]
                    and label_pair[j][1] == label_pair[i][1])
                    or
                    (label_pair[j][0] == label_pair[i][1]
                    and label_pair[j][1] == label_pair[i][0])):
                        label_pair[i][0] = 0 #Set to zeros as one wait for deleting
    '''Unique operation, delete all repeat elements and move unique ones to head.'''
    head = 0            #receive pointer
    search = 0          #Send pointer
    while search < pair_count:
        if label_pair[search][0] != 0:
            if head == search:
                head += 1
                search += 1
            else:
                label_pair[head][0] = label_pair[search][0]
                label_pair[head][1] = label_pair[search][1]
                head += 1
                search += 1
        else:
            search += 1
            
    '''Reset total number of equal pair'''
    pair_count = head
    
    '''
    Merge equal pair.
    Equal pair record just like a graph that stored as sparse matrix.
    So we need to search all the connection relationship from one node ,
    and  assign them a same label.
    '''
    label_flag = np.zeros(label_value, dtype = int) #Table of label mapping to new one
    new_label = 0                           #New label
    
    for i in range(1, label_value):
        if label_flag[i] != 0:
            continue
        '''New relationship created'''
        new_label += 1
        label_flag[i] = new_label
        '''Establish temporary list to store connection relationship'''
        temp_list = []
        temp_list.append(i)
        index = 0
        while index < len(temp_list):
            for pair in label_pair:
                if pair[0] == temp_list[index]:
                    equal_com = pair[1]    #Equal pair another component
                    if label_flag[equal_com] == 0:
                        temp_list.append(equal_com) #Add new connection
                        label_flag[equal_com] = new_label #Assign new label
                if pair[1] == temp_list[index]:
                    equal_com = pair[0]
                    if label_flag[equal_com] == 0:
                        temp_list.append(equal_com)
                        label_flag[equal_com] = new_label
            index += 1
            
    '''
    Mapping orignal label of run block to new one.
    At this time, 0 could be used as label.
    In the previous procedure, 0 was used as empty or invalid flag.
    '''
    for i in range(run_count):
        run_label[i] = label_flag[run_label[i]] - 1
    
    '''Create a list with object_info class'''
    object_set = [object_info() for i in range(new_label)]
    
    '''Achive connection labeled object information'''
    for i in range(run_count):
        index = run_label[i]
        if run_start[i] < object_set[index].left:
            object_set[index].left = run_start[i]
        if object_set[index].right < run_end[i]:
            object_set[index].right = run_end[i]
        if run_row[i] < object_set[index].up:
            object_set[index].up = run_row[i]
        if object_set[index].down < run_row[i]:
            object_set[index].down = run_row[i]
        object_set[index].area += run_end[i] - run_start[i] + 1
    
    '''Display result detection'''
    #bindata = int(bindata) * 255
    pl.figure('Connection label')
    pl.gray()
    pl.subplot(121)
    pl.imshow(src_img)
    pl.title('Orignal image')
    pl.axis('off')
    pl.subplot(122)
    pl.imshow(bindata)
    pl.title('Result')
    pl.axis('off')
    pl.gca()
    for i in range(new_label):
        pl.gca().add_patch(pl.Rectangle((object_set[i].left, object_set[i].up),\
        object_set[i].width, object_set[i].height, fill = False, color = (0,1,0)))

        
def degree2rad(x):
    return x / 180 * np.pi


def bilinear(img, x, y, x_offset, y_offset):
    xy = x_offset * y_offset
    output = (img[y, x] * (1 - x_offset - y_offset + xy)
                + img[y, x + 1] * (x_offset - xy)
                + img[y + 1, x] * (y_offset - xy)
                + img[y + 1, x + 1] * xy)
    return np.uint8(output)


def rotate_image(filename, rotate_degree=0, rotate_center_x=0, rotate_center_y=0):
    color_img = io.imread(filename)
    img_shape = color_img.shape
    if len(img_shape) > 2:
        gray_img = color.rgb2gray(color_img)
        gray_img = img_as_ubyte(gray_img)
    else:
        gray_img = color_img

    img_height, img_width = img_shape[0:2]
    rotate_img = np.zeros((img_height, img_width), dtype=np.uint8)
    # To protect array access, when use bilinear interpolate
    height_border = img_height - 2
    width_border = img_width - 2

    cos_value = np.cos(degree2rad(rotate_degree))
    sin_value = np.sin(degree2rad(rotate_degree))

    # New image original point in old image, rotate(-center_x, -center_y) and set to rotate center
    dx = -rotate_center_x * cos_value - rotate_center_y * sin_value + rotate_center_x
    dy = -rotate_center_y * cos_value + rotate_center_x * sin_value + rotate_center_y

    for i in range(img_height):
        for k in range(img_width):
            original_x = k * cos_value + i * sin_value + dx
            original_y = i * cos_value - k * sin_value + dy
            if original_x < 0 or original_y < 0 or width_border < original_x or height_border < original_y:
                pass
            else:
                integer_x = np.floor(original_x)
                integer_y = np.floor(original_y)
                rotate_img[i, k] = bilinear(gray_img, np.int(integer_x), np.int(integer_y),
                                            original_x - integer_x, original_y - integer_y)

    io.imshow(rotate_img)
