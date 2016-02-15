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
        #Pay attention to this constructor usage in subclass
        student.__init__(self, name,ID)
        self.__skill = skill
    
    def get_skill(self):
        return self.__skill
    def set_skill(self, skill):
        self.__skill = skill
        
class art_student(student):
    pass
        
def try_class():
    stu = student('Jack', 955)
    #Add a attribute dynamically
    stu.city = 'Beijing'
    stu.display_info()
    print('This student come from: ', stu.city)
    #Initialize new object of science_student
    stu_s = science_student('Tom', 900, 'computer')
    print("Science student's name is :", stu_s.get_name())
    #Show the type of stu_s
    print('The type of stu_s is :', type(stu_s))
    #If this object is a instance of one kind of class
    print('stu_s is a instance of student:', isinstance(stu_s, student))
    #List all method and attribute of this class
    print('All method and attribute in stu is :', dir(stu_s))
    stu_a = art_student('Mike',990)
    print('All method and attribute in art student object is :',dir(stu_a))
    print('All method and attribute in art student class is :',dir(art_student))
    print(stu_a.get_name())
    

    
        
    
        
