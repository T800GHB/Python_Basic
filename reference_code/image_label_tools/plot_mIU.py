# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 16:56:55 2017

@author: andrew
"""

from collections import namedtuple
import pylab as pl
import numpy as np
import argparse
import os
import os.path as op

IU_item = namedtuple('IU_item',['iter', 'mIU'])

def plot_process(args):
    
    if not op.exists(args.input):
        raise IOError('Can not find file at location: ', args.input)
    
    with open(args.input,'r') as fh:
        txt_list = fh.readlines()
        
    val_info_list = [x for x in txt_list if x.split(' ')[0] == '>>>' and 'mean IU' in x]
    
    if val_info_list:
    
        IU_list = []
        
        for info in val_info_list:
            record = info.split(' ')
            
            item = IU_item(int(record[4]), float(record[-1]))
            
            IU_list.append(item)
            
        length = len(IU_list)
        
        x = np.empty(length, dtype = np.int)
        y = np.empty(length, dtype = np.float)
        
        for i, item in enumerate(IU_list):
            x[i] = item.iter
            y[i] = item.mIU
             
        max_index = np.argmax(y)
        min_index = np.argmin(y)
        
        pl.figure('mean IoU')
        pl.plot(x,y,'green')
        pl.plot([x[max_index],x[max_index]],[y[min_index] * 1.05 ,y[max_index]], color='red', linestyle= '--')
        
        pl.text(x[length // 2],y[0],"iter: %d, mean IU: %.2f%%"%(x[max_index], y[max_index] * 100))
        
        if not op.exists(args.output):
            os.makedirs(args.output)
        pl.savefig(op.join(args.output,'train_log.png'),dpi = 128)
        
    else:
        raise IOError('Invalid log file')

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(                                     
    description= '''Visualize FCN train log, result will name as train_log.png''',
    formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument('-i', '--input', type = str, default = './train_log.txt',
                        help = 'Input train log')
    parser.add_argument('-o', '--output', type = str, default = './',
                        help = 'Output directory picture')
        
    args = parser.parse_args()
    plot_process(args)