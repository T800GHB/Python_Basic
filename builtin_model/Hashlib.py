# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 21:43:40 2016

@author: T800GHB

This file will demostrate how to use hashlib to calculate MD5, SHA1 value.
"""
import hashlib

def run_demo():
    """
    Message digest algorithms 
    Any length of file could calculate a MD5 or SHA1 value with fixed length.    
    """
    md5 = hashlib.md5()
    md5.update('How to be a good algorithm engineer.'.encode('utf-8'))
    print(md5.hexdigest())
    
    #If the file too big to load at once, you can calculate partically.
    md5_2 = hashlib.md5()
    md5_2.update('How to be a good '.encode('utf-8'))
    md5_2.update('algorithm engineer.'.encode('utf-8'))
    print(md5_2.hexdigest())
    
    sha1 = hashlib.sha1()
    sha1.update('How to be a good algorithm engineer.'.encode('utf-8'))
    print(sha1.hexdigest())