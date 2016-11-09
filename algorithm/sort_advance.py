# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 23:03:36 2016

@author: andrew
"""

import numpy as np

def quick_part(data, low, high):
    '''
    Seperate array into two parts with key value
    '''
    i = low
    j = high    
    key = data[i]
    
    while i < j:
        while key <= data[j] and i < j:
            j -= 1            
        data[i] = data[j]
     
        while key >= data[i] and i < j:
            i += 1            
        data[j] = data[i]
      
    data[i] = key
    
    return i

def quick_sort(data):
    '''
    Quick sort without recursion
    '''    
    num = len(data)
    
    stack = []
    stack.append([0, num - 1])
    
    while len(stack) != 0:
        index = stack[-1]
        if index[0] < index[1]:
            stack.pop()
            middle = quick_part(data, index[0], index[1])
            stack.append([index[0], middle - 1])
            stack.append([middle + 1, index[1]])
        else:
            stack.pop()
    
    return data
            
def demo():
    data = np.random.randint(100,size=20)
    print('Before sort\n', data)
    quick_result = quick_sort(data)
    print('Quick sort result\n', quick_result)
    
    