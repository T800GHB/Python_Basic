# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 10:28:10 2018

@author: andrew

tqdm is very easy to use as process bar
It will not impact efficiency
"""

from time import sleep
from tqdm import tqdm

def demo_tqdm():
    for i in tqdm(range(1000)):
        sleep(0.01)
