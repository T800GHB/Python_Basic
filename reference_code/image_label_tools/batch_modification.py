# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 12:07:25 2017

@author: andrew

Batch change some element of xml file
"""

from xml.etree import ElementTree
import os
import os.path as op
import shutil
import assist_util as au
import argparse

def main_process(args):
    src_path = args.src
    dst_path = args.dst
    dst_dir = op.basename(dst_path)
    src_dir = op.basename(src_path)
    if dst_dir == src_dir:
        raise IOError('Source and destination directory must be different')
    
    dir_list = os.listdir(src_path)
    
    files = [f for f in dir_list if op.isfile(op.join(src_path, f))]
    num_files = len(files)
    if not num_files:
        raise IOError('Source directory is empty')
    
    if op.exists(dst_path):
        shutil.rmtree(dst_path)
        os.makedirs(dst_path)
    else:
        os.makedirs(dst_path)
        
    bar_worker = au.process_bar(num_files)
    
    for f in files:
    
        tree = ElementTree.parse(op.join(src_path, f))
        
        root = tree.getroot()
                      
        root.find('folder').text = str(dst_dir)
        
        tree.write(op.join(dst_path, f))
        
        bar_worker.update()
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(                                     
    description= 'Change name of xml',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-s','--src', type = str, default = None,
                        help = 'Source directory that contain xml files')
    parser.add_argument('-d','--dst', type = str, default = None,
                        help = 'Destination directory to store xml files')
    args = parser.parse_args()
    main_process(args)
    