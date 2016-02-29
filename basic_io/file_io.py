# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 18:01:32 2016

@author: T800GHB
This file will show how to do some basic operation about file.
The recommend model to do IO operation is that use 'with' keyword
"""


def run_demo():
    """
    Open a file with readonly model.
    If the file does not exist, it will raise an IOerror.
    when we don't want to use this file anymore, close it, otherwise
    this part of system resource will not release.
    """
    try:
        f1 = open('filepath/filename', 'r')
        f1.read()
    finally:
        if f1:
            f1.close()
    """
    Use with keyword and open a file same like above block,
    and you don't need to call close function.
    """
    with open('filepath/filename','r') as f2:        
        """
        Read all of file, and store it at fp.
        When the file is close, it also exist.
        If open a file with 'r+' model, then the file can be wirte
        """
        fp1 = f2.read()
        #Read the specific size of file.
        fp2 = f2.read(1)
        #Read a line in this file.
        fp3 = f2.readline()
        """
        Read all of the lines in this file and return as list. 
        fp3 is a list contain all line.
        """
        fp4 = f2.readlines()
        
    with open('filepath/filename.bmp', 'rb') as f3:
        """
        Read a binary file and stroe it at local memory
        """
        bitmap = f3.read()
        
    with open('filepath/filename.txt','r',encoding = 'gbk', error ='ignore') as f4:
        """
        Read a text file that encoding type is not UTF-8, and ignore all 
        error when the read procedure encounter some illegal character
        """
        text = f4.read()
        
    with open('filepath/filename.txt', 'w') as f5:
        """
        Write some content into file.
        """
        f5.write('Hello my mind')
        #Make the pointer loacate to the head of file
        f5.seek(0)
        
    with open('filepath/filename.txt', 'a') as f6:
        """
        Write some content to the rear of file, that means append it on rear.
        If you open a existed file on 'w' model, system will clear the file
        and write something what you want.
        If you want to make sure whether the file has existed, you should us
        os.path.isfile('filename') to confirm.
        """
        f6.write('Hello again')
        
        
        
    
