# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 21:59:14 2016

@author: T800GHB
This file contain some exmaple how to define and use a function.
"""

"""
The content of this function show how to call function
"""
def call_basic():
    var = max(5,4)
    print('The greater one is :' , var)
    var = max(0,2,3,6,7,-1)
    print('The max of this set is :', var)
    nums = [1,2,43,5,67,9]
    print('The max of this list is :', max(nums))
    
def type_convert():
    str_var = '100'
    int_var = 200
    float_var = 11.102
    bool_var = True
    print('Convert float to int :', int(float_var))
    print('Convert str to int :' , int(str_var))
    print('Convert int to bool :', bool(int_var))
    print('Convert int to str :', str(int_var))
    print('Convert float to str :', str(float_var))
    print('Convert str to float :', float(str_var))
    print('Convert bool to int :', int(bool_var))
    print('Convert bool to float :', float(bool_var))
    print('Convert bool to str :', str(bool_var))
    
def controler():    
    """
    This function will be a controler that can be used to call other function.
    """
    x = 5
    y = -4
    str_var = '10'
    summation, product = multi_return(x, y)
    print('Result of multi_return is : %d, %d', %(summation, product))
    abs_var = abs_param_check(y)
    print('Result of abs is : ', abs_var)
    abs_var = abs_param_check(str_var)
    print('Result of abs is : ', abs)
    

def virtual_func():
    """This is a virtual function, so we must add a key word 'pass' in the body.
    """
    pass

def abs_param_check(x):
    """This function will check the type of parameter, 
    if the input type can't match what we want, we will throw a exception.
    """
    if not isinstance(x, (int,float)):
        raise TypeError('Bad operand type')
        
    if x >= 0:
        return x
    else:
        return -x
    
def multi_return(x,y):
    """This function will take two parameter then do multiplication and add.
    Finally, Two results return to caller at same time.
    """
    summation = x + y
    product = x * y
    return summation, product
    
    
