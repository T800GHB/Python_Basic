# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 19:31:26 2019

@author: hanbing.guo
"""

import numpy as np
from matplotlib import pyplot as plt

slot_length = 5.0

def rotate(theta, x, y, is_rad=True):
    if is_rad:
        rad = theta
    else:
        rad = np.deg2rad(theta)
        
    rx = x * np.cos(rad) - y * np.sin(rad)
    ry = x * np.sin(rad) + y * np.cos(rad)
    return rx, ry



def rotate_fly(theta, head_x, head_y, center_x, center_y):
    ox = head_x - center_x
    oy = head_y - center_y
    
    rx, ry = rotate(theta, ox, oy)
    
    fx = rx + center_x
    fy = ry + center_y
    
    return fx, fy

def show_demo():
    num_point = 100

    cx = 5
    cy = 5
    
    hx = cx
    hy = cy + 1
    
    length_noise = np.random.uniform(-0.2, 0.2, num_point)
    theta_noise = np.random.uniform(-10, 10, num_point)
    
    plt.figure(figsize=(6.5,6.5))
    for i in range(num_point):
        plt.clf()
        plt.axis([0, 2*cx, 0, 2 * cy])
        sx, sy = rotate_fly(theta_noise[i], hx, hy + length_noise[i], cx, cy)
    #    plt.plot([sx, cx], [sy, cy], color=(1,0,0))
        ax = plt.axes()
        ax.arrow(cx, cy, sx - cx, sy - cy, color=(1,0,0), head_width=0.15, head_length=0.15)
        plt.pause(0.3)
        
    plt.show()
    
def construct_slot(x, y, theta, slot_width):
    half_width = slot_width / 2
    half_length = slot_length / 2
    slot_corner = np.zeros((4,2))
    
    corner = np.zeros((4,2))
    corner[0] = [half_width, half_length]
    corner[1] = [half_width, -half_length]
    corner[2] = [-half_width, -half_length]
    corner[3] = [-half_width, half_length]
    
    for i in range(4):
        slot_corner[i] = rotate(theta, corner[i,0], corner[i, 1])
    
    
    slot_corner[:,0] = slot_corner[:,0] + x
    slot_corner[:,1] = slot_corner[:,1] + y
        
    
    return slot_corner
        
def parse_slot_to_vector(slot):
    if not slot.shape == (4,2):
        return None
    else:
        theta = np.arctan(slot[0,1]-slot[1,1], slot[0,0], slot[1,0])
        x = np.mean([slot[0,0], slot[1,0], slot[2,0], slot[3,0]])
        y = np.mean([slot[0,1], slot[1,1], slot[2,1], slot[3,1]])
        width = np.sqrt((slot[0,0] - slot[3,0])**2 + (slot[0,1] - slot[3,1])**2)
        
        return x, y, theta, width
    
#show_demo()
