# -*- coding: utf-8 -*-
"""
Created on Tue Aug 30 11:03:28 2016

@author: Hanbing Guo
"""

import struct as st
import pylab as pl
import numpy as np
import scipy as sp

#is_centered 0 means centered data, 1 means orignal data stored in numpy array
def load_mnist(is_centered = 0):    
#==============================================================================
#     This block of code load MNIST dataset into memory
#==============================================================================
    '''Specifiy file path'''
    train_image_filename = './image_process/MNIST/train-images.idx3-ubyte'
    train_label_filename = './image_process/MNIST/train-labels.idx1-ubyte'
    test_image_filename = './image_process/MNIST/t10k-images.idx3-ubyte'
    test_label_filename = './image_process/MNIST/t10k-labels.idx1-ubyte'
    '''Load train image data, store it into a n-dimensional numpy array'''
    with open(train_image_filename, 'rb') as binfile:
        buf = binfile.read()
        '''Index to indicate location of file'''
        index = 0 
        '''Use big-endian to read data information'''
        magic, numImages, rows, cols = st.unpack_from('>IIII', buf, index)
        train_image = np.zeros((numImages, rows, cols))
        index += st.calcsize('>IIII')
        for i in range(numImages):
            train_image[i,:,:] = np.array(st.unpack_from('>784B', buf, index)).reshape(rows, cols)
            index += st.calcsize('>784B')                
        
    with open(train_label_filename, 'rb') as binlabel:
        buflabel = binlabel.read()
        label_index = 0
        lmagic, numLabels = st.unpack_from('>II',buflabel, label_index)
        label_index += st.calcsize('>II')
        train_label = np.zeros((numLabels,), dtype = np.uint8)
        for i in range(numLabels):
            train_label[i] = np.uint8(st.unpack_from('1B',buflabel, label_index))
            label_index += st.calcsize('>1B')
    
    with open(test_image_filename, 'rb') as test_binfile:
        buf_test = test_binfile.read()
        index_test = 0
        t_magic, t_numImages, t_rows, t_cols = st.unpack_from('>IIII',buf_test, index_test)
        index_test += st.calcsize('>IIII')
        test_image = np.zeros((t_numImages, t_rows, t_cols))
        for i in range(t_numImages):
            test_image[i,:,:] = np.array(st.unpack_from('>784B', buf_test, index_test)).reshape(t_rows, t_cols)
            index_test += st.calcsize('>784B')
    
    with open(test_label_filename, 'rb') as test_binlabel:
        buf_test_label = test_binlabel.read()
        index_label = 0
        lt_magic,lt_numLabels = st.unpack_from('>II', buf_test_label, index_label)
        index_label += st.calcsize('>II')
        test_label = np.zeros((lt_numLabels,), dtype = np.uint8)
        for i in range(lt_numLabels):
            test_label[i] = np.uint8(st.unpack_from('1B', buf_test_label, index_label))
            index_label += st.calcsize('>1B')        
    
    #Calculate mean image for entire data set
    mean_image = np.zeros((rows, cols))
    for i in range(numImages):
        mean_image += train_image[i,:,:]
    
    mean_image /= numImages
    
    '''Zero mean process'''
    if is_centered == 0:
        train_image -= mean_image
        test_image -= mean_image
    '''
    It's ok, The order in MNIST has been shuffled.
    If it did not, you could use this index
    
    >>>index = np.arange(numImages)
    >>>np.ramdom.shuffle(index)
    '''
    
    pl.figure('First try')
    pl.gray()
    pl.imshow(mean_image)
    
    sp.misc.imsave('mean_image.bmp', mean_image)

    
    return train_image, train_label, test_image, test_label, mean_image
    
    
