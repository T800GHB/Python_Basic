# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 19:02:41 2016

@author: T800GHB
This file will show how to do some StingIO operation.
"""

from io import StringIO

def run_demo():
    """
    Read an write a string in local memory.
    This type of operation just like file that is a stream on device.
    """
    s = StringIO()
    s.write('Hello')
    s.write(' ')
    s.write('stream')
    s.write('\nGoodbye')
    #Use getvalue to achive the content in the stream
    print(s.getvalue())
    
    #Read the content frome StringIO
    sr = StringIO('\nHello\nGoodbye')     
    #Use readline to achive the content in the string stream
    for c in sr.readlines():
        print(c)
    