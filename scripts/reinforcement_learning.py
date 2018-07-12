#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 22:38:07 2018

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
NN=importlib.import_module("NN_class")
NN=importlib.reload(NN)

#%%
game = G_2048.Game_2048(4)

#%%

model = NN.NNet(16,4,1,16)

W1 = np.random.randn(model.input_size, model.hidden_sizes)
W2 = np.random.randn(model.hidden_sizes, model.output_size)

W = [W1,W2]

#%%
def score_weight(game, model, W):
    stuck = False
    while game.state == 1 and stuck == False:
        stuck = True
        previous_grid = game.grid
        p = model.forward(game.grid.reshape(16),W)
        action_ind = p.argmax()
        action = [game.up,game.down,game.right,game.left][action_ind]
        game.update(action)
        if (previous_grid != game.grid).any() or (game.grid == 0).any():
            stuck = False
    return(game.score())

#%%
score_weight(game, model, W)
game.display()


