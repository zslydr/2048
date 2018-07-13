#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 22:38:07 2018

@author: Raphael
"""

import os
import importlib
import numpy as np
os.chdir('/Users/Raphael/Github/2048/scripts/') #Select your working directory
cwd = os.getcwd()
G_2048=importlib.import_module("2048_class")
G_2048=importlib.reload(G_2048)
NN=importlib.import_module("NN_class")
NN=importlib.reload(NN)

#%% SCORE FUNCTION BASED ON THE WEIGHTS OF THE NN

def score_weight(game, model, W):
    # Indicate if the game is stuck (because NN can loop over a useless move without the game being lost)
    stuck = False 
    while game.state == 1 and stuck == False: # While the game is not lost and not stuck
        stuck = True
        previous_grid = game.grid # to test whether the game is stuck or not
        p = model.forward(game.grid.reshape(16),W) # Forward propagation with the grid as input
        action_ind = p.argmax() # Get the action index to perform
        action = [game.up,game.down,game.right,game.left][action_ind] # Select the action to perform
        game.update(action) # Perform the action
        if (previous_grid != game.grid).any() or (game.grid == 0).any(): #Check if the game is not stuck
            stuck = False
    return(game.score())

#%%
game = G_2048.Game_2048(4) # Initialize the game grid


model = NN.NNet(16,4,1,16) # Initialize the type of the NN (or population in our case)

W1 = np.random.randn(model.input_size, model.hidden_sizes)
W2 = np.random.randn(model.hidden_sizes, model.output_size)

W = [W1,W2] # Initialize ONE individual


score = score_weight(game, model, W) # SCORE of the inidividual
print(score)
game.display()


