#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 00:31:42 2017

@author: andrew
"""

import unittest
class Dict(dict):
    '''
    Define a subclass derive from standard dict.
    Commonly, this part of code is source code, sort at other file.
    I just want to demostrate conveniently.
    '''
    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

class TestDict(unittest.TestCase):
    '''
    Start with 'test' is method for testing.
    Otherwise those method will not execute at test phase
    '''
    def test_init(self):
        d = Dict(a=1, b='test')
        self.assertEqual(d.a, 1)
        self.assertEqual(d.b, 'test')
        self.assertTrue(isinstance(d, dict))

    def test_key(self):
        d = Dict()
        d['key'] = 'value'
        self.assertEqual(d.key, 'value')

    def test_attr(self):
        d = Dict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'], 'value')

    def test_keyerror(self):
        d = Dict()
        with self.assertRaises(KeyError):
            #Test if KeyError will raise in this block of code
            value = d['empty']

    def test_attrerror(self):
        d = Dict()
        with self.assertRaises(AttributeError):
            #Test if AttributeError will raise in this block of code
            value = d.empty
            
    def setUp(self):
        '''
        This method will execute before every test unit.
        So some preparation could be done here
        '''
        print('setUp...')

    def tearDown(self):
        '''
        This method will execute after every test unit.
        So some clean up could be done here
        '''
        print('tearDown...')

def demo():
    '''
    Run unit test by command:
        python -m unittest test_unit.py
    or run all test file in one batch:
        python -m unittest discover
    Statment:
        if __name__ == '__main__':
            unittest.main()
    '''          
    unittest.main()
