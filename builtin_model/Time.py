# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 23:15:07 2016

@author: T800GHB

This file will demostrate how to count time using time model.
Unit of clock() is second.
"""

import time
import math
import numpy as np

def demo_interval():
    """
    Using sin() function from math and numpy to compare time comsume.
    In python 3, xrange has changed to range, it's also a generator,
    if you want to acquire a list, call list() explicitly.
    """
    x = [i*0.01 for i in range(10000000)]
    """clock()---get current CPU time"""  
    start = time.clock()
    """enumerate will return a pair containing a count(index = 0) and a value"""
    for i,t in enumerate(x):
        x[i] = math.sin(t)
    print('math sin: ', time.clock() - start)
    
    x = [i*0.01 for i in range(10000000)]
    x = np.array(x)
    start = time.clock()
    """
    numpy.sin() is a ufunc.
    If the second argument is same as first one, 
    it means return result to orignal location.
    """
    np.sin(x, x)
    print('numpy sin: ', time.clock() - start)
    """
    In this comparison, nump.sin is faster than math.sin,
    But, if you just want to calculate only one value, math.sin will be faster.
    """
