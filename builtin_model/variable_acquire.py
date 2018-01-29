# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 12:45:46 2018

@author: andrew

Usage about build-in method: locals() and globals()
"""

e = 1.0
f = 'bbc'

def demo_locals():
    a = 1
    b = 'ccd'
    for i in range(10):
        j = 0
        k = i
    # All local variable could achive by locals(), return as dict
    locals_dict = locals()
    print('Type locals_dict:\n', type(locals_dict))    
    print('\nContent in locals_dict:\n', locals_dict)
    #print(globals())
    
def demo_globals():
    globals_dict = globals()
    # All global variable in this module could achive by globals(), return as dict
    print('Type globals_dict:\n', type(globals_dict))
    print('\nContent in globals_dict:\n', globals_dict)
    
demo_globals()