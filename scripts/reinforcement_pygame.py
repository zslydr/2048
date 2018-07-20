#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 15:17:48 2018

@author: Raphael
"""
import os
import importlib
import seaborn as sns
import numpy as np
import time
import pygame
import pickle
os.chdir('/Users/Raphael/Github/2048/scripts/') #Select your working directory
cwd = os.getcwd()
G_2048=importlib.import_module("2048_class")
G_2048=importlib.reload(G_2048)

game = G_2048.Game_2048(4)

with open('winner_net.pickle', 'rb') as f:
    winner_net = pickle.load(f)

pygame.font.init()
my_font = pygame.font.Font(None, 32)

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (220/255, 220/255, 220/255)
colors = [GREY] + sns.color_palette("Oranges", 15)
font_color = BLACK

values = [0] + [2**x for x in range(1,15)]


# This sets the WIDTH and HEIGHT of each grid location
WIDTH_grid = 150
HEIGHT_grid = WIDTH_grid
 
# This sets the margin between each cell
MARGIN = 5
 
pygame.init()
 
# Set the width and height of the screen [width, height]
size_grid = [(WIDTH_grid)*game.n + 5 * MARGIN, (HEIGHT_grid)*game.n + 5 * MARGIN]
size = size_grid
size[1] += 100
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
begin = False
penality = 0
bad_move_cmpt = 0
stuck = False 
actions = []
nb_it = 0
# -------- Main Program Loop -----------
while not done:
    
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            begin = True
            
    
    screen.fill(WHITE)
    
    # DRAW THE GRID
    for row in range(game.n):
        for column in range(game.n):
            color = WHITE
            ind_color = values.index(int(game.grid[row,column])) # COLOR INDEX FROM LIST OF POSSIBLE VALUES
            pygame.draw.rect(screen,
                             np.floor(np.dot(colors[ind_color],255)),
                             [(MARGIN + WIDTH_grid) * column + MARGIN,
                              (MARGIN + HEIGHT_grid) * row + MARGIN,
                              WIDTH_grid,
                              HEIGHT_grid])
            textsurface = my_font.render(str(int(game.grid[row,column])), True, font_color)
            screen.blit(textsurface, ((MARGIN + WIDTH_grid) * column + MARGIN+5,(MARGIN + HEIGHT_grid) * row + MARGIN + 5))
    
    
    textsurface = my_font.render("Fitness = "+str(game.score - penality), True, font_color)
    screen.blit(textsurface, (size[0]/2 - 50 , size[1] - 75))
    
    textsurface = my_font.render("Score = "+str(game.score), True, font_color)
    screen.blit(textsurface, (size[0]/2 - 50 , size[1] - 55))
    
    
    if begin == True:
        if game.state == 1 and stuck == False:
            stuck = True
            previous_grid = game.grid # to test whether the game is stuck or not
            p = winner_net.activate(np.append(game.grid, [bad_move_cmpt**2, np.count_nonzero(game.grid)]))
            action_ind = np.array(p).argmax() # Get the action index to perform
            actions.append(action_ind)
            action = [game.up,game.down,game.right,game.left][action_ind] # Select the action to perform
            action() # Perform the action
            #print((previous_grid != game.grid).any())
            if game.changed: #Check if the game is not stuck
                bad_move_cmpt = 0
                penality = 0
                stuck = False
                screen.blit(textsurface, (size[0]/2 - 50 , size[1] - 35))
                rect = pygame.Rect(0, 0, WIDTH_grid * (row + 1), HEIGHT_grid * (column + 1))
                sub = screen.subsurface(rect)
                pygame.image.save(sub, "/Users/Raphael/Github/2048/resources/screenshots/" + "screenshot" + str(nb_it) + ".png")
                nb_it += 1
            if stuck == True:
                bad_move_cmpt += 1
                if bad_move_cmpt < 20:
                    stuck = False
            penality += bad_move_cmpt
        else:
            textsurface = my_font.render("Neural net stuck", True, font_color)
            screen.blit(textsurface, (size[0]/2 - 50 , size[1] - 35))


    

    #time.sleep(0.1)
    #game.next_state()
    time.sleep(0.1)
    pygame.display.flip()
 
    # --- Limit to 10 frames per second
    clock.tick(30)
 
# Close the window and quit.
pygame.quit()
#sns.countplot(actions)

#%%
ss_path = "/Users/Raphael/Github/2048/resources/screenshots/"
from os import listdir
from os.path import isfile, join
ss_names = [ss_path + f for f in listdir(ss_path) if isfile(join(ss_path, f)) and f != '.DS_Store']

d={}
for i in range(len(ss_names)):
    d[int(ss_names[i][:-4][59:])] = ss_names[i]

ss_names = []
for key in sorted(d):
    ss_names.append(d[key])

#%%
import imageio
with imageio.get_writer('/Users/Raphael/Github/2048/resources/2048_AI.gif', mode='I') as writer:
    for ss_name in ss_names:
        image = imageio.imread(ss_name)
        writer.append_data(image)
    
#%%

import os, shutil
for ss_name in ss_names:
    try:
        if os.path.isfile(ss_name):
            os.unlink(ss_name)
        #elif os.path.isdir(file_path): shutil.rmtree(file_path)
    except Exception as e:
        print(e)


