# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 20:11:38 2016

@author: andrew

This file will demostrate 8 kinds of algorithm for sorting.
I just want to discribe theory, only support with 1 dimensional array.
"""

import numpy as np
import math


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

def quick_sort(data, low, high):
    '''
    Quick Sort is a fast and basic algorithm.
    This algorithm will always seperate array into two parts ,
    according to key value.
    If the array can't seperate any more, all procedure done.
    '''
    #Stop condition    
    if high <= low:
        return
    i = low
    j = high
    #There are many methods to set key, here is samplest one.
    key = data[low]
    '''    
    Seperate array into two parts, left part are less than key, right part are
    great than key.
    '''
    while i < j:
        while i < j and key <= data[j]:
            j -= 1         
        data[i] = data[j]   #Switch location between key and less one     
        while i < j and data[i] <= key:
            i += 1
        data[j] = data[i]   #Switch location between key and great one
    
    data[i] = key       #Put the key to centeral position.
 
    quick_sort(data, low, i-1)
    quick_sort(data, i+1, high)    
    
    return data

def adjust_heap(data, i, size):    
    #The location of i is father, so the children of i is below.    
    lchild = 2 * i + 1
    rchild = 2 * i + 2
    '''
    Assume the location i is max value among father and its children.
    So, if the max value is not father, switch i and max location.
    Always keep location of father max vaule in its subset. 
    '''
    max = i
    #Keep location i in correct range, and find max value
    if i < size / 2:
        if lchild < size and data[lchild] > data[max]:
            max = lchild

        if rchild < size and data[rchild] > data[max]:
            max = rchild

        if max != i:
            data[max], data[i] = data[i], data[max]
            #Struct has changed, adjust struct of father's children
            adjust_heap(data, max, size)
    
def build_heap(data, size):
    '''    
    Adjust order of array from leaf to root, then the root is maximun of array.
    From size / 2 + 1 to end are leaves.
    So, pay attention to the reverse order.
    '''
    for i in range(0, int(size/2))[::-1]:
        adjust_heap(data, i, size)
    
def heap_sort(data):
    
    size = len(data)
    build_heap(data, size)
    '''
    Output the ascent array.
    Pay attention to reverse order, put the maximum at last location,
    then adjust struct of rest part.
    '''
    for i in range(0, size)[::-1]:
        data[0], data[i] = data[i], data[0]
        adjust_heap(data, 0, i)
    
    return data

def merge(left, right):
    #Index
    i = 0
    j = 0
    #Temperory container
    result = []       
    #According to the order, descent or ascent, one by one merger.     
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    #Append rest part of array onto result.
    result += list(left[i:])
    result += list(right[j:])
    return result            
    
def merge_sort(data):
    '''
    The idea of Merge sort is  divide and conquer.
    Split array into smallest one, 1 element, and merge those parts.
    '''
    #Stop condition
    if len(data) <= 1:
        return data
    #Split into two parts and recursion 
    middle = int(len(data) / 2)    
    left = merge_sort(data[0:middle])
    right = merge_sort(data[middle: len(data)])
    #Result is a list, not a numpy array.
    return merge(left,right)    

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
    
def radix_sort(data, radix = 10):
    '''
    This method will sort array without comparsion.
    Just like hash, sort by empty and ordered array.
    Put choas elements into container, according to the 
    current radix(radix of decimal is 10)
    From low radix to high radix.
    But, this algorithm just support integer
    '''
    #Calculate max radix of this choas array.
    k = int(math.ceil(math.log(max(data), radix)))
    #According to the basic radix, allocate buckets(container).
    bucket = [[] for i in range(radix)]   
    
    #From low radix to high radix, assign to each bucket.
    for i in range(1, k+1):
        #Calculate the value of specific radix, put the elements into buckets.
        for j in data:            
            bucket[int(j/(radix**(i-1)) % (radix**i))].append(j)
        #Clear the orignal data   
        del data[:]
        #Receive the ordered elements with specific radix
        for z in bucket:
            #Now, data is ordered with specific radix            
            data += z
            #Clear bucket for reuse.
            del z[:]

    return data

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

def counting_sort(data):
    '''
    This is a kind of bucket sort. 
    Put the choas elements into ordered array.
    The procedure of counting consider the repeat elements.
    This method will cost so much memory, so it will get best preformence 
    for sorting integer from 0 to 100.
    '''
    d_size = len(data)
    #This is a ordered array
    counter = np.zeros(d_size, dtype = np.int)
    result = np.zeros(d_size, dtype = np.int)
    #Counting the frequency of each element.
    for i in range(d_size):
        counter[data[i]] += 1
    #Calculate the index of different element
    for i in range(1, d_size):
        counter[i] += counter[i - 1]
    #Forward or backward could work.
    #for i in range(d_size-1, -1, -1):
    for i in range(d_size):
        element = data[i]  
        #Get the index, this location is the lastest of all can save this value.    
        index = counter[element] - 1     
        result[index] = element
        '''
        Adjust the index of this value, 
        capacity in result array of this value will reduce.
        '''
        counter[element] -= 1
    
    return result

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
    quick_result = quick_sort(data, 0, len(data) - 1)
    print('Quick result\n',quick_result)
    radix_result = radix_sort(list(data))
    print('Radix result\n',np.array(radix_result))
    count_result = counting_sort(data)
    print('Counting result\n', count_result)
    merge_result = np.array(merge_sort(data))
    print('Merge result\n',merge_result)       
    heap_result = heap_sort(data)
    print('Heap result\n', heap_result)