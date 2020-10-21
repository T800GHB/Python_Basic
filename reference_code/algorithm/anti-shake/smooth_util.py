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

class Slot:
    def __init__(self,x=0.0, y=0.0, angle=0.0, length=0.0):
        self.x = x
        self.y = y
        self.angle = angle
        self.length = length
    
    def clear(self):
        self.x = 0.0
        self.y = 0.0
        self.angle = 0.0
        self.length = 0.0
    
    def set_pose(self, x, y, angle, length):
        self.x = x
        self.y = y
        self.angle = angle
        self.length = length
        
        
class Smoother:
    def __init__(self, factor = 0.6):
        self.px = 0
        self.py = 0
        self.__factor = factor
        self.__init_status = False
        
    def smooth(self, x, y):
        if not self.__init_status:
            self.px = x
            self.py = y
            self.__init_status = True
            
            return x, y
        
        outx = self.__factor * x + (1 - self.__factor) * self.px
        outy = self.__factor * y + (1 - self.__factor) * self.py
        
        self.px = outx;
        self.py = outy;
        
        return outx, outy
    
class KalmanSmooth:
    def __init__(self):
        self.px = 10
        self.py = 10
        self.ox = 0
        self.oy = 0
        self.R = 0.1
        self.Q = 0.001
        self.init_status = False
    
    def smooth(self, x, y):
        if not self.init_status:
            self.init_status = True
            self.ox = x
            self.oy = y
            
            return x, y
    
        self.px = self.px + self.Q
        kgx = self.px / (self.px + self.R)
        outx = self.ox + kgx * (x - self.ox)
        self.px = self.px * (1 - kgx)
        
        self.py = self.py + self.Q
        kgy = self.py / (self.py + self.R)
        outy = self.oy + kgy * (y - self.oy)
        self.py = self.py * (1 - kgy)
        
        self.ox = outx
        self.oy = outy
        
        return outx, outy
        
class KalmanLoc:
    def __init__(self):
        self.P = np.ones(2)
        self.R = np.ones(2)
        self.Q = np.ones(2)
        self.init_status = False
        self.old_pose = np.zeros((2))
    
    def smooth(self, x, y, theta = 0):
        if not self.init_status:
            self.init_status = True
            self.P *= 10
            self.R *= 0.1
            self.Q *= 0.001
            self.old_pose = np.array([x, y])
            print('Init here')
            return x, y
        
        new_loc = np.array([x, y])
        self.P = self.P + self.Q
        kg = self.P / (self.P + self.R)
        output = self.old_pose + kg * (new_loc - self.old_pose)
        self.P = self.P * (np.ones((2,)) - kg)
        
        self.old_pose = output
        
        return output[0], output[1]
    
class KalmanPose:
    def __init__(self):
        self.dim = 4
        self.P = np.ones(self.dim)
        self.R = np.ones(self.dim)
        self.Q = np.ones(self.dim)
        self.init_status = False
        self.hit = False
        self.old_pose = Slot()
    
    def smooth(self, x, y, theta, length):
        if not self.init_status:
            self.init_status = True
            self.P *= 10
            self.R *= 0.1
            self.Q *= 0.001
            self.old_pose = Slot(x,y,theta, length)
            return x, y, theta, length
        
        if (theta < 0 and self.old_pose.angle > 0 
            and np.abs(theta) > np.pi / 2 and np.abs(self.old_pose.angle) > np.pi / 2):
            normal_theta = 2 * np.pi + theta
        elif (theta > 0 and self.old_pose.angle < 0 
              and np.abs(theta) > np.pi / 2 and np.abs(self.old_pose.angle) > np.pi / 2):
            normal_theta = theta - 2 * np.pi
        else:
            normal_theta = theta
            
        old_array = np.array([self.old_pose.x, self.old_pose.y, self.old_pose.angle, self.old_pose.length])  
        new_loc = np.array([x, y, normal_theta, length])
        self.P = self.P + self.Q
        kg = self.P / (self.P + self.R)
        output = old_array + kg * (new_loc - old_array)
        self.P = self.P * (np.ones((self.dim,)) - kg)
        
        self.old_pose = Slot(output[0], output[1], output[2], output[3])
        
        return output[0], output[1], output[2], output[3]
    
    def reset(self):
        self.init_status = False
    
            
class SlotTracker:
    def __init__(self, max_capacity = 12, accept_range = 0.6):
        self.track_pool = [KalmanPose() for i in range(max_capacity)]
        self.thre = accept_range
    
    def match_track_pose(self, slot):
        record_idx = -1
        for i, record in enumerate(self.track_pool):
            x_dis = abs(slot.x - record.old_pose.x)
            y_dis = abs(slot.y - record.old_pose.y)
            if x_dis < self.thre and y_dis < self.thre and record.init_status:
                record.hit = True
                record.smooth(slot.x, slot.y, slot.angle, slot.length)
                record_idx = i
                break
                
        if record_idx < 0:
            for i, record in enumerate(self.track_pool):
                if not record.init_status:
                    record.smooth(slot.x, slot.y, slot.angle, slot.length)
                    record.hit = True
                    break
        
    def get_output(self):
        result = []
        for i, record in enumerate(self.track_pool):
            if record.hit:
                result.append([i,record.old_pose])
                record.hit = False
            else:
                record.reset()
                
        return result
    