# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 20:54:01 2016

@author: T800GHB

This file will demostrate how use basic function offered by numpy model.

Numpy is designed to stroe multi-dimensional array, it's called ndarray.
Array in numpy is so different from array in native python.
In numpy, dimensions named axes, number of axes called rank.
For example, 3D coordiante [1,2,3] is a array of rank 1 and length 3.
[[1,2,3],
[4,5,6]]    
is a array of rank 2. Length of first rank is 2, and second rank is 3.

There some introduction about attribute of numpy's array:
ndarray.ndim
    rank of ndarray
ndarray.shape
    dimensions of array. It's a tuple indicate length of array in each dimension.
ndarray.size
    total elements of array. It equal to product of element in shape.
ndarray.dtype
    type of element in array.
ndarray.itemsize
    size of element in array.
ndarray.data
    buffer that store the real element of array. We will not use it directly.
    but get reference.
"""

"""
I just want to distinguish between numpy and native python,
so choose import numpy as np instead of from numpy import *
"""
import numpy as np

def demo_attribute():
    """
    np.arange(n) is a function that return a continuous integer from 0 to n.
    Pass (n, m , s) to arange means create sequence integer from n to m with interval s.
    np.reshape(*args) is a function that form a new array with specific dimensions.    
    """
    a = np.arange(12).reshape(3,4)
    print('Data :\n', a)
    print('Shape:\n', a.shape)
    print('Rank:\n', a.ndim)
    print('Type:\n', a.dtype.name)
    print('Size of element:\n', a.itemsize)
    print('size of array:\n', a.size)
    
def demo_create():
    """
    Create numpy array by ways:
    1.normal list or tuple.
    2.numpy function. For example, zeros, ones etc.
    """
    a = np.array([1,2,3])
    print('Array create from list\n', a)
    b = np.array([(1.1,2.0,3.6),(4,5,6)])
    print('Two dimensional array create from list of tuple\n',b)
    """
    Pass a type as paramter to array, new array will create as this type.
    """
    f = np.array([[1,2], [3,4]], dtype = complex)
    print('Array with complex type\n', f)
    """
    zeros() will create a array with all zero.
    ones() will create a array with all one.
    empty() will create a array with random number that rely on memory state.
    Pass a tuple as shape to those function.
    Those function use float64 as default type.
    """
    z = np.zeros((3,4))
    print('All zero array\n', z)
    o = np.ones((2,5), dtype = int)
    print('All one array\n', o)
    e = np.empty((2,3))
    print("'empty' array\n", e)
    """
    Create a sequence that contain specific number of element.
    linspace could produce sequence with high precision.
    """
    l = np.linspace(1, 20, 16)
    print('Line space sequence\n', l)
    
    
    


