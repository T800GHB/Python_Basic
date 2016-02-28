# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 19:29:07 2016

@author: T800GHB
This file will show how to do some byte IO operation.
"""

from io import BytesIO

def run_demo():
    """
    Do some operation on local operation as byte stream.
    """
    b = BytesIO()
    b.write('中文'.encode('utf-8'))
    #Print out as 0x value
    print(b.getvalue())
    
    br = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
    s = br.read()
    print(s)