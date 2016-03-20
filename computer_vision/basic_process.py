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