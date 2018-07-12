#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:35:21 2018

@author: Raphael
"""

import os
import numpy as np
os.chdir('/Users/Raphael/') #Select your working directory
cwd = os.getcwd()
    
#%%

class NN:
    
    def __init__(self,input_size, output_size, nb_hidden, hidden_sizes):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_sizes = hidden_sizes
        self.nb_hidden = nb_hidden
        
    def sigmoid(self, s):
        return 1/(1+np.exp(-s))
    
    def activation(self, last_layer):
        return(np.array([x/sum(last_layer) for x in last_layer]))
    
    def forward(self, input_, weights):
        l = input_
        for w in weights:
            l = self.sigmoid(np.dot(l,w))
        return(self.activation(l))
    
    def cross_entropy(self, input_, weights, output_):
    m = y.shape[0]
    p = self.forward(input_, weights)
    log_likelihood = -np.log(p[range(m),output_])
    loss = np.sum(log_likelihood) / m
    return loss
        


#%%

X = np.array([0,0,1])

NNet = NN(3,3,3)

W1 = np.random.randn(NNet.input_size, NNet.hidden_size)
W2 = np.random.randn(NNet.hidden_size, NNet.output_size)

W = [W1,W2]

p = NNet.forward(X,W)

#%%

np.linalg.norm(np.array([1,0])-np.array([0.5,0.5]))


#%%

np.dot([0,0,1],np.random.randn(3,2))