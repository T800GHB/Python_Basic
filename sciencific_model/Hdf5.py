# -*- coding: utf-8 -*-
"""
Created on Fri Jan 12 10:17:43 2018

@author: hanbing.guo
"""

import h5py
import numpy as np

"""
Group just like dict, it will create directory-like struct
Dataset just like array
"""
def demo_hdf5():
    arr = np.arange(12, dtype = np.int32)
    ones = np.ones((2,4), dtype = np.float,)
    zeros = np.zeros(4, dtype = np.int8)
    randn = np.array(np.random.randn(1000,1000), dtype = np.float32)
    
    # Create a empty dataset
    with h5py.File('Test0.hdf5','w') as fh:
        d1 = fh.create_dataset('dset0', (12,), 'i')
        d1[...] = arr
        for k in fh.keys():
            print(fh[k].name)
            print(fh[k].value)
    
    # Create a dataset with numpy array
    with h5py.File('Test1.hdf5', 'w') as fh:
        d2 = fh.create_dataset('dset1', data = arr)
        for k in fh.keys():
            print(fh[k].name)
            print(fh[k].value)
    
    # Assign content directly
    with h5py.File('Test2.hdf5', 'w') as fh:
        fh['arr'] = arr
        fh['ones'] = ones
        fh['zeros'] = zeros
        
    with h5py.File('Test2.hdf5', 'r') as fh:
        for k in fh.keys():
            print(k)
            print(fh[k].name)
            print(fh[k].shape)
            print(fh[k].value)
        receive = np.array(fh['arr'])
        
    # Create a group
    with h5py.File('Test3.hdf5', 'w') as fh:
        # Create a group named 'set'
        group = fh.create_group('set')
        # Assign content into this group
        group['dset0'] = arr
        group['dset1'] = ones
        for key in group.keys():
            print(group[key].name)
            print(group[key].value)
            
    # Create multi-fold group
    with h5py.File('Test4.hdf5', 'w') as fh:
        #Top hierarchy
        group1 = fh.create_group('set1')
        group2 = fh.create_group('set2')
        dset1 = fh.create_dataset('dset1', data = arr)
        
        #Second hierarchy
        c1 = group1.create_group('car1')
        group1['dset2'] = ones
        
        c2 = group2.create_group('car2')
        group2['dset3'] = zeros
        
        print('\nGroup and dataset on the root')
        for k in fh.keys():
            print(fh[k].name)
        
        print('\nGroup and dataset on the group1')
        for k in group1.keys():
            print(group1[k].name)
            
        print('\nGroup and dataset on the group2')
        for k in group2.keys():
            print(group2[k].name)
        
        print('\nContent in c1 and c2')
        print(c1.keys())
        print(c2.keys())
        
        print('\nType discrimination')
        print(type(c2) == h5py.Group)
        print(type(group2['dset3']) == h5py.Dataset)
        
    # Create a chunked dataset
    with h5py.File('Test5.hdf5', 'w') as fh:
        # Automatic chunk data
        # Auto-chunking is also enabled when using compression or maxshape
        dset = fh.create_dataset("autochunk-data", data = randn, chunks=True)
        for k in fh.keys():
            print(k)
            print(fh[k].name)
            print(fh[k].shape)
    
    with h5py.File('Test6.hdf5', 'w') as fh:
        # Specific chunk size manually
        dset = fh.create_dataset("fixed-size-data", data = randn, chunks = (100,100))
        for k in fh.keys():
            print(k)
            print(fh[k].name)
            print(fh[k].shape)
    
    # Create a compression file
    with h5py.File('Test7.hdf5', 'w') as fh:
        #Specific type of compression as 'gzip'
        dset = fh.create_dataset('zip-file', data = randn, compression = 'gzip')
        for k in fh.keys():
            print(k)
            print(fh[k].name)
            print(fh[k].shape)
