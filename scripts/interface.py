#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 21:35:01 2018

@author: Raphael
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import importlib
os.chdir('/Users/Raphael/Github/2048/scripts/') #Select your working directory
cwd = os.getcwd()
G_2048=importlib.import_module("2048_class")
G_2048=importlib.reload(G_2048)
#%%

game = G_2048.Game_2048(4)

fig, ax = plt.subplots()
#bnext.on_clicked(game.update(game.up))

axleft = plt.axes([0.7, 0.01, 0.05, 0.075])
bleft = Button(axleft, 'left')
bleft.on_clicked(game.interactup)
#axright = plt.axes([0.7, 0.01, 0.05, 0.075])
#bright = Button(axprev, 'left')
plt.show()