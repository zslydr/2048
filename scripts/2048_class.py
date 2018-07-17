import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def superposition_layer(l1,l2):
    l1_previous = l1
    l2_previous = l2
    for i in range(len(l1)):
        if l1[i] == 0:
            l1[i] = l2[i]
            l2[i] = 0
        elif l1[i] == l2[i]:
            l1[i] = l1[i]*2
            l2[i] = 0
    
    return(l1,l2)

class Game_2048(object):
    
    def __init__(self,n):
        self.n = n
        self.grid = np.repeat(np.zeros(n),n).reshape((n,n))
        self.next_state()
        self.state = 1
    
    def end(self):
        print("Game over, score: ",self.score())
        
    def next_state(self):
        number = np.random.choice([2,4], 1, p = [0.8, 0.2])
        possible_next_position = []
        for i in range(self.n):
            for j in range(self.n):
                if self.grid[i, j] == 0:
                    possible_next_position.append((i,j))
        if len(possible_next_position) != 0:
            ind = np.random.randint(0,len(possible_next_position))
            self.grid[possible_next_position[ind][0], possible_next_position[ind][1]] = number
        
    def score(self):
        return(int(np.sum(self.grid)))
    
    def up(self):
        if self.state == 1:
            for k in range(self.n-1,0,-1):
                for i in range(k):
                    superposition_layer(self.grid[i, :],self.grid[i+1, :])
            self.next_state()
            self.update_state()
        else:
            self.end()

    
    def down(self):
        if self.state == 1:
            for k in range(self.n):
                for i in range(self.n - 1, k, -1):
                    superposition_layer(self.grid[i, :],self.grid[i-1, :])
                    
            self.next_state()
            self.update_state()
        else :
            self.end()
            
    def right(self):
        if self.state == 1:
            for k in range(self.n):
                for j in range(self.n - 1, k, -1):
                    superposition_layer(self.grid[:, j],self.grid[:, j-1])
                    
            self.next_state()
            self.update_state()
        else :
            self.end()
        
    def left(self):
        if self.state == 1:
            for k in range(self.n-1,0,-1):
                for j in range(k):
                    superposition_layer(self.grid[:, j],self.grid[:, j+1])
                    
            self.next_state()
            self.update_state()
        else :
            self.end()
            
    def update_state(self):
        self.state = 0
        if (self.grid == 0).any():
            self.state =1
            return(None)
        
        for i in range(self.n):
            for j in range(self.n):
                for k in range(3):
                    for p in range(3):
                        if abs(k-1) != abs(p-1):
                            if i+k-1 >= 0 and i+k-1 <= 3 and j+p-1 >= 0 and j+p-1 <= 3:
                                #print(i+k-1,j+p-1)
                                if self.grid[i, j] == self.grid[i+k-1, j+p-1]:
                                    self.state = 1
                                    break

            
    def display(self):
        #fig, ax = plt.subplots()
        sns.heatmap(self.grid, annot=True, linewidths=.5, cbar=False)
        plt.tick_params(
                which='both', 
                bottom=False, 
                left = False,
                labelleft = False,
                labelbottom=False)
        plt.show()


