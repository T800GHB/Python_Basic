# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 22:21:42 2016

@author: T800GHB
This file will demostrate how to use regular expression in python.
The detial of usage will not list.
When needed, learn it deeper.
Basis:
^       start
$       end
\d      a nunber
\w      a number or character
*       any longer of string include 0
+       not less one character
?       0 or 1
{n}     n character
{n,m}   n to m character
A|B     A or B can be matched
[]      scope.[0-9a-zA-Z\_] can match one of number , a character , underscore.
()      group

"""
#Python use regular expression with re model.
import re

def run_demo():
    """
    Match function will search between pattern and instance.
    If successfully matched, return a match object, otherwise None
    """
    r = re.match(r'^\d{3}-\d{3,8}$', '024-883215')    
    print('Result of re match function:', r)  
    
    """
    Split string with specific pattern
    """
    s = re.split(r'[\s,\;]+','a,b;;c d')
    print('Result of spliting a string is: ',s)
    
    """
    Use () to form more than one group, the group(0) wiil always be 
    orignal information
    """
    m = re.match(r'^(\d{3})-(\d{3,8}$)','010-254554')
    print('Group 0 :', m.group(0))
    print('Group 1 :', m.group(1))
    print('Group 2 :', m.group(2))
    
    """
    If you don't want to use greedy match, ? can help
    Groups function will return a tuple that contain a sperated group.
    """
    g = re.match(r'^(\d+?)(0*)$','102300').groups()
    print('Result of un-greedy : ', g)
    
    """
    Compile a regular expression when you will use a pattern frequently.
    """
    re_telephone = re.compile(r'^(\d{3})-(\d{3,8})$')
    c = re_telephone.match('022-027492').groups()
    print('Result of compiled pattern matched: ', c)
    
    
    
    
    