# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 21:33:06 2016

@author: T800GHB
This file will show how to deal with directory.
"""

import os
#Copy file and other senior operation is contain in shutil model

def run_demo():
    #Print out the system type
    print(os.name)
    #Print out the detail system information
    print(os.uname())
    #Print out the environment variable
    print(os.environ)
    #Get the specific environment variable
    print(os.environ.get('PYTHONPATH'))
    #Get absolute path of current directory, argument means current directory
    print(os.path.abspath('.'))
    #Combine two directory then create new one.
    print(os.path.join('.','testdir'))
    #Separate file name and path
    print(os.path.split('user/path/filename.txt'))
    #Get the extension of file. The second element in tuple is extension.
    print(os.path.splitext('user/path/filename.txt'))
    #List all of file contain in the specific directory.Now upper.
    print(os.listdir('..'))
    #Creat a file
    with open('test.txt','w') as f:
        f.write('test')
    #Rename a file
    os.rename('test.txt', 'test.py')
    #Delete a file
    os.remove('test.py')
    #Create a new directory with full path
    os.mkdir('./testdir')
    #remove a existed directory with full path
    os.rmdir('./testdir')
    #list all the directory in current directory
    print([x for x in os.listdir('.') if os.path.isdir(x)])
    #list all .py file contain in current directory
    print([x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py'])
    

