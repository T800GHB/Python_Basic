# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 12:16:01 2015

@author: andrew
"""

import svmMLiA

dataArr, labelArr = svmMLiA.loadDataSet('testSet.txt')

b, alphas = svmMLiA.smoSimple(dataArr, labelArr, 0.6, 0.001,40)

