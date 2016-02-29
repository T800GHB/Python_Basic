# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 21:20:30 2016

@author: T800GHB
This file will show how to serialize some file to disk.
"""
import pickle
import json

class Student(object):
    """
    This class will demostrate how to serialize any kind of class
    """
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score
        
def student2dict(var):
    return{
    'name':var.name,
    'age':var.age,
    'score':var.score
    }

def dict2student(d):
    return Student(d['name'], d['age'], d['score'])
    
def run_demo():
    """
    Serialize a object to disk, then reload it.
    The object will be serialzied to a binary string.
    But the pickle object can not pass between different language.
    If the version of python different, it may not work.
    """
    dw = dict(name = 'Jack', age = 28, job = 'engineer')
    """
    Write a dictionary object to disk as binary format.
    dumps will return a bytes. You can also stroe a bytes returned by dumps
    """
    with open('./test.txt', 'wb') as fw:
        pickle.dump(dw, fw)
    """        
    Load a binary file from disk
    You can also open the file sotre those bytes first, then un-serialize its
    content by loads().
    """
    with open('./test.txt', 'rb') as fr:
        dr = pickle.load(fr)
        
    print(dr)
    
    dsw = dict(name = 'Tom', age = 40, job = 'fireman')
    """
    Serialize a object with json, then reload it.
    json will serialize object to a string, so you should operate the file
    to read and wite with 'r' and 'w' model.
    As same before, you can use dumps and loads.
    """
    with open('./json_test.txt', 'w') as fsw:
        json.dump(dsw, fsw)
        
    with open('./json_test.txt', 'r') as fsr:
        dsr = json.load(fsr)
        
    print(dsr)
    
    """
    Serialize a arbitrary type to json format.
    File operation just like same before, not repeat any more.
    """
    s = Student('Andrew', 18, 100)
    #Use specific function to deal with type convert
    print(json.dumps(s, default=student2dict))
    #Use built-in attribute to deal with type convert
    sj = json.dumps(s, default=lambda obj: obj.__dict__)
    #Un-serialize it to object with specific function to complete type convertion.
    print(json.loads(sj, object_hook=dict2student))
        
    
    
    
    
    
