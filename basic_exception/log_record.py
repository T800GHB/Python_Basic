# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:57:00 2016

@author: T800GHB
This file will show how to use log record important message.
"""

import logging

def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def run_demo():
    try:
        bar('0')
    except Exception as e:
        logging.exception(e)
    print('END')


