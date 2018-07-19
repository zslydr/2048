#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 09:00:03 2018

@author: Raphael
"""
import os
import importlib
import seaborn as sns
import numpy as np
import time
os.chdir('/Users/Raphael/Github/2048/scripts/') #Select your working directory
cwd = os.getcwd()
G_2048=importlib.import_module("2048_class")
G_2048=importlib.reload(G_2048)

game = G_2048.Game_2048(4)
 
import pygame

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
WIDTH_grid = 100
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
 
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            game.down()
        if event.type == pygame.KEYUP and event.key == pygame.K_UP:
            game.up()
        if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
            game.right()
        if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
            game.left()
            
            
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
    
    
    textsurface = my_font.render("Fitness = "+str(game.score()), True, font_color)
    screen.blit(textsurface, (size[0]/2 - 50 , size[1] - 50))
    
    #time.sleep(0.1)
    #game.next_state()
 
    pygame.display.flip()
 
    # --- Limit to 10 frames per second
    clock.tick(30)
 
# Close the window and quit.
pygame.quit()