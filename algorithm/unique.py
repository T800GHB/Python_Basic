# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 22:29:31 2016

@author: andrew

This file record two kinds of method which could complete unique operation on array.
"""

def unique_ordered(a):
    '''
    Reserve unique elements onto orignal array, at same time, 
    this operation will keep the order they had.
    '''
    '''
    Label repeat element.
    In this demostration, 0 will be treated as label of same element.
    In searching procedure, repeated element will be set to 0.
    If you want to consider 0 as a normal, you could select another label.
    '''
    cur = 1
    for i in range(1,len(a)):
        for j in range(cur):
            if a[j] != 0:
                if a[i] == a[j]:
                    a[i] = 0
        cur += 1
    
    '''
    Delete null element and push unique element to the head of array.
    '''
    head = 0;                   #Point to the location of receiving.
    search = 0;                 #Point to the location of achiving.
    while search < len(a):
        if a[search] != 0:
            if search == head:
                '''Have not find unique element'''
                search += 1
                head += 1
            else:
                '''Push element to the head of array'''
                a[head] = a[search]
                head += 1
                search += 1
        else:
            '''Searching element wait for copying'''
            search += 1
    '''Now, head means total number of unique element'''
    
    print('Number of element of is: ', head)
    '''Delete empty element'''
    a[head : len(a)] = []
    print(a)
    
def unique_chaos(a):
    '''
    Reserve unique elements onto orignal array, 
    but this kind of method could guarantee order.
    This way is more efficient, because less copy.
    '''
    '''Situation is same as above one'''
    cur = 1
    for i in range(1,len(a)):
        for j in range(cur):
            if a[j] != 0:
                if a[i] == a[j]:
                    a[i] = 0
        cur += 1
    '''Copy element from rear to empty location'''
    head = 0;
    rear = len(a) - 1
    while head < rear:
        '''Head pointer find empty location'''
        if a[head] == 0:
            '''Rear index point to an empty location'''
            if a[rear] == 0:
                '''Find un-empty location at rear'''
                while a[rear] == 0:
                    rear -= 1
                if head < rear:
                    '''No conflict between head and rear, copy from rear'''
                    a[head] = a[rear]
                    rear -= 1
                    head += 1
                else:
                    '''Conflicted, quit directly'''
                    head = rear
            else:
                '''Rear is not empty'''
                a[head] = a[rear]
                rear -= 1
                head += 1                
        else:
            '''Head pointer has not find empty location, keep searching'''
            head += 1
    count = head + 1
    print('Number of element of is: ', count)
    '''Delete empty element'''
    a[count : len(a)] = []
    print(a)
    
def demo():
    '''Test set'''
    a = [1,1,2,2,1,3,4,4,3,3,5,1,2,4,6,3]       #Normal
    b = [1,2,3,4]                               #All different
    c = [1,1,1,1]                               #All same
    d = [7] 
    a1 = a.copy()
    b1 = b.copy()
    c1 = c.copy()
    d1 = d.copy()                                    #Only one
    print('Orignal data')
    print(a)
    print(b)
    print(c)
    print(d)
    print('unique_ordered')
    unique_ordered(a)
    unique_ordered(b)
    unique_ordered(c)
    unique_ordered(d)                              
    print('unique_chaos')
    unique_chaos(a1)
    unique_chaos(b1)
    unique_chaos(c1)
    unique_chaos(d1)
                
    
            
    
    
