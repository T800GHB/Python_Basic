# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:15:18 2016

@author: T800GHB
This file will show how to deal with exception.
"""

def error_demo():
    return 10 / 0

def run_demo():
    """
    This stript demostrate how to handle the exception
    """
    var = input('Input an number: ')
    #If some error will occur in this procedure, put it into try block.
    try:
        print('try...')        
        r = 10 / int(var)
        #Handle the exception happened in the called function.
        #So, you don't need to assign try block everywhere.
        #Just put try block on the spot where the exception may occur
        e = error_demo()
        print('result:', r, e)
    #If there are some exception, exception block will handle it according
    #to its type.
    except ValueError as e:
        print('ValueError:', e)
    except ZeroDivisionError as e:
        print('ZeroDivisionError:', e)
    #If no exception happened, else block will execute.
    else:
        print('no error!')
    #No matter what has happened, finally block will execute.
    finally:
        print('finally...')
    print('END')