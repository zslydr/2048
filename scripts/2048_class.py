import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def superposition_layer(l1,l2, e1, e2, s, changed):
    for i in range(len(l1)):
        if l1[i] == 0:
            if l2[i] > 0:
                changed = True
            l1[i] = l2[i]
            l2[i] = 0
        elif l1[i] == l2[i]:
            if l1[i] > 0 and e1[i] == False and e2[i] == False:
                s = s + l1[i]*2**2
                l1[i] = l1[i]*2
                l2[i] = 0
                e1[i] = True
                changed = True
            #else:
                #l1[i] = l1[i]*2
    return(int(s), changed)

class Game_2048(object):
    
    def __init__(self,n):
        self.n = n
        self.grid = np.zeros((n,n))
        self.state = 1
        self.changed = True
        self.next_state()
        self.has_evolved = np.zeros((n,n), dtype=bool)
        self.score = 0
    
    def end(self):
        print("Game over, score: ",self.score)
        
    def next_state(self):
        #
        if self.state == 1 and self.changed == True:
            number = np.random.choice([2,4], 1, p = [0.8, 0.2])
            possible_next_position = []
            for i in range(self.n):
                for j in range(self.n):
                    if self.grid[i, j] == 0:
                        possible_next_position.append((i,j))
            if len(possible_next_position) != 0:
                ind = np.random.randint(0,len(possible_next_position))
                self.grid[possible_next_position[ind][0], possible_next_position[ind][1]] = number
            self.update_state()
        
    #def score(self):
     #   return(int(np.sum(self.grid)))
    
    def up(self):
        self.changed = False
        if self.state == 1:
            for k in range(self.n-1,0,-1):
                for i in range(k):
                    self.score, self.changed = superposition_layer(self.grid[i, :], self.grid[i+1, :], 
                                        self.has_evolved[i, :], self.has_evolved[i+1, :],
                                        self.score,
                                        self.changed)
            self.next_state()
            self.has_evolved = np.zeros((self.n,self.n), dtype=bool)
        else:
            self.end()

    
    def down(self):
        self.changed = False
        if self.state == 1:
            for k in range(self.n):
                for i in range(self.n - 1, k, -1):
                    self.score, self.changed = superposition_layer(self.grid[i, :],self.grid[i-1, :],
                                        self.has_evolved[i, :], self.has_evolved[i-1, :],
                                        self.score,
                                        self.changed)
            self.next_state()
            self.has_evolved = np.zeros((self.n,self.n), dtype=bool)
        else :
            self.end()
            
    def right(self):
        self.changed = False
        if self.state == 1:
            for k in range(self.n):
                for j in range(self.n - 1, k, -1):
                    self.score, self.changed = superposition_layer(self.grid[:, j],self.grid[:, j-1], 
                                        self.has_evolved[:, j], self.has_evolved[:, j-1], 
                                        self.score,
                                        self.changed)
            self.next_state()  
            self.has_evolved = np.zeros((self.n,self.n), dtype=bool)
        else :
            self.end()
        
    def left(self):
        self.changed = False
        if self.state == 1:
            for k in range(self.n-1,0,-1):
                for j in range(k):
                    self.score, self.changed = superposition_layer(self.grid[:, j],self.grid[:, j+1], 
                                        self.has_evolved[:, j], self.has_evolved[:, j+1], 
                                        self.score,
                                        self.changed)
            self.next_state()
            self.has_evolved = np.zeros((self.n,self.n), dtype=bool)
        else :
            self.end()
            
    def update_state(self):
        self.state = 0
        if (self.grid == 0).any():
            self.state = 1
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


