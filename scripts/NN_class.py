#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 17:35:21 2018

@author: Raphael
"""

import numpy as np

class NNet:
    
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
        


