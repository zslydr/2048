#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 16:33:57 2018

@author: Raphael
"""

import os
import importlib
import numpy as np
import seaborn as sns
os.chdir('/Users/Raphael/Github/2048/scripts/') #Select your working directory
cwd = os.getcwd()
G_2048=importlib.import_module("class_game")
G_2048=importlib.reload(G_2048)

#%% EXAMPLE

g = G_2048.Game_2048(4)
nb_coups = 0

while g.state == 1:
    #p = [g.up,g.right][np.random.randint(0,2)]
    #p = [g.up,g.down,g.right,g.left][np.random.randint(0,4)]
    p = [g.up,g.down,g.right,g.left][nb_coups%4]
    g.update(p)
    nb_coups += 1
    
print("Game over, score: ",g.score())
print("nombre de coups: ",nb_coups)
g.display()

#%%
score = []
n = 100
for i in range(n):
    g = G_2048.Game_2048(4)
    nb_coups = 0
    while g.state == 1:
        p = [g.up,g.right][np.random.randint(0,2)]
        #p = [g.up,g.down,g.right,g.left][np.random.randint(0,4)]
        #p = [g.up,g.down,g.right,g.left][nb_coups%4]
        g.update(p)
        nb_coups += 1
    score.append(g.score())

sns.tsplot(score)

