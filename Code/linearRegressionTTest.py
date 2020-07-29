#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 13:41:19 2018

@author: ethanmoyer
"""


from __future__ import print_function
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.sandbox.regression.predstd import wls_prediction_std

np.random.seed(9876789)


y = np.array([45, 12, 19, 12, 4, 15, 48, 14, 34, 30, 39, 29, 47, 36, 21, 43, 3, 13, 9, 11, 48, 6, 7, 18, 47, 6, 40, 47])
X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28])
X = sm.add_constant(X)
 
model = sm.OLS(y, X)
results = model.fit()
print(results.summary())

#Look for P>abs(t) value at x1 row for analysis

y = np.array([genetic_attribute_list])
x = np.array([environmental_attribute_list])
x = sm.add_constant(X)
model = sm.OLS(y, X)
results = model.fit()
print(results.summary())

