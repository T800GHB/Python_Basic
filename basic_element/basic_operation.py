# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 14:40:26 2015

@author: T800GHB

This file introduce basic element tpye and operation about it.
At same time, some example show how use conditional desicion and loop operation.
"""

def Basic_Print():
    a = 1
    b = 2
    c = 2.36
    print(a,b,c)
    #print formating
    print('Format print %d, %d, %s' %(a,b,c))
    str_1 = 'This is a '
    str_2 = 'small test!'
    #print a string from which two strings cat
    print('This is string concat', str_1 + str_2)
    #type convertion
    str_3 = str(a)
    print('Format convert from int to str'
    ,str_3,str(c))
    #print a type of variable
    print('Type print a is ',type(a),'c is ',type(c))
    l = [1,2,3,4,5,6,7,8]
    #list inference
    [print(i) for i in l]
    print('The above is list inference')
    
def Basic_list():
    name = ['Andrew', 'Jack', 'Tom']
    print('This is list of name')
    [print( i) for i in name]
    print('The length of this list is ', len(name))
    print('This last item of list is ', name[-1])
    name.append('Freeman')
    print('Add a item on rear ' ,name[-1])
    name.insert(1, 'Adam')
    print('Insert a item at second index', name)
    print('Pop the last item', name.pop())
    name.pop(1)
    print('Pop the second item', name)
    name[1] = 'Nick'
    print('Replace second item', name)
    mix = ['string', 89, True, [1,2]]
    print('This is a mix list', mix)
    print('The length of mix is ', len(mix))
    
def Basic_tuple():
    name = ('Andrew', 'Jack', 'Nick')
    print('This is a tuple', name)
    alone = ('Tom',)
    print('This is a tuple contain only one item', alone)
    name_list = list(name)
    print('This is list convert from tuple', name_list)
    
def Basic_judge():
    length = int(input('Please enter the length of running: '))
    gender = input('Please enter your gender: ')
    if length < 500 and gender == 'M':
        print('You are so weak')
    elif length > 500 and gender == 'M':
        print('You are so strong')
    else:
        print("I don't know!")
        
def Basic_loop():
    name = ['Nick', 'Andrew', 'Tom', 'Freeman', 'Bush']
    for item in name:
        print(item)
    
    capacity = len(name)
    index = 0
    while index < capacity :
        print(name[index])
        index = index + 1
        
    sum = 0
    for item in [1,2,3,4,5,6,7,8,9,10]:
        sum += item
    print(sum)
    
    sum = 0
    sequence = list(range(30))
    for item in sequence:
        sum += item
    print(sum)
    
def Basic_dict():
    score_dict = {'Mike':95, 'Tom':80, 'Jack':60}
    print(score_dict)
    score_dict['Nick'] = 100
    print(score_dict)
    'Forest' in score_dict
    print(score_dict.get('Tom'))
    print(score_dict.get('Forest', 3000))
    print(score_dict.pop('Mike'))
    print(score_dict.keys())
    print(score_dict.items())
    print(score_dict.values())
    name = ['Andrew', 'Tomas', 'Forest']
    score = [90, 90, 100]
    pair = dict.fromkeys(name, 100)
    print(pair)
    pair.update(score_dict)
    print(pair)     
    score_dict.clear()
    print(score_dict)
    index = {1:'Mike', 2:'Nick', 3:'Tom',90: 'Matt'}
    print(index)
    
    
    
    
def Basic_set():
    type  = set(['car', 'truck', 'ambulance'])
    name = set(['car', 'truck', 'digger'])
    print(type)
    type.add('bus')
    print(type)
    type.remove('truck')
    print(type & name)
    print(type | name)
    
        
    
     
    
