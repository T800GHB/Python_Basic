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
    print('Result of multi_return is : %d, %d' %(summation, product))
    abs_var = abs_param_check(y)
    print('Result of abs is : ', abs_var)
    #This kind of usage will cause a type error.
    #abs_var = abs_param_check(str_var)
    print('Result of abs is : ', abs)
    #Input null
    defult_param()  
    #Input first parameter
    defult_param(x)
    #As same before,so the defult parameter  fill the rest of parameter list.
    defult_param(y)
    #Input dual parameter
    defult_param(x,y)
    
    list_var = [1,2,'big',True]
    #Input constant value and variable
    mutable_arguments_list(1,x)
    #All varibales
    mutable_arguments_list(x,y,str_var)
    #Input list as parameter
    mutable_arguments_list(*list_var)
    #If i input only list , without star before list, it will like input only one.
    mutable_arguments_list(list_var)
    #Input key word parameter. The number of argument  is mutable
    keyword_argment_list(city = 'New York', age = 30)
    keyword_argment_list(city = 'New York', age = 28, job = 'Engineer')
    
    dict_var = {'city ':'New York', 'age ':28, 'job' : 'Engineer', 'company' : 'DeepTec'}
    #Take the dict as input
    keyword_argment_list(**dict_var)
    #When we call the named key word argument,  please input the name of argument.
    named_keyword(city = 'Dalian', age = 40)
    #But you can ommit the order of argument
    named_keyword(age = 40, city = 'London')
    #If function offer some defult value, we can directly miss any one
    named_keyword(age = 49)
    
    
    
    

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
    
def defult_param(x = 0, y = 1):
    """This example show how to define function with defult parameter.
    But, the most important rule, do not use empty list as defult value.
    """
    print('Received parameter is : %d, %d.' %(x,y))
    
def mutable_arguments_list(*args):
    """ If the argument's list is mutable, function received tuple acctually.
    """
    print('The content in argment list is :')
    for item in args:
        print(item)
        
def keyword_argment_list(**kw):
    """This function show how to define a key word parameter list.
    Acctually, this function received a dict as input.
    The number of key word parameter is mutable.
    """
    print('The key word parameter is :' ,kw)
    
def named_keyword(*,city = 'shenyang', age):
    """If we want to define a named key word parameter, assign a star with 
    comma before those argument.
    If we ignore the star and comma before argument , those will be normal argument.
    """
    print('The argument is :', city ,'and' , age)
    
    
    
    
    
    

    
    
