# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 22:48:22 2016

@author: T800GHB

This file will demostrate how to use basic function in scikit-learn

sklearn is model name of scikit-learn.
scikit-learn has contained some dataset, such as  iris and digits.
"""

from sklearn import datasets
from sklearn import svm
from sklearn.externals import joblib

def demo_quick_start():
    """
    This block of code is duplication from offical documentation --- quick start.
    Using svm to do classification.
    """    
    digits = datasets.load_digits()
    
    """
    Give a fixed parameter to initialize svm model, return a classifier.
    SVC is C-Support Vector Classification.
    """
    clf = svm.SVC(gamma = 0.001, C = 100)
    """
    Use all the images of our dataset apart from the last one to train model.
    fit() function will perform optimization procedure.
    """
    clf.fit(digits.data[:-1], digits.target[:-1])
    """
    Predict a new image which does not use to train model.
    """
    result = clf.predict(digits.data[-1:])
    print('The category of last image is:', result)
    """
    Two way to save model: pickle and joblib.
    Use joblib’s replacement of pickle (joblib.dump & joblib.load), 
    which is more efficient on big data, 
    but can only pickle to the disk and not to a string.
    
    joblib.dump returns a list of filenames. 
    Each individual numpy array contained in the clf object 
    is serialized as a separate file on the filesystem.
    All files are required in the same folder
    when reloading the model with joblib.load.
    """
    joblib.dump(clf, 'svm_model.pkl')
    """Load from list of files"""
    clf_dup = joblib.load('svm_model.pkl')
    """
    Refitting and update parameter of svm model.
    The default kernel is rbf(Radial basis function), 
    set model with linear kernel, then fit it.
    """
    clf_dup.set_params(kernel = 'linear').fit(
    digits.data[:-1], digits.target[:-1])
    print('Category of first image is:', clf_dup.predict(digits.data[0:1]))
    