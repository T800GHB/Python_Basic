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