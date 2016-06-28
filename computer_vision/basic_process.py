# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 22:20:53 2016

@author: T800GHB

This file will demostrate how to use PIL , numpy and matplotlib to process
image.
"""

from PIL import Image
import numpy as np
import pylab as pl
import os

def get_imlist(path):
    """
    Return a list of name that format is jpg in specific directory.
    """
    return [os.path.join(path,f) for f in os.listdir(path) if f.endwith('jpg')]

def demo_PIL():
    """
    Image model include most frequently used tools.
    open() could open a image file and return PIL object.
    """
    img = Image.open('./computer_vision/scenery.jpg')
    """Create a new image , not just reference copy"""
    im = img.copy()
    width, height = im.size
    print('Image width %d, height %d.'%(width, height))
    """convert('L') return grey image."""
    im_grey = im.convert('L')
    """save image as specific path and name"""
    im_grey.save('grey.jpg')    
    """Achive specific part from orignal image"""
    box = (100,200,300,300)
    region = im.crop(box)
    """Rotate image with fixed degree"""
    region = region.transpose(Image.ROTATE_180)
    """Paste a image onto another one"""
    im.paste(region,box)
    """Resize a image"""
    im_re = img.resize((256,256))
    im_re.save('resize.jpg')
    """Rotate a image with specific degree"""
    im_ro = img.rotate(45)
    im_ro.save('rotate.jpg')
    """create a thumbnail as specific max side length. I've tried output 64*42"""
    im.thumbnail((64,64))
    """formation convertion --- change postfix"""
    im.save('thumbnail.png')
    """
    display image.
    I don't know why this can't work on linux, but windows made it.
    I expect there is a window to display no matter what form it is.
    """
    im.show()
    
    
def demo_mpl():
    """
    Open a image file and store it in a numpy array, draw something on it.
    """
    im = np.array(Image.open('./computer_vision/scenery.jpg'))
    pl.imshow(im)
    x = [100, 100, 400, 400]
    y = [200, 500, 200, 500]    
    pl.plot(x,y,'r*')
    pl.plot(x[:2],y[:2],'y-')
    pl.title('Picture: scenery.jpg')
    """turn off the axis"""
    pl.axis('off')
    pl.show()
    
def demo_channel():
    """
    Open a image, store it in a numpy array.
    """
    im = np.array(Image.open('./computer_vision/scenery.jpg'))    
    print('Shape of image is ', im.shape)
    """
    Demostate different channel.
    """    
    red = np.zeros(im.shape)
    red[...,0] = im[...,0]
    green = np.zeros(im.shape)
    green[...,1] = im[...,1]
    blue = np.zeros(im.shape)
    blue[...,2] = im[...,2]
    pl.figure('Different channel')
    pl.subplot(2,2,1)
    pl.title('Orignal image')
    pl.axis('off')
    pl.imshow(im) 
    pl.subplot(2,2,2)
    pl.title('Red Channel at 1')
    pl.axis('off')
    pl.imshow(red)
    pl.subplot(2,2,3)
    pl.title('Green Channel at 2')
    pl.axis('off')
    pl.imshow(green)
    pl.subplot(2,2,4)
    pl.title('Blue Channel at 3')
    pl.axis('off')
    pl.imshow(blue)
    
    
def demo_contour():
    """
    Show the contour and histogram of image.
    """
    im = np.array(Image.open('./computer_vision/scenery.jpg').convert('L'))
    """Create a new figure, then plot on it, just like a new canvas"""
    pl.figure('Image information')
    """Do not use color information"""
    pl.gray()
    """Create a subplot on this figure, allocate location"""
    pl.subplot(1,2,1)
    """Contour image"""
    pl.contour(im, origin='image')
    """equal increments"""
    pl.axis('equal')
    pl.axis('off')
    """
    Calculate histogram. We should flatten data firstly,
    then specify number of bins
    """
    pl.subplot(1,2,2)
    pl.hist(im.flatten(), 128)
    pl.show()

def demo_interactive():
    """
    Interactive label
    """    
    im = np.array(Image.open('./computer_vision/scenery.jpg'))
    pl.imshow(im)
    print('Please click 3 points')
    """Get mouse click input from GUI"""
    x = pl.ginput(3)
    print("You've clicked:",x)
    pl.show()
    
def demo_graymapping():
    """
    Gray space mapping, just change the way of distribution
    """
    im = np.array(Image.open('./computer_vision/scenery.jpg').convert('L'))
    """Reverse mapping"""
    im_r = 255 - im
    """Mapping gray space to specific range[100, 200]"""
    im_f = (100.0 / 255) * im + 100
    """Square pixel value"""
    im_s = 255 * (im/ 255.0)**2
    """Show image"""
    pl.figure('Gray space mapping')  
    pl.gray()
    pl.subplot(2,2,1)
    pl.title('orignal gray image')
    pl.imshow(im)
    pl.subplot(2,2,2)
    pl.title('Reversed gray')
    pl.imshow(im_r)
    pl.subplot(2,2,3)
    pl.title('Mapping to a [100,200]')
    pl.imshow(im_f)
    pl.subplot(2,2,4)
    pl.title('Square pixel value')
    pl.imshow(im_s)    
    pl.show()
    
def demo_histeq():
    """
    Gray histogram equalization, make every gray value have same distribution.
    This process could imporve contrast of image.
    """
    im = np.array(Image.open('./computer_vision/scenery.jpg').convert('L'))
    imhist, bins = np.histogram(im.flatten(), bins = 256, normed = True)
    cdf = imhist.cumsum()
    """Normalization"""
    cdf = 255 * cdf / cdf[-1]
    im_n = np.interp(im.flatten(),bins[:-1], cdf)
    """
    Image of equalization.
    I don't know why reshape() function can't modify shape attribute, 
    it just change the arrangement of output if you print it out.
    I've tried when you create a array with reshape(), it works.
    """
    #im_n.reshape(im.shape)
    im_n.shape = im.shape
    
    pl.figure('Histogram equalization')
    pl.subplot(1,2,1)
    pl.gray()
    pl.imshow(im)
    pl.title('Orignal gray image')
    pl.subplot(1,2,2)
    pl.gray()
    pl.imshow(im_n)
    pl.title('equalized image')
    pl.show()
    
def demo_average():
    """
    Calculate a mean of images.
    """
    imlist = os.listdir(image_floder)       #Set path to floder of images
    """Open first image, then store it to a float array"""
    average_im = np.array(Image.open(imlist[0]),'f')
    
    for imname in imlist[1:]:
        try:
            average_im += np.array(Image.open(imname))
        except:
            print(imname + '...skipped')
    average_im /= len(imlist)
    
    pl.figure('Mean image')
    pl.imshow(average_im)
    pl.axis('off')
    pl.show()