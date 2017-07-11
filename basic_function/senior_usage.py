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
    
    
def fun_name(func):
    """This function define a decorator, it will reinforce other function
    by use @ ahead on what we want to be better.
    """
    def additional(*args, **kw):
        print('Call %s()'%(func.__name__))
        return func(*args, **kw)
    return additional

"""Use decorator
"""
@fun_name
def now():
    print('2016-2-2')

#This decorator will not run function
def check_info(func):
    def warp(age, weight, height):
        if type(age) != int:
            raise IOError('Age with incorrect format')
        if 100 < weight :
            raise IOError('Weight out of range')
        if 300 < height:
            raise IOError('Height out of range')
        return func(age, weight, height)
    return warp

import time

def time_cost(func):
    def warp(*args, **kw):
        start = time.clock()
        result = func(*args, **kw)
        print(func.__name__, ' CPU time: ', time.clock() - start, ' seconds')
        return result
    return warp       

def check_result(func):
    def warp(*args, **kw):
        power = func(*args, **kw)
        if power < 10000:
            raise ValueError('Too weak!')
        else:
            print('Just fine')
        return power
    return warp

@check_info    
def health_index(age, weight, height):
    value = age * height / weight
    print('Age: ', age, ' weight: ', weight, ' height: ',height, 
          ' health index: ', value)
'''
Pay attention to the order of  decorator
Switch last two decorator will cause different result
'''
@check_info
@check_result
@time_cost
def power_index(age, weight, height):
    power = age * height * weight
    print('Age: ', age, ' weight: ', weight, ' height: ',height, 
          ' power index: ', power)
    return power

from datetime import datetime  

import functools

#This decorator will receive a parameter
def display(name = 'Anonymous'):
    def decorator(func):
        @functools.wraps(func)
        def warper(*args, **kw):
            print(name, ' call method: ', func.__name__)
            func(*args, **kw)
            return func
        return warper
    return decorator


def display_compatible(dec = None, name = 'Anonymous'):
    '''
    This decorator could be used as:
        @display_compatible
        @display_compatible()
        @display_compatible(name = 'Andrew')
    But not like this:
        @display_compatible('Andrew')
        Must send a keyword argument
    The principle behind this is:
        If use @display_compatible, the first argument will be the 
        function that pass into decorator.
        If use append callable symbol ()behind @display_compatible,
        the arguments passed into just like normal function
    '''
    if dec and name != 'Anonymous':
        raise
    def decorator(func):
        @functools.wraps(func)
        def warper(*args, **kw):
            print(name, ' call method: ', func.__name__)
            func(*args, **kw)
            return func
        return warper
    if dec:
        print('First argument: ', dec, ' and its name: ', dec.__name__)
        return decorator(dec)
    else:
        print('First argument: ',dec)
        return decorator
        
def compatible_wrap(func):
    '''
    a decorator of decorator, allowing the decorator to be used as:
    @decorator(with, arguments, and=kwargs) or @decorator
    '''
    @functools.wraps(func)
    def new_dec(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # actual decorated function
            return func(args[0])
        else:
            # decorator arguments   
            return lambda realf: func(realf, *args, **kwargs)
            
    return new_dec

@compatible_wrap
def display_flexible(func, name = 'Nobody'):
    @functools.wraps(func)
    def warper(*args, **kw):
        print(name, ' call method: ', func.__name__)
        func(*args, **kw)
        return func
    return warper
       
'''
Optional decorator
@display_compatible
@display_compatible()
@display_compatible(name = 'Jack')
@display_flexible
@display_flexible()
@display_flexible('Tom')
@display_flexible(name = 'Tom')
'''
#@display('Andrew')
@display_flexible('Tom')
def current_time():
    print('Current time: ', datetime.now())
    
def pre_process(signal = 'awake', status = 'unkonw'):
    print('preprocess')    
    
def post_process(signal = 'awake', status = 'unkonw'):
    print('post process')
 
#Decorator with function object parameter
def protector(pre_func, post_func):
    def decorator(func):
        @functools.wraps(func)
        def warper(signal = 'awake', status = 'unkonw'):
            
            pre_result = pre_process(signal, status)
            if pre_result:
                return pre_result
            
            normal_result = func(signal, status)
            if normal_result:
                return normal_result
            
            post_result = post_process(signal, status)
            if post_result:
                return post_result
        return warper
    return decorator
    
@protector(pre_process, post_process)
def normal_process(signal = 'awake', status = 'unkonw'):
    print('Normal process')
    
def decorator_demo():
    now()
    health_index(30, 50, 170)
    '''
    Below cases will cause error
    health_index('20',20,140)
    health_index(20, 70, 500)
    '''
    power_index(30,50,80)
    #Function name has changed
    print('Current func name: ', power_index.__name__)
    '''
    Below cases will cause error
    power_index(20,30,5)
    power_index('20', 20, 50)
    '''
    current_time()
    #Decorator use @functools.warps will keep orignal name
    print('Current func name: ', current_time.__name__)
    
    normal_process()
    
    
def partial_func():
    """This script will show how to define a partial function.
    Partial function conduct from a function we already have, but we want to
    fix some argument or input data.
    """
    #Int is a function that will convert a string to a number.
    #At same time we can pass a key word argument 'base' as base of convertion
    #partial(builtins.object)
    #partial(func, *args, **keywords) - new function with partial application
    #of the given arguments and keywords.
    int2 = functools.partial(int, base = 2)
    res = int2('10010100')
    print('The result convert by int2 is :', res)