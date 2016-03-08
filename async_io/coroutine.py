# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 21:14:58 2016

@author: T800GHB

This file will demostrate how the coroutine works.
Coroutine could switch between two sub-program very efficiently.
"""


def consumer():
    """
    This function is a procedure in generator.
    """
    r = ''
    while True:
        """
        Start yield next time , run a loop , then return.
        yield could receive parameter then pass to n.
        Run a loop then return r, r is a fixed value, 
        so you could observe produce receive same return-value.
        
        """
        n = yield r
        if not n:
            return
        print('[Consumer] Consuming %s...'%n)
        r = '200OK'
        
def produce(c):
    """
    Send function could transmit parameter to generator.
    Send none to start generator.
    """
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[Producer] Producing %s...'%n)
        r = c.send(n)
        print('[Producer] Consumer return %s...' %r)
    #Close generator
    c.close()
    
    
def run_demo():
    #Create a generator
    c = consumer()
    #Use generator to implement coroutine.
    produce(c)	