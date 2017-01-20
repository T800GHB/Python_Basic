#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 22:03:59 2017

@author: andrew
"""

from setuptools import setup
from setuptools import find_packages

setup(
      #Project name
      name = 'app_demo',
      #Project version
      version = '1.0',
      #Wheather to install as a zip package or 
      #a normal directory(name postfix is egg).
      #keep False will be a good choice.
      zip_safe = False,
      #Automatically find packages in current directory
      packages = find_packages(),# packages = ['app_demo'],
      #Whether to include non-python files list in MANIFEST.in
      include_package_data = True,
      #Where to find and list of files to exclude
      exclude_package_date={'':['.gitignore']},
      #Automaticlly find dependencies and install from PyPI
      install_requires=[
        'Numpy>=0.10',
        'Scipy>=0.10'
        ],
      #URLs where to find dependencies
      dependency_links=[
        'http://example.com/dependency.tar.gz'
        ],  
        
      author = 'Andrew Green',
      
      author_email = 't800ghb@qq.com',
      
      description = "This is a sample package",
      
      license = "BSD",
      
      keywords = "hello world example",
      #Project web page
      url = "http://example.com/HelloWorld/", 
      #Get documents comments from code
      long_description=__doc__,   # 从代码中获取文档注释
      )