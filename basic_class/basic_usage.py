# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 22:59:29 2016

@author: T800GHB

This file will demostrate how to define a class and add attribute and method
"""

class student(object):
    #Define a construction function
    #self must assign to first argument,it's like 'this' in C++
    #Variable start with two underscore will be treated as private member.
    def __init__(self, name, ID):
        self.__name = name
        self.__ID = ID
    def display_info(self):
        print('The student: %s, ID num : %s' %(self.__name, self.__ID))

    
    #Define get and set method
    def get_name(self):
        return self.__name
    def get_ID(self):
        return self.__ID
    def set_name(self,name):
        self.__name = name
    def set_ID(self, ID):
        self.__ID = ID
        
    
class science_student(student):
    def __init__(self, name, ID, skill):
        self.__name = name
        self.__ID = ID
        self.__skill = skill
    
    def get_skill(self):
        return self.__skill
    def set_skill(self, skill):
        self.__skill = skill
        
def try_class():
    stu = student('Jack', 955)
    #Add a attribute dynamically
    stu.city = 'Beijing'
    stu.display_info()
    print('This student come from: ', stu.city)
    
    stu_s = science_student('Tom', 900, 'computer')

    
        
    
        
