#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 14 18:02:57 2018

@author: Raphael
"""

import os
import neat
import importlib
import numpy as np
os.chdir('/Users/Raphael/Github/2048/scripts') #Select your working directory

G_2048=importlib.import_module("2048_class")
G_2048=importlib.reload(G_2048)
cwd = os.getcwd()

#%%

def score_weight(game, net):
    # Indicate if the game is stuck (because NN can loop over a useless move without the game being lost)
    stuck = False 
    s = 0
    while game.state == 1 and stuck == False: # While the game is not lost and not stuck
        stuck = True
        previous_grid = game.grid # to test whether the game is stuck or not
        p = net.activate(game.grid.reshape(16))
        action_ind = np.array(p).argmax() # Get the action index to perform
        action = [game.up,game.down,game.right,game.left][action_ind] # Select the action to perform
        action() # Perform the action
        if (previous_grid != game.grid).any() or (game.grid == 0).any(): #Check if the game is not stuck
            stuck = False
    s = game.score()
    if stuck and game.state == 1:
        s = s - s/2
    return(s)
#%%
def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        game = G_2048.Game_2048(4)
        genome.fitness = 4.0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = score_weight(game, net)
        
def run(config_file):
    # Load configuration.
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 300)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
    return(winner)

#%%

winner = run("config-feedforward.txt")

#%%


