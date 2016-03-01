# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 21:29:25 2016

@author: T800GHB
This file will show how to utilize operating system.
There are some many operating system function encapsulate in os model.
There will be some difference about print message in console 
between ipython and natural python.
"""
import os
import time
import random
#multiprocessing model could run on multi platform.
from multiprocessing import Process
#Use pool can create more than one process once.
from multiprocessing import Pool
#Process communication.Pipes is another altertive.
from multiprocessing import Queue

import subprocess

def child_proc(name):
    print('Run child process %s(%s)' %(name, os.getpid()))
    
def long_time_task(name):
    """
    This is also a child process demostration function.
    This function will call sleep to delay a certain of time.
    """
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))
    
# Write data to process
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

# Read data from process
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

def run_demo_fork():
    """
    Use fork to create a new process, the parent will return the child's 
    PID, the later will return 0.
    Fork can only be used on Linux/Unix/Mac
    """
    print('Process %s start' %(os.getpid()))
    pid = os.fork()
    if pid == 0:
        print('Child process %s and the parent process is %s.' 
        %(os.getpid(), os.getppid()))
    else:
        print('Parent process %s create child process %s.'%(os.getpid(), pid))
        
        
def run_demo_multi_proc():
    """
    Use cross platform model 'multiprocess' to create new process.
    Process return a object of process.
    """
    print('Parent process %s.' % os.getpid())
    p = Process(target = child_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
    
def run_demo_pool_proc():
    """
    Use Pool function create many process. Pool return a object of pool.
    The argument of Pool is number of process can be created once.
    You can set this argument accroding to number of core on CPU.
    """
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
    
def run_demo_subproc():
    """
    Run a external process.'
    This block just like run command 'nslookup www.python.org' in prompt.
    But ipython console will not output many information.
    If you want to see complete putput message, please run it on natural
    python console.
    """
    print('$ nslookup www.python.org')
    r = subprocess.call(['nslookup', 'www.python.org'])
    print('Exit code:', r)
    """
    Send some message to subprocess use std.
    """
    print('$ nslookup')
    #Create a subprocess and configuration
    p=subprocess.Popen(['nslookup'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    #Send message to this process.
    output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
    print(output.decode('utf-8'))
    print('Exit code:', p.returncode)
    
def run_demo_proc_com():
    """
    Parent create Queue, and then pass it to all subprocess.    
    """
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # Start subprocess pw，write data into queue.
    pw.start()
    # Start subprocess pr，read data from queue.
    pr.start()
    # Waiting for pw stop.
    pw.join()
    # pr will always，can not stop by itself，so terminate it on force.
    pr.terminate()
    