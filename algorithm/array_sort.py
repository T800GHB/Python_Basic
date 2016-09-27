# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 20:11:38 2016

@author: andrew

This file will demostrate 8 kinds of algorithm for sorting.
I just want to discribe theory, only support with 1 dimensional array.
"""

import numpy as np



def insert_sort(data):
    '''
    Insert sort, ascending order.
    New one will achvie from higher location.
    Insert new one to the location where biger ones move behind.
    '''
    count = len(data)
    
    for i in range(1, count):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:            
            data[j + 1] = data[j]   #move bigger one to behind            
            j -= 1
        data[j + 1] = key           #just put it down 
    return data
    

def bubble_srot(data):
    '''
    Bubble sort, ascending order.
    Switch location between big one and small one
    '''
    count = len(data)
    
    for i in range(count):
        for j in range(i + 1, count):
            if data[j] < data[i]:
                key = data[i]           #The head of subset will keep smallest one
                data[i] = data[j]
                data[j] = key
    return data

def quick_sort(data):
    pass

def heap_sort(data):
    pass

def merge_sort(data):
    pass

def select_sort(data):
    '''
    Select sort will find smallest one in the rest of array;
    exchange location between smallest one and rest of head.
    '''
    count = len(data)
    for i in range(count):
        min_index = i
        for j in range(i+1, count):
            if data[j] < data[min_index]:
                min_index = j
        #If the smallest has found, take exchange.
        if min_index != i:
            temp = data[i]
            data[i] = data[min_index]
            data[min_index] = temp
    
    return data            
    
def radix_sort(data):
    pass

def shell_sort(data):
    '''
    DL.Shell sort
    
    '''
    count = len(data)
    step = 2                #Factor of decrease group size
    group = np.int(count / step)
    
    while group > 0:
        for i in range(group):
            #Subset is made by index of increment, like this group variable
            j = i + group
            while j < count:
                #First review position
                k = j - group
                key = data[j]
                while k >= 0 and key < data[k]:                    
                    #Switch small one to the head of this subset
                    data[k + group] = data[k]
                    #Review older location  
                    k -= group
                #Insert small one into correct position, all behind are bigger
                data[k + group] = key
                #Jump into newer location 
                j += group
        #Decrease size of group
        group = np.int(group / step)
        
    return data   

def demo_sort():    
    data = np.arange(30)
    np.random.shuffle(data)
    print(data)
    insert_result = insert_sort(data)
    print('Insert result\n',insert_result)
    bubble_result = bubble_srot(data)
    print('Bubble result\n',bubble_result)
    shell_result = shell_sort(data)
    print('Shell result\n',shell_result)
    select_result = select_sort(data)
    print('Select result\n',select_result)