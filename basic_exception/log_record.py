# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:57:00 2016

@author: T800GHB
This file will show how to use log record important message.

"""

import logging
import logging.config
import basic_exception.model_log as bm

'''
TODO:
    RotatingFileHandler demostration
'''

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
    '''
    How to capture a exception by logger adn record ti to a file.
    '''
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
    
def config_demo():
    '''
    This code block will demostrate how to create logger 
    with file handler, stream handler and filter
    '''
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    #Create a file handler for recording log to file
    fh = logging.FileHandler('/tmp/python_test.log')
    #Create a stream handler for sending log information to console
    sh = logging.StreamHandler()
    #Define format for handler
    formatter = logging.Formatter('%(asctime)s-%(name)s-%(lineno)d-%(levelname)s-%(message)s')  
    fh.setFormatter(formatter)
    sh.setFormatter(formatter)
    #Add handlers to logger
    logger.addHandler(fh)
    logger.addHandler(sh)
    #Create log filter to find out which part of log could send out
    fl = logging.Filter('basic_exception.log_record')
    logger.addFilter(fl)    
    
    logger.debug('logger debug message')  
    logger.info('logger info message')  
    logger.warning('logger warning message')  
    logger.error('logger error message')  
    logger.critical('logger critical message')  
    
def config_file_demo():
    '''
    Load configuration of log from file
    '''
    '''
    disable_existing_loggers=False is serious important.
    If not set this parameter as false, you will distroy logging instance
    when you load configration file.
    Consequence is that logging instance in submodel will not work.
    '''
    logging.config.fileConfig('./basic_exception/logging.conf',disable_existing_loggers=False) 
    '''   
    If you want to use specific name of configuration, this line will work
    logger = logging.getLogger('simpleExample')
    If you want to use model name in log output, just use __name__ when you
    call getLogger, this configuration reference from root.
    
    basicConfig and dictConfig is not convenient, so as JSON and YAML
    '''
    logger = logging.getLogger(__name__)    
    logger.debug('logger debug message')  
    logger.info('logger info message')  
    logger.warning('logger warning message')  
    logger.error('logger error message')  
    logger.critical('logger critical message')  
    #Test work status of logging instance in submodel 
    bm.test_logger()