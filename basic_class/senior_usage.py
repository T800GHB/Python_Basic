# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 20:34:12 2016

@author: T800GHB

This file will show how to use some senior property about class
"""

from types import MethodType

from enum import Enum, unique

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

class car(object):
    def __init__(self, brandmark, s = 0.0, w_load = 0.0):
        self.__brandmark = brandmark  
        self.__speed = s
        self.__w_load = w_load
        
    #Class customization.If object reference an attribute that does not exist
    #__getattr__ will call automatically.
    def __getattr__(self, attr):        
        if attr == 'horsepower':
            return 1000
        raise AttributeError("Car object has no attribute %s" %attr)    
    """
    Define a decorator on an attribute
    """
    @property
    def speed(self):
        return self.__speed
    @speed.setter
    def speed(self, speed):
        if not isinstance(speed, float):
            raise ValueError('Speed must be a float point.')
        if speed < 0 or speed > 500:
            raise ValueError('Speed is not on correct range')
        self.__speed = speed
    #This attribute can only be read
    @property
    def brandmark(self):
        return self.__brandmark
    
    #This method could call by class name or its instantiated object
    #First argument is class name, like self in instance method as first default arguments
    #Scenario fit for creating instance as factory method
    @classmethod
    def weight_load_car(cls, ex_weight):
        print('Class name: ', cls, ' , extra weight: ', ex_weight)
        #Something magic information
        brand = 'Chevrolet'
        speed = 100
        weight = 1500
        return cls(brand, speed, weight + ex_weight)
    #This method colud call by class name or its instantiated object
    #Its dose not need fixed first argument
    #Scenario firt for working without any variable or method contained in this class
    #There is no big difference with normal method in current module, only service for this class
    @staticmethod
    def welcome(cumstomer):
        print('Welcome ', cumstomer, ' use our car')
"""
This is a enum class, @unique decorator will make sure there is no repeated
element.
"""
@unique
class Weekday(Enum):
    Sun = 0 # Set Sun's value to be 0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6
        


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
    
    c = car('Benz')
    #This will raise an error
    #c.speed = 400
    #This will work free
    c.speed = 300.0
    print('Car speed is :', c.speed)
    print('The brandmark of car is :', c.brandmark)
    #Brandmark can only be read, so you can not set it.
    #c.brandmark = 'BMW'
    #This will call __getattr__, horsepower does not a attribute belong to car.
    print('The horsepower of car is :', c.horsepower)
    #This will also call __getattr__, but it will raise an error.
    #print('The type of car is :', c.type)
    big_car = car.weight_load_car(100)
    #Same as above, because c is object of car
    c.weight_load(100)
    car.welcome('andrew')
    c.welcome('andrew')
    #Define a object that is enum element
    day = Weekday.Mon
    print('Enum element :',day)
    print('Enum element value:', day.value)
    print('Object and Enum element :', day == Weekday.Mon)
    print('Enum element index as name', Weekday['Tue'])
    print('Enum element value index as name', Weekday['Tue'].value)
