# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 22:23:17 2016

@author: T800GHB

This file will demostrate how to use some function in itertools model.
If you just create a itertools objcet, it will not produce any thing.
Only if you use for loop to make it works.
"""

import itertools

def run_demo_count():
    """
    Unlimited produce a number as fixed interval.
    Need Ctrl + C to end.
    """
    naturals = itertools.count(1)
    for n in naturals:
        print(n)
        
def run_demo_takewile():
    """
    Achive a part of Unlimited sequence.
    You can specify the rule to imply by takewile.
    """
    naturals = itertools.count(1)
    ns = itertools.takewhile(lambda x : x <= 10, naturals)
    print('The section achive from naturals is: ', list(ns), ns)
    
def run_demo_cycle():
    """
    Unlimited produce a same pattern as you specified.
    Need Ctrl + C to end.
    """
    cs = itertools.cycle('ABC')
    for c in cs:
        print(c)
        
def run_demo_repeat():
    """
    Produce a same pattern as you specified, and you can set times of repeation.
    """
    ns = itertools.repeat('ABC',3)
    for s in ns:
        print(s)
        
def run_demo_chain():
    """
    Chain can catenate more than one part to execute iteration procedure.
    """
    for c in itertools.chain('ABC','BCD','CDE'):
        print(c)
        
def run_demo_groupby():
    """
    Groupby function will cluster same neighbour into a list.
    """
    for key, group in itertools.groupby('AAABBBCCCAAA'):
        print(key, list(group))
    
    """
    If you want to specify some rule into group procedure, make lambda expression
    as second parameter of groupby.
    """
    for key, group in itertools.groupby('AAaBBCcCaAa', lambda c : c.upper()):
        print(key, list(group))
        
        
    
    
