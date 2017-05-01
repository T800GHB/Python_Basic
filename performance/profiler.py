#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 21:58:34 2017

@author: andrew
"""

import cProfile
import pstats
import os
import numpy as np

'''
This script will demostrate how to evaluate performance of program.

Profile class ,from cProfile, generate data for analysis, methods include:
    enable(): Start collect performance data for analysis
    disable(): Stop collect performance data for analysis
    create_stats(): Stop collection, and create stats object for collected data
    print_stats(): Create stats object and print collected data out
    dump_stats(filename): Write the performance data into file(binary formate)
    runcall(func, *args, **kwargs): Collect data from stats object of func

Stats class, from pstats, read and operate stats files(binary formate)
Stats could receive stats file and cProfile.Profile object as source of data
    strip_dirs(): Delete all the path of called function from report
    dump_stats(filename): Same utility as cProfile.Profile.dump_stats(filename)
    sort_stats(*keys): Sort the report list.
    reverse_order(): reverse the current report order.
    print_stats(): sent the information to the standard output.
    
Performance evaluation index
ncalls: count of calling
tottime: execute time in this function, does not include time of call others
percall: tottime / ncalls
cumtime: accumulate time, include time of call others

Tools for analysis:
    gprof2dot: https://github.com/jrfonseca/gprof2dot
    gprof2dot -f pstats test_run.prof | dot -Tpng -o test_run.png
    
    vprof: https://github.com/nvdv/vprof
    vprof -c c run.py
    
    RunSnakeRun:
    runsnake test_run.prof
    
    KCacheGrind & pyprof2calltree:
    pyprof2calltree -i test_run.prof -k  # Convert formate and execute KCacheGrind
'''

def do_cprofile(filename):
    """
    Decorator for function profiling.
    """
    def wrapper(func):
        def profiled_func(*args, **kwargs):
            '''
            Flag for do profiling or not.
            This flag will get from environment variables
            Set this flag by:     export PROFILING=y
            '''
            DO_PROF = os.getenv("PROFILING")
            if DO_PROF:
                print('Start collect performance data')
                profile = cProfile.Profile()
                profile.enable()
                result = func(*args, **kwargs)
                profile.disable()
                # Sort stat by internal time.
                sortby = "tottime"
                ps = pstats.Stats(profile).sort_stats(sortby)
                ps.dump_stats(filename)
            else:
                print('Run function as normal')
                result = func(*args, **kwargs)
            return result
        return profiled_func
    return wrapper

@do_cprofile("./test_run.prof")  
def test_func():
    data = np.arange(1000000).reshape(1000,1000)
    sin_data = np.sin(data)
    product = np.dot(sin_data, data)
    return product
    
def demo():
    print('First demo:')
    cProfile.run('np.sin(2**8)')
    print('\nSecond demo:')
    '''
    Set evvironment variable
    '''
    os.environ['PROFILING'] = str('y')
    os.system('echo $PROFILING')
    
    test_func()
    
    p = pstats.Stats('./test_run.prof')
    #List first 10 line and output all 100% with regular expression
    p.strip_dirs().sort_stats('cumtime').print_stats(10,1.0,'.*')