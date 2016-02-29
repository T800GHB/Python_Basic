# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 21:20:30 2016

@author: T800GHB
This file will show how to serialize some file to disk.
"""
import pickle

def run_demo():
    """
    Serialize a object to disk, then reload it.
    The object will be serialzied to a binary string.
    """
    dw = dict(name = 'Jack', age = 28, job = 'engineer')
    #Write a dictionary object to disk as binary format.
    with open('./test.txt', 'wb') as fw:
        pickle.dump(dw, fw)
        
    #Load a binary file from disk
    with open('./test.txt', 'rb') as fr:
        dr = pickle.load(fr)
        
    print(dr)
    
