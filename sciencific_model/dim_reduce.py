# -*- coding: utf-8 -*-
"""
Created on Sun Sep 25 21:07:19 2016

@author: andrew
"""


import numpy.linalg as nl
import numpy as np
import image_process.data_import as di
import scipy.io as si

def demo_dim_reduce(save_result = False):
#==============================================================================
# Just want to receive first two return value,
# tuple indices must be integers or slices.
# If the wanted locations is not continous, there is no easy way.
#==============================================================================
    train_images, train_labels = di.load_mnist()[:2]
    
    num_samples, height, width = train_images.shape
    #Every column is a sample
    features = train_images.reshape((num_samples, height * width)).T    
    #Save numpy array as MATLAB specific format .mat
    si.savemat('matlab',{'feature_set': features, 'label_set': train_labels})
    
    pca_set = pca()
    
    lda_set = lda()
    #Save result as Matlab format
    if save_result:
        si.savemat('dim_reduce_result',{'pca_output':pca_set, 'lda_output':lda_set})

def pca(accept_ratio = 0.90):
#==============================================================================
#   Principal Component Analysis
#   Idea is to reserve main feature basis
#==============================================================================
    #Load data from mat, this a MATLAB specific format store data
    mat_data = si.loadmat('matlab.mat')
    #Data type convertion. Use astype method.
    feature_set = mat_data['feature_set'].astype(np.float) 
    #Number of samples
    num_samples = feature_set.shape[1]
    #Calculate all samples mean, dimension unchanged
    mean_all = np.mean(feature_set, 1)
    #Create a matrix contain all samples that minus mean
    samples_minus_mean = feature_set - np.tile(mean_all, (num_samples, 1)).T
    #Calculate convariance matrix for dataset
    c_all = samples_minus_mean.dot(samples_minus_mean.T) / num_samples
    '''
    Calculate eign-value and eign-vector, in MATLAB use eig(c_all,'noblance').
    In numpy, eig can't complete this work, but use svd produce same result with
    MATLAB
    '''
    eignvector, eignvalue, null = np.linalg.svd(c_all)
    #Decent sort and return index
    sort_index = np.argsort(-eignvalue)
    
    sum_eignvalue = eignvalue.sum()
    
    max_index = 0
    for i in range(len(sort_index)):
        ratio = eignvalue[sort_index[:i]].sum() / sum_eignvalue
        if accept_ratio < ratio:
            max_index = i
            break
    #According to ratio, select most important eign-vector
    project_basis = eignvector[:,sort_index[:max_index + 1]]
    #According to new basis, project orignal feature to lower dimensional feature
    pca_set = (project_basis.T).dot(feature_set)

    return pca_set
    
def lda(accept_ratio = 0.95):
#==============================================================================
#   Linear Discriminant Analysis
#   This is supervised dimensional reduction method
#   So, samples and its labels are needed.
#   The main idea is that maximize distance between classes, at same time
#   minimize distance within class
#==============================================================================
    '''
    This example works fine, but the convariance matrix of within-class
    can't calculate inverse matrix, so run this example will confront some
    problem
    '''
    mat_data = si.loadmat('light.mat')
    
    features = mat_data['feature_set'].astype(np.float)
    labels = mat_data['label_set']
    
    '''For LDA processing conveniently, sorted label and feature is needed'''
    re_index = np.argsort(labels,1).reshape(labels.shape[1])
    label_set = labels[0,re_index]
    feature_set = features[:, re_index]
    #Number of samples
    num_samples = feature_set.shape[1]
    #Number of feature dimension
    dim = feature_set.shape[0]
    #Label maybe not contiunious number, so get unique labels and its quantity
    unique_labels = np.unique(label_set)
    
    num_labels = unique_labels.shape[0]
    last_index = num_labels - 1
    #Use a matrix to store start index , end index and its quantity
    class_info = np.zeros((3,num_labels))
    #First start index
    class_info[0,0] = 0
    #Last end index
    class_info[1,last_index] = num_samples - 1
    #Temperory 
    tmp_label = label_set[0]
    class_num = 0
    '''
    Pay attention to this class information acquire,
    label need to be sorted ,not shuffled,[0,0,0,1,1,1,2,2,2] is ok,
    but [0,2,1,0,1,2] will not work.
    Because we want to calculate the convariance within class, choas label
    arrange is so bad to do this.
    '''
    for i in range(1,num_samples):
        if label_set[i] != tmp_label:
            class_info[2,class_num] = i - class_info[0,class_num]
            class_info[1,class_num] = i - 1
            class_num += 1
            class_info[0,class_num] = i
            tmp_label = label_set[i]
            
    
    class_info[2,last_index] = class_info[1,last_index] - class_info[0,last_index] + 1
    #Calculate all samples mean, dimension unchanged
    mean_all = np.mean(feature_set, 1)
    #Container of mean for each class
    mean_each = np.zeros((dim, num_labels), dtype = np.float)
    for i in range(num_labels):
        mean_each[:,i] = np.mean(feature_set[:,class_info[0,i]: class_info[1,i]], 1)
        
    mean_each_minus_all = mean_each - np.tile(mean_all, (mean_each.shape[1], 1)).T
    
    #Calculate covariance matrix between classes
    c_between = mean_each_minus_all.dot(mean_each_minus_all.T) / num_labels
    
    #Create a matrix contain all samples that minus mean of each class
    temp_set = np.zeros(feature_set.shape, dtype = np.float)
    
    for i in range(num_labels):
        temp_set[:, class_info[0,i]: class_info[1,i] + 1] = \
        feature_set[:, class_info[0,i]:class_info[1,i] + 1] \
        - np.tile(mean_each[:,i], (class_info[2,i], 1)).T
        
    #Calculate convariance matrix for each classes
    c_class = np.zeros((num_labels, dim, dim))
    for i in range(num_labels):
        c_class[i,...] =\
        temp_set[:, class_info[0,i]: class_info[1,i] + 1].dot(temp_set[:, class_info[0,i]: class_info[1,i] + 1].T)\
        / class_info[2,i]
        
    #Calculate convariance matrix within class
    c_within = c_class.sum(axis = 0)
    print('nima')
    #Calculate eign-value and eign-vector
    V,D = nl.eig(nl.inv(c_within).dot(c_between))
    #The result is complex number, real number is needed.
    eignvalue = V.astype(np.float)
    eignvector = D.astype(np.float)
    #Decent sort and return index, pay attention to sign - before array
    sort_index = np.argsort(-eignvalue)
    #Calculate sum of eign-value
    sum_eignvalue = eignvalue.sum()
    #Achive most important part of eign-value and eign-vector, according to ratio of sum of eign-vector    
    max_index = 0
    for i in range(len(sort_index)):
        ratio = eignvalue[sort_index[:i]].sum() / sum_eignvalue
        if accept_ratio < ratio:
            max_index = i
            break
    print('haha')
    #According to ratio, select most important eign-vector
    project_basis = eignvector[:,sort_index[:max_index + 1]]
    #According to new basis, project orignal feature to lower dimensional feature
    lda_set = (project_basis.T).dot(feature_set)
    print('fuck')
    return lda_set