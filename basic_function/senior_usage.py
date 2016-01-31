# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 10:26:31 2016

@author: T800GHB
This file will show some senior usage of function.
Something like, functional programming, lambda function.
"""

def add(x, y, func):
    return func(x) + func(y)

def high_order_function():
    """This script will show how to pass a function as a argument into another
    function.
    so, it will also show a usage of functional programming.
    """
    #abs is a built-in function, to calculate a absolute value
    func = abs
    #Name of function is a variable
    res = func(-5)
    #Pass a function as a argument
    res = add(-5, 6, func)
    print('The result of addition is :' , res)
    