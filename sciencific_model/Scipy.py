# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 00:08:38 2016

@author: T800GHB

This file will demostrate how to use some basic function in scipy.
Scipy include some function to process image, this part will show at
computer vision field.
"""
import numpy as np
from scipy.optimize import leastsq
import pylab as pl
from scipy import interpolate

def func(x, p):
    """
    Parameter of this function will be fitted
    """
    A, k, theta = p
    """Return a result of function with current parameter"""
    return A*np.sin(2 * np.pi* k * x + theta)
    
def residuals(p, x, y):
    """
    Calculate the residuals between prediction and real value.
    """
    return func(x, p) - y
    
def demo_leastsq():
    """
    Use least square to fit parameter of function.
    In this demostration, do 3 step:
    1.Generate some noise data derive frome sine function;
    2.Give a first guess;
    3.Use those above, fit parameters of function.
    """
    x = np.linspace(0, -2*np.pi, 100)
    A, k, theta = 10, 0.34, np.pi/6     #real parameter
    y0 = func(x, [A, k, theta])         #real data
    """ y1 simulate the data that we have sampled."""
    y1 = y0 + 2*np.random.randn(len(x))
    """First guess of those parameters need to fit """
    p0 = [0,0.2,0]
    """
    Call leastsq() to fit. 
    keep same argument order between args and residuals.
    """
    plsq = leastsq(residuals, p0, args = (x, y1))
    print('Real parameter:' ,[A, k, theta])
    print('Fitted parameter:', plsq[0])
    
    pl.plot(x, y0, label='Real data')
    pl.plot(x, y1, label='Real data with noise')
    pl.plot(x, func(x, plsq[0]), label='Fitted data')
    pl.legend()
    pl.show()
    
def demo_B_spline():
    """
    Interpolate B spline
    """
    x = np.linspace(0, 2*np.pi+np.pi/4, 10)
    y = np.sin(x)
    
    x_new = np.linspace(0, 2*np.pi+np.pi/4, 100)
    f_linear = interpolate.interp1d(x, y)
    tck = interpolate.splrep(x, y)
    y_bspline = interpolate.splev(x_new, tck)
    
    pl.figure('Interpolate')
    pl.plot(x, y, 'o', label = 'Orignal data')
    pl.plot(x_new, f_linear(x_new), label = 'Linear interpolate')
    pl.plot(x_new, y_bspline, label = 'B-Spline interpolate')
    pl.legend()
    pl.show()