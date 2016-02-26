# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 20:34:12 2016

@author: T800GHB

This file will show how to use some senior property about class
"""

from types import MethodType

class student(object):
    pass

class person(object):
    """
    If you define a special variable '__slots__ in class,
    the element in tuple is the attribute that can be used.
    otherwise, you can bind another attribute on object.
    We can add attribute by add a method on class or object,
    but the method name must in __slots__.
    """
    __slots__ = ('name','age', 'set_skill')
    
class man(person):
    pass

def set_skill(self,skill):
    self.skill = skill

def set_age(self, age):
    self.age = age

def run_demo():    
    s = student()
    s.name = "Tom"                      #Bind a attribute dynamically.
    s.set_age = MethodType(set_age, s)  #Bind a method dynamically.
    s.set_age(20)
    print('Name and age of student is %s, %d' %(s.name, s.age))
    """
    If you want to use name and set_age on other object, it will not
    work. 
    If you want bind a method on class type , then all object which 
    belong to this class can use it.
    """
    student.set_skill = MethodType(set_skill, student)
    s_o = student()
    s_o.set_skill('dancing')
    print('The age of student is :', s_o.skill)    
    p = person()
    p.name = 'Jack'
    p.age = 20
    #This will arise an error
    #p.skill = 'computer'
    person.set_skill = MethodType(set_skill, person)
    p.set_skill('singing')
    print('Name and age of person is %s, %d' %(p.name, p.age))
    print('What this person can do is :', p.skill)
    #slot variable will not work on the subclass
    m = man()
    m.skill = 'computer'
    print('The skill of man is :', m.skill)
