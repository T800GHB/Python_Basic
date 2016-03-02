# -*- coding: utf-8 -*-
"""
Created on Wed Mar  2 20:57:42 2016

@author: T800GHB
This file will show how to use multithread complete task.
Python use GIL as thread lock, so it will always utilize one of CPU core.
If you want to utilize CPU's multi-core with python, multi-process can do it.
"""
import time
import threading
#Global varibale, you can access this one in all scope of file.
balance = 0
#Create thread lock
lock = threading.Lock()

def change_it(n):
    """
    Declare the variable is global, then use it, or it will be treated
    as local variable
    """
    global balance
    balance = balance + n
    balance = balance - n
    
def run_thread(n):
    for i in range(100000):
        # First, acquire lock
        lock.acquire()
        try:
            # Do something what you want.
            change_it(n)
        finally:
            #Release lock, or resource
            lock.release()

def loop():
    """
    This function will pass to thread.
    """
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

def run_demo():
    print('thread %s is running...' % threading.current_thread().name)
    """
    Create a thread object with function will be executed and name.
    """
    t = threading.Thread(target=loop, name='LoopThread')
    t.start()
    t.join()
    print('thread %s ended.' % threading.current_thread().name)
    
def run_demo_lock():
    """
    Create two thread and execute them at same time.
    """
    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)
