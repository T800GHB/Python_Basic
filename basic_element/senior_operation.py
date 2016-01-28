# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 22:40:31 2016

@author: T800GHB
This file contain some high-level feature about python
"""

def slice_index():
    """This file show how a list can be indexed by slice feature.
    We can use all feature below on tuple to acquire element.
    Pay attention to the point that content of tuple can not be changed.
    """
    num = [1,2,3,4,5,6,7,8,9,0]
    """If we want to acquire three element at the head of list, 
    use a colon between the range.
    """
    head = num[0:3]
    print('First three element is : ', head)
    #If the beginning index is 0, you can ommit left range index
    head = num[:5]
    print('First five element is :',head)
    #If you want to acquire item from rear, offer a negative value.
    #Please take care of order is left to right, reverse this order will get nothing
    #For example, num[-1, -4], return a null list.
    last_element = num[-4 : -1]
    print('The rear item is :', last_element)
    #List indices must be integers or slices, not tuple or different flag.
    #Bad example is last_elemnt = num[-1, 1]
    
    #If we want to acquire element by simplific interval.
    sparse_acquire = num[0:8:3]
    print('Acquire item every three element: ', sparse_acquire)
    #If we ommit both left and right index, this means use what all we have.
    sparse_acquire = num[::3]
    print('Acquire item every three element in full range: ', sparse_acquire)
    
   
    
    
    
    
    
