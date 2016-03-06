# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 19:36:12 2016

@author: T800GHB

This file will demostrate how to use built-in model --- collections.
"""

from collections import namedtuple
from collections import deque
from collections import defaultdict
from collections import OrderedDict
from collections import Counter

def run_demo():
    """
    namedtuple will create a tuple that can be index by attribute.
    The property of namedtuple same like tuple(value can't be changed).
    """
    Point = namedtuple('Point',['x','y'])
    p = Point(4,8)
    print('The coordinate is %d, %d.' %(p.x, p.y))
    Circle = namedtuple('Circle',['x','y','r'])
    c = Circle(3,9,4)
    print('The parameter of circle is : %d, %d, %d.'%(c.x, c.y, c.r))
    
    """
    Deque could execute delete and insert operation very efficiently.
    It also can be indexed by location.
    """
    q = deque(['a', 'b', 'c'])
    q.append('x')
    q.appendleft('y')
    print('Content in deque: ', q)
    print('Third element in q is: ', q[3] )
    
    """
    Defaultdict can set notification when index a key that does not exist in dict.
    Other property between defaultdict and dict will keep same.
    """
    dd = defaultdict(lambda:'Not exist')
    dd['key1'] = 'abc'
    print('Value of key1 and key2 is: %s, %s' %(dd['key1'], dd['key2']))

    """
    OrderedDict will keep order of key as input sequence.
    Keys in normal dict is disorder.
    When we iterate the normal dict, order is unknown.
    """
    od = OrderedDict()
    od['z'] = 1
    od['x'] = 2
    od['y'] = 3
    print('The key in orderdict is: ', list(od.keys()))
    del od['x']
    print('The key in deleted orderdict is: ', list(od.keys()))
    
    """
    Counter is a subclass of dict.
    It will do basic statistics.
    """
    c = Counter()
    for ch in 'Engineering':
        c[ch] = c[ch] + 1
    print('The statistics result is :', c)
    