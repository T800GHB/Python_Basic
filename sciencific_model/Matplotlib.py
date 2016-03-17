# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 23:51:44 2016

@author: T800GHB

This file will demostrate some plot from gallery
These plot are just part copy of teaching material from
http://www.labri.fr/perso/nrougier/teaching/matplotlib/scripts/
I just want to experience performence.

More interesting plot, reference http://matplotlib.org/gallery.html.
"""

import numpy as np
import pylab as plt

def f(x,y):
    return (1-x/2+x**5+y**3)*np.exp(-x**2-y**2)

def demo_plot():
    n = 256
    X = np.linspace(-np.pi,np.pi,n,endpoint=True)
    Y = np.sin(2*X)
    
    plt.axes([0.025,0.025,0.95,0.95])
    
    plt.plot (X, Y+1, color='blue', alpha=1.00)
    plt.fill_between(X, 1, Y+1, color='blue', alpha=.25)
    
    plt.plot (X, Y-1, color='blue', alpha=1.00)
    plt.fill_between(X, -1, Y-1, (Y-1) > -1, color='blue', alpha=.25)
    plt.fill_between(X, -1, Y-1, (Y-1) < -1, color='red',  alpha=.25)
    
    plt.xlim(-np.pi,np.pi), plt.xticks([])
    plt.ylim(-2.5,2.5), plt.yticks([])
    # savefig('../figures/plot_ex.png',dpi=48)
    plt.show()

def demo_scatter():
    n = 1024
    X = np.random.normal(0,1,n)
    Y = np.random.normal(0,1,n)
    T = np.arctan2(Y,X)
    
    plt.axes([0.025,0.025,0.95,0.95])
    plt.scatter(X,Y, s=75, c=T, alpha=.5)
    
    plt.xlim(-1.5,1.5), plt.xticks([])
    plt.ylim(-1.5,1.5), plt.yticks([])
    # savefig('../figures/scatter_ex.png',dpi=48)
    plt.show()
    
def demo_bar():
    n = 12
    X = np.arange(n)
    Y1 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)
    Y2 = (1-X/float(n)) * np.random.uniform(0.5,1.0,n)
    
    plt.axes([0.025,0.025,0.95,0.95])
    plt.bar(X, +Y1, facecolor='#9999ff', edgecolor='white')
    plt.bar(X, -Y2, facecolor='#ff9999', edgecolor='white')
    
    for x,y in zip(X,Y1):
        plt.text(x+0.4, y+0.05, '%.2f' % y, ha='center', va= 'bottom')
    
    for x,y in zip(X,Y2):
        plt.text(x+0.4, -y-0.05, '%.2f' % y, ha='center', va= 'top')
    
    plt.xlim(-.5,n), plt.xticks([])
    plt.ylim(-1.25,+1.25), plt.yticks([])
    
    # savefig('../figures/bar_ex.png', dpi=48)
    plt.show()
    
def demo_contour():    

    n = 256
    x = np.linspace(-3,3,n)
    y = np.linspace(-3,3,n)
    X,Y = np.meshgrid(x,y)
    
    plt.axes([0.025,0.025,0.95,0.95])
    
    plt.contourf(X, Y, f(X,Y), 8, alpha=.75, cmap=plt.cm.hot)
    C = plt.contour(X, Y, f(X,Y), 8, colors='black', linewidth=.5)
    plt.clabel(C, inline=1, fontsize=10)
    
    plt.xticks([]), plt.yticks([])
    # savefig('../figures/contour_ex.png',dpi=48)
    plt.show()

def demo_imshow():
    n = 10
    x = np.linspace(-3,3,3.5*n)
    y = np.linspace(-3,3,3.0*n)
    X,Y = np.meshgrid(x,y)
    Z = f(X,Y)
    
    plt.axes([0.025,0.025,0.95,0.95])
    plt.imshow(Z,interpolation='nearest', cmap='bone', origin='lower')
    plt.colorbar(shrink=.92)
    
    plt.xticks([]), plt.yticks([])
    # savefig('../figures/imshow_ex.png', dpi=48)
    plt.show()
        
def demo_pie():
    n = 20
    Z = np.ones(n)
    Z[-1] *= 2
    
    plt.axes([0.025,0.025,0.95,0.95])
    
    plt.pie(Z, explode=Z*.05, colors = ['%f' % (i/float(n)) for i in range(n)])
    plt.gca().set_aspect('equal')
    plt.xticks([]), plt.yticks([])
    
    # savefig('../figures/pie_ex.png',dpi=48)
    plt.show()
    
def demo_quiver():
    n = 8
    X,Y = np.mgrid[0:n,0:n]
    T = np.arctan2(Y-n/2.0, X-n/2.0)
    R = 10+np.sqrt((Y-n/2.0)**2+(X-n/2.0)**2)
    U,V = R*np.cos(T), R*np.sin(T)
    
    plt.axes([0.025,0.025,0.95,0.95])
    plt.quiver(X,Y,U,V,R, alpha=.5)
    plt.quiver(X,Y,U,V, edgecolor='k', facecolor='None', linewidth=.5)
    
    plt.xlim(-1,n), plt.xticks([])
    plt.ylim(-1,n), plt.yticks([])
    
    # savefig('../figures/quiver_ex.png',dpi=48)
    plt.show()
    
def demo_grid():
    ax = plt.axes([0.025,0.025,0.95,0.95])

    ax.set_xlim(0,4)
    ax.set_ylim(0,3)
    ax.xaxis.set_major_locator(plt.MultipleLocator(1.0))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(0.1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1.0))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(0.1))
    ax.grid(which='major', axis='x', linewidth=0.75, linestyle='-', color='0.75')
    ax.grid(which='minor', axis='x', linewidth=0.25, linestyle='-', color='0.75')
    ax.grid(which='major', axis='y', linewidth=0.75, linestyle='-', color='0.75')
    ax.grid(which='minor', axis='y', linewidth=0.25, linestyle='-', color='0.75')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    # savefig('../figures/grid_ex.png',dpi=48)
    plt.show()
    
def demo_multi_grid():
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.025, left=0.025, top = 0.975, right=0.975)
    
    plt.subplot(2,1,1)
    plt.xticks([]), plt.yticks([])
    
    plt.subplot(2,3,4)
    plt.xticks([]), plt.yticks([])
    
    plt.subplot(2,3,5)
    plt.xticks([]), plt.yticks([])
    
    plt.subplot(2,3,6)
    plt.xticks([]), plt.yticks([])
    
    # plt.savefig('../figures/multiplot_ex.png',dpi=48)
    plt.show()
    
def demo_polar():
    ax = plt.axes([0.025,0.025,0.95,0.95], polar=True)

    N = 20
    theta = np.arange(0.0, 2*np.pi, 2*np.pi/N)
    radii = 10*np.random.rand(N)
    width = np.pi/4*np.random.rand(N)
    bars = plt.bar(theta, radii, width=width, bottom=0.0)
    
    for r,bar in zip(radii, bars):
        bar.set_facecolor( plt.cm.jet(r/10.))
        bar.set_alpha(0.5)
    
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    # savefig('../figures/polar_ex.png',dpi=48)
    plt.show()
    
def demo_3D():
    from mpl_toolkits.mplot3d import Axes3D

    fig = plt.figure()
    ax = Axes3D(fig)
    X = np.arange(-4, 4, 0.25)
    Y = np.arange(-4, 4, 0.25)
    X, Y = np.meshgrid(X, Y)
    R = np.sqrt(X**2 + Y**2)
    Z = np.sin(R)
    
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.cm.hot)
    ax.contourf(X, Y, Z, zdir='z', offset=-2, cmap=plt.cm.hot)
    ax.set_zlim(-2,2)
    
    # savefig('../figures/plot3d_ex.png',dpi=48)
    plt.show()