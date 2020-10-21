# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 09:57:12 2019

@author: hanbing.guo
"""

import numpy as np
from matplotlib import pyplot as plt
import rotate_util as ru
import smooth_util as su

num_point = 200

center = 15
cx = center
cy = center
unit_range = 0.3
arrow_length = 2.4
slot_width = arrow_length
noise_x = np.random.uniform(-unit_range,unit_range,num_point)
noise_y = np.random.uniform(-unit_range,unit_range,num_point)
angle_offset = 2890
num_moving = 160

drift = 0.0

length_noise = np.random.uniform(-0.3, 0.3, num_point)
length_noise1 = np.random.uniform(-0.3, 0.3, num_point)
theta_noise = np.random.uniform(-5, 5, num_point) + angle_offset
theta_noise1 = np.random.uniform(-5, 5, num_point) + angle_offset


nx = cx + noise_x
ny = cy + noise_y
hx = nx
hy = ny + arrow_length + length_noise

nx1 = nx
ny1 = ny + slot_width

text_offset = 3
        
def demo_location_smooth():
    kf = su.KalmanLoc()
    
    plt.figure(figsize=(13,6.5))
    for i in range(num_point):
        plt.clf()
        ap = plt.subplot(1,2,1)
        ap.axis([0,2*center,0,2*center])
        ap.set_title('original')
        ap.scatter(nx[i], ny[i], color=(1,0,0))
                
        bp = plt.subplot(1,2,2)
        bp.axis([0,2*center,0,2*center])
        bp.set_title('smooth')
        sx, sy = kf.smooth(nx[i], ny[i])
        plt.scatter(sx, sy, color=(0,1,0))
        print('ox: ',nx[i], ',oy: ', ny[i], ',nx: ', sx, ',ny: ', sy)
        plt.pause(0.2)
        
def demo_pose_smooth():
    kf = su.KalmanPose()
    fig = plt.figure(figsize=(13,6.5))
    for i in range(num_point):
        fig.clf()
        ap = fig.add_subplot(121)
        ap.axis([0,2*center,0,2*center])
        ap.set_title('original')
        osx, osy = ru.rotate_fly(np.deg2rad(theta_noise[i]), hx[i], hy[i], nx[i], ny[i])
        
        ap.arrow(nx[i], ny[i], osx - nx[i], osy - ny[i], color=(1,0,0), head_width=0.25, head_length=0.25)
        
        bp = fig.add_subplot(122)
        
        bp.axis([0,2*center,0,2*center])
        bp.set_title('smooth')
        sx, sy, st, sl = kf.smooth(nx[i], ny[i], np.deg2rad(theta_noise[i]), arrow_length + length_noise[i] )
        nsx, nsy = ru.rotate_fly(st, sx , sy + sl, sx, sy)
        bp.arrow(sx, sy, nsx - sx, nsy - sy, color=(0,1,0), head_width=0.25, head_length=0.25)
        plt.pause(0.2)
        
    plt.show()
    
def convert_to_plot_list(corner_list):
    corner_list = [list(x) for x in corner_list]
    corner_list.append(corner_list[0])
    in_x = []
    in_y = []
    for corner in corner_list:
        in_x.append(corner[0])
        in_y.append(corner[1])
    return in_x, in_y

def demo_single_slot():
    
    kf = su.KalmanPose()
    fig = plt.figure(figsize=(17,8.5))
    result = []
    
    for i in range(num_point):
        fig.clf()
        ap = fig.add_subplot(121)
        ap.axis([-3*center,2*center,-3*center,2*center])
        ap.set_title('original')
        if (i < num_moving):
            ny[i] -= i * drift
            hy[i] -= i * drift
        else :
            ny[i] -= num_moving * drift
            hy[i] -= num_moving * drift
        osx, osy = ru.rotate_fly(np.deg2rad(theta_noise[i]), hx[i], hy[i], nx[i], ny[i])
        
        ap.arrow(nx[i], ny[i], osx - nx[i], osy - ny[i], color=(1,0,0), head_width=0.25, head_length=0.25)
        
        raw_corner_list = ru.construct_slot(nx[i], ny[i], np.deg2rad(theta_noise[i]), arrow_length + length_noise[i])
        raw_in_x, raw_in_y = convert_to_plot_list(raw_corner_list)
        ap.plot(raw_in_x, raw_in_y, color=(1,0,1))
        ap.text(nx[i] + text_offset, ny[i] + text_offset, '1')
        bp = fig.add_subplot(122)
        
        bp.axis([-3*center,2*center,-3*center,2*center])
        bp.set_title('smooth')
        sx, sy, st, sl = kf.smooth(nx[i], ny[i], np.deg2rad(theta_noise[i]), arrow_length + length_noise[i])
        result.append([sx, sy, st, sl])
        smooth_corner_list = ru.construct_slot(sx, sy, st, sl)
        smooth_in_x, smooth_in_y = convert_to_plot_list(smooth_corner_list)
        bp.plot(smooth_in_x, smooth_in_y, color=(0,1,1))
        nsx, nsy = ru.rotate_fly(st, sx , sy + sl, sx, sy)
        bp.arrow(sx, sy, nsx - sx, nsy - sy, color=(0,1,0), head_width=0.25, head_length=0.25)
        bp.text(sx + text_offset, sy + text_offset, '2')
        plt.pause(0.1)
        
    plt.show()
    
    with open('original_pose.txt', 'w') as fh:
        for i in range(num_point):
            fh.writelines(','.join([str(nx[i]), str(ny[i]), 
                        str(np.deg2rad(theta_noise[i])), str(arrow_length +length_noise[i])]))
            fh.writelines('\n')
            
    with open('smooth_pose.txt', 'w') as fh:
        for sx, sy, st, sl in result:
            fh.writelines(','.join([str(sx), str(sy), str(st), str(sl)]))
            fh.writelines('\n')
            
tracker = su.SlotTracker()

result = []
fig = plt.figure(figsize=(14,7))
for i in range(num_point):
    fig.clf()
    ap = fig.add_subplot(121)
    ap.axis([0,2*center,0,2*center])
    ap.set_title('original')
    if i < num_moving:
        ny[i] -= i * drift
        ny1[i] -= i * drift
    else:
        ny[i] -= num_moving * drift
        ny1[i] -= num_moving * drift

    raw_corner_list = ru.construct_slot(nx[i], ny[i], np.deg2rad(theta_noise[i]), arrow_length + length_noise[i])
    raw_in_x, raw_in_y = convert_to_plot_list(raw_corner_list)
    ap.plot(raw_in_x, raw_in_y, color=(1, 0, 1))
    
    raw_corner_list1 = ru.construct_slot(nx1[i], ny1[i], np.deg2rad(theta_noise1[i]), arrow_length + length_noise1[i])
    raw_in_x1, raw_in_y1 = convert_to_plot_list(raw_corner_list1)
    ap.plot(raw_in_x1, raw_in_y1, color=(1, 0, 1))
    
    bp = fig.add_subplot(122)
        
    bp.axis([0, 2*center, 0, 2*center])
    bp.set_title('smooth')
    slot1 = su.Slot(nx[i], ny[i], np.deg2rad(theta_noise[i]), arrow_length + length_noise[i])
    slot2 = su.Slot(nx1[i], ny1[i], np.deg2rad(theta_noise1[i]), arrow_length + length_noise1[i])
    tracker.match_track_pose(slot1)
    tracker.match_track_pose(slot2)
    
    output = tracker.get_output()
    for idx, item in output:
        result.append([item.x, item.y, item.angle, item.length])
    for idx, item in output:
        smooth_corner_list = ru.construct_slot(item.x, item.y, item.angle, item.length)
        smooth_x, smooth_y = convert_to_plot_list(smooth_corner_list)
        bp.plot(smooth_x, smooth_y, color=(0, 1, 0))
        bp.text(smooth_x[0], smooth_y[0], str(idx))

    plt.pause(0.1)

with open('original_slot_list.csv', 'w') as fh:
    for i in range(num_point):
        fh.writelines(','.join([str(nx[i]), str(ny[i]),
                                str(np.deg2rad(theta_noise[i])), str(arrow_length + length_noise[i])]))
        fh.writelines('\n')
        fh.writelines(','.join([str(nx1[i]), str(ny1[i]),
                                str(np.deg2rad(theta_noise1[i])), str(arrow_length + length_noise1[i])]))
        fh.writelines('\n')

with open('smooth_slot_list.csv', 'w') as fh:
    for sx, sy, st, sl in result:
        fh.writelines(','.join([str(sx), str(sy), str(st), str(sl)]))
        fh.writelines('\n')

plt.show()

