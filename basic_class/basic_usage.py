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
        print('Student initialization done')
        
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
        '''
        Pay attention to this constructor usage in subclass
        Do not mix with super()
        '''
        student.__init__(self, name,ID)
        print('Science student initialization start')
        self.__skill = skill
        print('Science student initialization done')
    
    def get_skill(self):
        return self.__skill
    def set_skill(self, skill):
        self.__skill = skill
    
    def display_info(self):
        #Call method of father. This usage allow in python3
        super().display_info()
        print('Skill of science student: ', self.__skill)
        
class art_student(student):
    def __init__(self, name, ID, level):
        #Super inheritance.Call constructor of father
        super(art_student, self).__init__(name, ID)
        self.__level = level
        print('Art student initialization done')
    
    def display_info(self):
        #Call method of father. This usage is compatible with python2
        super(art_student, self).display_info()
        print('Art of level is: ', self.__level)

class sport_student(student):
    def __init__(self, name, ID, event, level):
        #Call __init__ in father. This usage allow in python3
        super().__init__(name, ID, level)
        self.__event = event
    
    def display_info(self):
        super().display_info()
        print('Event of sport student: ', self.__event)
        
class super_student(sport_student, art_student):
    def __init__(self, name, ID, event, level, age):
        '''
        Initialization of multiple inheritance are so complicated.
        Sport student has attribute : name , ID , event
        For this initialization, you need to modify father of this class.
        Add attribute level to __init__ of class sport student
        The order in MRO is order of inheritance list.
        '''
        super().__init__(name, ID, event, level)
        self.__age = age
        
    def display_info(self):
        super().display_info()
        print('Age of super student: ', self.__age)
    
        
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
    stu_s.display_info()
    
    stu_a = art_student('Mike',990,3)
    print('All method and attribute in art student object is :',dir(stu_a))
    print('All method and attribute in art student class is :',dir(art_student))
    print(stu_a.get_name())
    stu_a.display_info()
    
    stu_sport = sport_student('Andrew', 245, 'Judo')
    stu_sport.display_info()
    
class Base(object):

    def __init__(self):
        print ("enter Base")
        print ("leave Base")
        
class A(Base):

    def __init__(self):
        print ("enter A")
        super(A, self).__init__()
        print ("leave A") 

class B(Base):

    def __init__(self):
        print ("enter B")
        super(B, self).__init__()
        print ("leave B")

class C(A, B):

    def __init__(self):
        print ("enter C")
        super(C, self).__init__()
        print ("leave C")
        
def super_analysis():
    '''
    This function will demostrate working process in detail about super() 
    and effect of MRO(Method Resolution Order) for multiple inheritance.
    '''    
    c = C()
    #mro() will return a list of resolution order
    print('Resolution Order: ')
    for item in C.mro():
        print(item)
        
    stu_super = super_student(
        name = 'William', ID = 100, age = 20, event = 'Run', level = 5)
    stu_super.display_info()
