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
    
def lazy_sum(*args):
    """This script show how to return a function as output.
    Pay attention to the time that returned function really run.
    """
    def sum_fun():
        """The inner function could access argument and local variable
        external function.
        """
        summation = 0
        for item in args:
            summation += item
        return summation
    return sum_fun
    
def return_lambda(x = 0, y = 0):
    return lambda  x,y :x * x + y*y
    
            

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
    
def sorted_usage():
    """This script will show  how to use high-level property about sorted function.
    We can input a function to sorted, then the output order will be as our wish.
    """
    list_var = [23, 45, -4, -98, -200, 500]
    res = sorted(list_var)
    print('The result of orignal sorted is :', res)
    #Use key function on sort procedure.
    res = sorted(list_var,key=abs)
    print('The result of key order is :', res)
    #Reverse it, Pay attention to reverse is a key argument
    res = sorted(list_var,key=abs, reverse = True)
    print('The result of reverse is :', res)    
    
def return_function():
    """This script will show how to use function as return value.
    The most important thing is that return will not implement immediately,
    but when call it.
    """
    fp = lazy_sum(1,2,3,4,5,6,7)
    print('This is a function object', fp)
    sum_var = fp()
    print('This is a result of lazy_sum :', sum_var)
    
def lambda_function():
    """This script will show how to use lambda function.
    lambda function is a temporary function object, so we don't need to care
    name confliction. 
    """
    list_var = [1,2,3,4,5,6,7,8,9,0]
    #Use lambda to define a temporary function and take it as input
    #Use lambda key word and assign a argument behind it, the express add 
    #back on colon
    res = map(lambda x : x*x , list_var)
    print('The result of mapping a list is :', list(res))
    #A lambda function could assign to a function object.
    fp = lambda x : x*x
    print('The result of lambda function object is:', fp(9))
    #This kind of usage is so bad, if i do not assign a defult value to 
    #positional arguments
    fp = return_lambda()
    print('The result of returned lambda function object is:', fp(3,7))
    
    
    
    
    
    
    

    