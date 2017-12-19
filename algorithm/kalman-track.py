# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 16:06:03 2017

@author: hbguo

This file demostrate a sample kalman filter for tracking signal.
There is no input signal for changing system status.
So, system will always keep as before, only consider the measured signal.
I want to observe whole process, some intermediate keep into array.
Follow the 5 key formula.
"""

import numpy as np
import pylab as pl

num_signal = 200                    #number of data
w = np.random.randn(num_signal)     #system noise

v = np.random.randn(num_signal)     #measurement noise
sequence = np.arange(num_signal)    


x = np.zeros((num_signal,))
a = 1

for k in range(1,num_signal):
    x[k] = a * x[k-1] + w[k-1]
    
h = 1                               #parameter for measurement system
z = x + v                           #measurement value

Q = 0.001                           #system process activation noise covariance
R = 0.1                             #measurement noise covariance
     
     
p = 10                              #Posterior estimate covariance

output = np.zeros((num_signal,))

for t in range(1,num_signal):
    p_past = a**2 * p + Q
    kg = h * p_past / (h** 2 * p_past + R)
    output[t] = a * output[t-1] + kg * (z[t] - a * h * output[t-1])
    p = p_past - h * kg * p_past
     
pl.figure('Kalman')
pl.plot(sequence, output, color = (0,1,0))
pl.plot(sequence, z, color = (1,0,0))
