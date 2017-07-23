from distutils.core import setup, Extension
 
module1 = Extension('math_opt',
                    sources = ['math_opt.cpp'])
 
setup (name = 'Demo math operation',
       version = '1.0',
       description = 'This is a demo package by Andrew',
       ext_modules = [module1])
