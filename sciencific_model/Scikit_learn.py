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
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn import linear_model
import pylab as pl

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
    
def demo_knn():
    """
    This block will demostrate how to use KNN algorithm as classifier to 
    deal with iris data.
    """
    iris = datasets.load_iris()
    iris_data = iris.data
    iris_label = iris.target
    print('Categories in iris dataset is :\n',np.unique(iris_label))
    """
    Split iris data in train and test data.
    A random permutation, to split the data randomly.
    """
    np.random.seed(0)
    """Randomly permute a sequence, or return a permuted range."""
    indices = np.random.permutation(len(iris_label))
    iris_data_train = iris_data[indices[:-10]]
    iris_label_train = iris_label[indices[:-10]]
    iris_data_test = iris_data[indices[-10:]]
    iris_label_test = iris_label[indices[-10:]]
    """Create and fit a nearest-neighbor classifier"""
    knn = KNeighborsClassifier()
    knn.fit(iris_data_train, iris_label_train)
    """Predicted result"""
    result = knn.predict(iris_data_test)
    print('Prdicted result is:\n',result)
    print('Ground truth is:\n',iris_label_test)
    
def demo_linear_regression():
    """
    This block will demostrate how to use linear regression to fit Diabetes
    dataset ,then to predict state of new patients.
    """
    diabetes = datasets.load_diabetes()
    diabetes_data_train = diabetes.data[:-20]
    diabetes_label_train = diabetes.target[:-20]
    diabetes_data_test = diabetes.data[-20:]
    diabetes_label_test = diabetes.target[-20:]
    """Create and fit a linear regressor"""
    linreg = linear_model.LinearRegression()
    linreg.fit(diabetes_data_train, diabetes_label_train)
    print('The parameter of this linear model:\n',linreg.coef_)
    """Calculate mean square error"""
    mse = np.mean((linreg.predict(diabetes_data_test) - diabetes_label_test)**2)
    print('Mean square error on test set is:\n',mse)
    """
    Explained variance score: 1 is perfect prediction
     and 0 means that there is no linear relationship between X and Y.
    """
    score = linreg.score(diabetes_data_test, diabetes_label_test)
    print('Relation coefficient between test data and label is:\n',score)
    
def demo():
    X = np.c_[ .5, 1].T
    y = [.5, 1]
    test = np.c_[ 0, 2].T
    regr = linear_model.LinearRegression()   
    
    pl.figure() 
    
    np.random.seed(0)
    for _ in range(6): 
       this_X = .1*np.random.normal(size=(2, 1)) + X
       regr.fit(this_X, y)
       pl.plot(test, regr.predict(test)) 
       pl.scatter(this_X, y, s=3) 
    pl.show()