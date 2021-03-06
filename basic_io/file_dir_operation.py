# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 21:33:06 2016

@author: T800GHB
This file will show how to deal with directory.
"""

import os
import shutil
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

def distribute_files(src_dir, dst_prefix, group_capcaity):
    '''
    This tool will distribut files in one directory into many directories.
    Each new directory capacity is specific.
    group_capcaity is max capcaity of each directory
    '''
    #Get file names, not include directories
    dirlist = os.listdir(src_dir)
    files = [x for x in dirlist if not os.path.isdir(x)]
    num_files = len(files)
    #If the names of file in this directory does not keep same length, append zeros before them
    max_files_len = max([len(x) for x in files])
    pad_char = '0'

    for i in range(num_files):
        filename_len = len(files[i])
        if filename_len < max_files_len:
            num_pad = max_files_len - filename_len
            #Repeat specific charater
            new_name = num_pad * pad_char + files[i]
            #Rename it and record in orignal list
            os.rename(os.path.join(src_dir, files[i]), os.path.join(src_dir, new_name))
            files[i] = new_name
    #Sort file name
    files.sort()    
    
    order_capacity = len(str(num_files // group_capcaity))
    
    for i in range(num_files):
        if i % group_capcaity == 0:
            dst_dir = os.path.join(dst_prefix, 
                                   os.path.split(src_dir)[-1] + '_'
                                   + (order_capacity - len(str(i // group_capcaity))) * pad_char
                                   + str(i // group_capcaity))
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            else:
                #Do not keep orignal directory and files under this one
                shutil.rmtree(dst_dir)
                os.makedirs(dst_dir)

        shutil.copy(os.path.join(src_dir, files[i]), dst_dir)  

def aggregate_files(src_dir, dst_dir):
    '''
    This tool will gether files from different directories into one directory
    '''
    #Find all the directories
    dir_list = [x for x in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, x))]
    #Pay attention to parameter of os.path, if you just assign name, it will not work
    #Please add path to the directory or file
    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
        os.makedirs(dst_dir)
    else:
        os.makedirs(dst_dir)
    #Copy to one driectories
    num_dirs = len(dir_list)
    for i in range(num_dirs):
        src_path = os.path.join(src_dir, dir_list[i])
        file_list =  [x for x in os.listdir(src_path) if os.path.isfile(os.path.join(src_path,x))]
        for f in file_list:
            shutil.copy(os.path.join(src_path,f), dst_dir)
