#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 22:38:07 2018

@author: Raphael
"""

import os
import importlib
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import normalize
os.chdir('/Users/Raphael/Github/2048/scripts/') #Select your working directory
cwd = os.getcwd()
G_2048=importlib.import_module("2048_class")
G_2048=importlib.reload(G_2048)
NN=importlib.import_module("NN_class")
NN=importlib.reload(NN)

#%% 

# SCORE FUNCTION BASED ON THE WEIGHTS OF THE NN
def score_weight(game, model, W):
    # Indicate if the game is stuck (because NN can loop over a useless move without the game being lost)
    stuck = False 
    s = 0
    while game.state == 1 and stuck == False: # While the game is not lost and not stuck
        stuck = True
        previous_grid = game.grid # to test whether the game is stuck or not
        previous_score = game.score()
        p = model.forward(game.grid.reshape(16),W) # Forward propagation with the grid as input
        action_ind = p.argmax() # Get the action index to perform
        action = [game.up,game.down,game.right,game.left][action_ind] # Select the action to perform
        action() # Perform the action
        if (previous_grid != game.grid).any() or (game.grid == 0).any(): #Check if the game is not stuck
            stuck = False
        s = s + game.score() - previous_score
    return(s)

# FUNCTION TO BREED TWO  NEURAL NETWORK WEIGHTS
def breed(W1, W2, nb_children):
    children = []
    for i in range(nb_children):
        child_W = []
        for w1,w2 in zip(W1,W2):
            child_w = np.array([])
            for x,y in zip(w1.reshape(np.product(w1.shape)),w2.reshape(np.product(w2.shape))):
                if np.random.uniform() > .5:
                    child_w = np.append(child_w,x)
                else:
                    child_w = np.append(child_w,y)
            child_w = child_w.reshape(w1.shape)
            child_W.append(child_w)
        children.append(child_W)
    return(children)

# FUNCTION TO PERFORM A MUTATION TO A NEURAL NETWORK WEIGHT
def mutation(W, sigma, mu):
    new_W = []
    for w in W:
        new_w = np.array([])
        for x in w.reshape(np.product(w.shape)):
            if np.random.uniform() < .1:
                #new_w = np.append(new_w, sigma * np.random.randn() + mu)
                new_w = np.append(new_w, 0)
            else:
                new_w = np.append(new_w, x)
        new_w = new_w.reshape(w.shape)
        new_W.append(new_w)
    return(new_W)



def redef_score(value, max_):
    return(np.exp(1 / (0.3 + max_ - value)))

def proba_pick(value, total):
    return( value / total)

def sigmoid(s):
    return(1. / (1 + np.exp(-s)))




#%%
# EXEMPLE SUR UNE GENERATION
game = G_2048.Game_2048(4) # Initialize the game grid


model = NN.NNet(16,4,1,(16,)) # Initialize the type of the NN (or population in our case)
W = []
s = model.input_size
for size in model.hidden_sizes:
    W.append(np.random.randn(s, size))
    s = size

W.append(np.random.randn(model.hidden_sizes[-1], model.output_size))


score = score_weight(game, model, W) # SCORE of the inidividual
print(score)
game.display()

#%%
model = NN.NNet(16,4,2,(16,))
sigma = 100
mu = 0
n_pop = 50
n_generations = 100
population = {}
res_generation = []

for i in range(n_pop):
    population[i] = {}
    W = []
    s = model.input_size
    for size in model.hidden_sizes:
        W.append(sigma * np.random.randn(s, size) + mu)
        s = size
    W.append(sigma * np.random.randn(model.hidden_sizes[-1], model.output_size) + mu)

    population[i]['weight'] = W


for generations in range(n_generations):
    
    for i in range(n_pop):
        game = G_2048.Game_2048(4)
        population[i]['score'] = score_weight(game, model, population[i]['weight'])
    
    df = pd.DataFrame.from_dict(population, orient = 'index')
    
    df = df.sort_values(by = "score", ascending = False)
    
    #df["rank"] = [x for x in range(df.shape[0])]
    #df["redef_rank"] = np.exp(-df["rank"])
    #df["redef_score"] = df.score.apply(lambda x : sigmoid(x))
    #df["normalized_score"] = np.exp(normalize(df.score.astype(float).values.reshape(1, -1))[0])
    #df["proba_pick"] = df.normalized_score.apply(lambda x : proba_pick(x,df.normalized_score.sum()))
    
    print("génération ", generations, "average score: ", df.score.mean())
    res_generation.append(df.score.mean())
    
    n_best = 10
    n_lucky = 0
    
    breeders_ind = [x for x in range(n_best)]
    breeders_ind.extend(np.random.choice(range(n_best,n_pop), n_lucky, replace = False))
    
    breeders = df.iloc[breeders_ind].index.values
    population = {}
    for i in range(int(n_pop/2)):
        parents = np.random.choice(breeders, 2, replace = False)
        #parents = np.random.choice(df.index.values, 2, replace = False, p = df["proba_pick"])
        #print(df.loc[parents[0]]["rank"], df.loc[parents[1]]["rank"])
        children = breed(df.loc[parents[0]]["weight"], df.loc[parents[1]]["weight"], 2)
        for j,child in enumerate(children):
            population[2*i+j] = {}
            population[2*i+j]["weight"] = mutation(child, sigma, mu)

#%%
for i in range(n_pop):
    game = G_2048.Game_2048(4)
    population[i]['score'] = score_weight(game, model, population[i]['weight'])
df = pd.DataFrame.from_dict(population, orient = 'index')
df = df.sort_values(by = "score", ascending = False)
print("génération ", generations, "average score: ", df.score.mean())
res_generation.append(df.score.mean())
#%%
sns.set(style="whitegrid")
sns.tsplot(res_generation)