#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 16:25:14 2017

@author: andrew

This model will provide some helpful function or class
"""

import sys

class process_bar(object):
    '''
    This class could display a process bar onto console
    '''
    def __init__(self, num_items, bar_length = 50, init_count = 0.0):
        self.__process_bar_length = bar_length
        #The factor of percent must be not integer
        self.__num_files = float(num_items)
        self.__file_count = float(init_count)
    def update(self):
        '''
        Use this this method in the loop of program
        '''
        self.__file_count += 1
        percent = self.__file_count / self.__num_files
        has_done = '#' * int(percent * self.__process_bar_length)
        spaces = ' ' * (self.__process_bar_length - len(has_done))
        sys.stdout.write("\rPercent: [%s] %d%%"%(has_done + spaces, percent * 100))
        sys.stdout.flush()