# -*- coding: utf-8 -*-
"""
Created on Thu Dec 31 14:40:26 2015

@author: T800GHB

This file introduce basic element tpye and operation about it.
At same time, some example show how use conditional desicion and loop operation.
"""
from collections import defaultdict

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
    names = ['Nick', 'Andrew', 'Tom', 'Freeman', 'Bush']
    for item in names:
        print(item)
    
    capacity = len(names)
    index = 0
    while index < capacity :
        print(names[index])
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
    
    #Loop with index
    for i, name in enumerate(names):
        print(i, '-->',name)
    
def Basic_dict():
    score_dict = {'Mike':95, 'Tom':80, 'Jack':60}
    print(score_dict)
    #If key not in dict, create a new item and assign its value
    score_dict['Nick'] = 100
    print(score_dict)
    #To judge if a key in this dict
    print('Forest' in score_dict)
    #Achive the element of dict by 'get'. 'Tom' is a item of dict
    print(score_dict.get('Tom'))
    #Use 'get' method to return a value that a item is not in this dict
    print(score_dict.get('Forest', 3000))
    #Delete a item and return its value
    print(score_dict.pop('Mike'))\
    #Methods : 'keys', 'items', 'values' will return a iterable view
    print(score_dict.keys())
    print(score_dict.items())
    print(score_dict.values())
    #Create a dict from list and set its default value
    name = ['Andrew', 'Tomas', 'Forest']
    pair = dict.fromkeys(name , 100)
    print(pair)
    #Create a dict with default for every new key
    party = defaultdict(lambda: 200)
    party['Pony']
    party['Frank'] += 20    
    #Merge dict 'pair' and 'score_dict', result will store in 'pair'
    pair.update(score_dict)
    print(pair)    
    #More efficient method to merge 'kid', 'pair', 'party', return new dict
    kid = {'Coco': 30}
    group = {**kid, **pair, **party}
    print('Merged result:\n', group)
    #Remove all the items of dict
    score_dict.clear()
    print(score_dict)
    #Initialize key and value in dict by 'setdefault'
    #If key in dict, do nothing, otherwise add key and set its value
    group.setdefault('Coco', 20)
    group.setdefault('List', []).append('list_item')
    print(group)
    
def Basic_set():
    type  = set(['car', 'truck', 'ambulance'])
    name = set(['car', 'truck', 'digger'])
    print(type)
    type.add('bus')
    print(type)
    type.remove('truck')
    print(type & name)
    print(type | name)
    
def Basic_assign():
    '''
    Switch value of variable 'a' and 'b', 
    old usage will utilize a tmp variable, just like :
        tmp = a
        a = b
        b = tmp
    But more pythonic usage could do it directly
    '''
    a = 3
    b = 5
    print('Value a: ',a ,' , value b: ', b)
    a,b = b,a
    print('Value a: ',a ,' , value b: ', b)
    
    '''
    Sequencely unpack a tuple or list.
    'info' is a tuple
    '''
    info = 'vttalk', 'female', 28, 'happy@qq.com'
    name, gender, age, email = info
    print(name, gender, age, email)

def Basic_string():
    '''
    Basic usage of string
    '''
    #String concate, use '+' symbol or 'join' method
    names = ['raymond', 'rachel', 'matthew', 'roger',
         'betty', 'melissa', 'judith', 'charlie']   

    s = names[0]
    for name in names[1:]:
        s += ', ' + name
    print (s)
    #More efficient way, less memory, '.' as seperator
    print(','.join(names))


    