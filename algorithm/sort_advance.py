# -*- coding: utf-8 -*-
"""
Created on Wed Nov  9 23:03:36 2016

@author: andrew

This file will demostrate some sort algorithm with advanced skills.
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
    
def adjust_heap_max(data, i, size):
    
    if i < size / 2:
        left = 2 * i + 1
        right = 2 * i + 2 
        
        loc = i
        max_idx = i 
        
        if left < size and data[max_idx] < data[left]:
            max_idx = left
        if right < size and data[max_idx] < data[right]:
            max_idx = right
            
        while max_idx != loc:
            
            data[loc], data[max_idx] = data[max_idx], data[loc]            
            loc = max_idx
                
            left = 2 * loc + 1
            right = 2 * loc + 2
            
            if left < size and data[max_idx] < data[left]:
                max_idx = left
            if right < size and data[max_idx] < data[right]:
                max_idx = right   
                

def adjust_heap_min(data, i, size):   
    
    if i < size / 2:
        min_idx = i
        loc = i
        while True:
            left = 2 * loc + 1
            right = 2 * loc + 2
            
            if left < size and data[min_idx] > data[left]:
                min_idx = left
            if right < size and data[min_idx] > data[right]:
                min_idx = right 
            
            if min_idx != loc:
                data[loc], data[min_idx] = data[min_idx], data[loc]            
                loc = min_idx
            else:
                break


def build_heap_max(data, size):    
    for i in range(int(size / 2))[::-1]:
        adjust_heap_max(data, i, size)

def build_heap_min(data, size):
    for i in range(int(size / 2))[::-1]:
        adjust_heap_min(data, i, size)
    
            
def heap_sort(data):
    '''
    Heap sort without recursion
    '''
    num = len(data)
    build_heap_max(data, num)
    for i in range(num)[::-1]:
        data[0], data[i] = data[i], data[0]
        adjust_heap_max(data, 0, i)
    
    return data
    
def topk(data, k):
    '''
    Find top-k big element
    '''
    num = len(data)
    top = data[:k]
    build_heap_min(top, k)
    
    for i in range(k, num):
        if top[0] < data[i]:
            top[0] = data[i]
            
            adjust_heap_min(top, 0, k)
            
    return top

            
def demo():
    data = np.random.randint(100,size=20)
    print('Before sort\n', data)
    quick_result = quick_sort(data)
    print('Quick sort result\n', quick_result)
    heap_result = heap_sort(data)
    print('Heap sort result\n', heap_result)
    top_result = topk(data, 5)
    print('Top result\n', top_result)