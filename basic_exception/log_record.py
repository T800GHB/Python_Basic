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

def error_demo():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)    
    # create a file handler    
    handler = logging.FileHandler('error.log')    
    handler.setLevel(logging.INFO)   
    # create a logging format    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)    
    # add the handlers to the logger    
    logger.addHandler(handler)    
    logger.info('Hello, this is a error logging demo.')
    try:
        bar('0')
    except Exception as e:
        #Use exc_info=True to record call stack
        logger.error('Incorrect usage: ', exc_info = True)
        #Or use like this for exception
        #logger.exception('Wrong usage: ')
        
def output_demo():
    '''
    The default level is warning, 
    so the level higher than warning will sent out message.
    The level order is 
    CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET
    '''
    logging.debug('debug message')  
    logging.info('info message')  
    logging.warning('warning message')  
    logging.error('error message')  
    logging.critical('critical message') 
    