# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 10:26:31 2016

@author: T800GHB
This file will show some senior usage of function.
Something like, functional programming, lambda function.
"""

def add(x, y, func):
    return func(x) + func(y)
    
def square(x):
    return x*x
    
def combine(x, y):
    return x*10 + y
    
def is_odd(x):
    return x % 2 == 1

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
    
def map_reduce():
    """This script will show how use a high-level function map and reduce
    """
    list_var = [0,1,2,3,4,5,6,7,8,9]
    #Map require two argument as input, a function work on each element and data
    res = map(square, list_var)
    #The return value will be a iterator, so we need to convert to a list for display
    print('The result of map is :', list(res))
    from functools import reduce
    #reduce function will work on two continuous element 
    res = reduce(combine, list_var)
    print('The result of reduce is :', res)
    
def filter_usage():
    """This script will show how to use bulit-in filter function.
    filter function will receive a function and data as input.
    The element will be reserved that function work on it return true
    """
    list_var = [0,1,2,3,4,5,6,7,8,9]
    res = filter(is_odd, list_var)
    #The return object is a iterator
    print('The result of filter is :',list(res))
    
    

    