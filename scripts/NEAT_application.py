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

visualize = importlib.import_module("visualize")
visualize=importlib.reload(visualize)
cwd = os.getcwd()

def score_weight(game, net):
    # Indicate if the game is stuck (because NN can loop over a useless move without the game being lost)
    stuck = False 
    penality = 0
    bad_move_cmpt = 0
    while game.state == 1 and stuck == False: # While the game is not lost and not stuck
        stuck = True
        p = net.activate(np.append(game.grid, [bad_move_cmpt**2, np.count_nonzero(game.grid)])) #
        action_ind = np.array(p).argmax() # Get the action index to perform
        action = [game.up,game.down,game.right,game.left][action_ind] # Select the action to perform
        action() # Perform the action
        if game.changed: #Check if the game is not stuck
            bad_move_cmpt = 0
            stuck = False
        if stuck == True:
            bad_move_cmpt += 1
            if bad_move_cmpt < 20:
                stuck = False
        #print(game.n**2 - np.count_nonzero(game.grid))
        penality += bad_move_cmpt * np.floor(np.log(1 + game.score))
        penality += - (game.n**2 - np.count_nonzero(game.grid)) * game.score * 0.01
    return(game.score - penality)

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
    #p.add_reporter(neat.Checkpointer(5))

    
    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 1000)


    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))
    return(winner)

#%%

winner = run("config-feedforward.txt")

#%%
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     "config-feedforward.txt")
node_names = {0:'up', 1: 'down', 2:'right', 3 : 'left'}
    
visualize.draw_net(config, winner, True, node_names = node_names)
#visualize.plot_stats(stats, ylog=False, view=True)
#visualize.plot_species(stats, view=True)
#%%
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     "config-feedforward.txt")

import pickle
with open('genome.pickle', 'wb') as f:
    pickle.dump(winner, f, protocol=pickle.HIGHEST_PROTOCOL)
