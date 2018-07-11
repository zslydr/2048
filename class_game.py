import numpy as np

def superposition_layer(l1,l2):
    for i in range(len(l1)):
        if l1[i] == 0:
            l1[i] = l2[i]
            l2[i] = 0
        elif l1[i] == l2[i]:
            l1[i] = l1[i]*2
            l2[i] = 0
    return(l1,l2)


#%%

class Game_2048:
    
    def __init__(self,n):
        self.n = n
        self.grid = np.repeat(np.zeros(n),n).reshape((n,n))
        self.next_state()
        self.state = 1
    
    def end(self):
        print("Game over, score: ",self.score())
        
    def next_state(self):
        number = np.random.randint(1,3)*2
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
        for i in range(self.n-1,0,-1):
            self.grid[i-1,:],self.grid[i,:] = superposition_layer(self.grid[i-1, :],self.grid[i, :])
    
    def down(self):
        for i in range(self.n-1):
            self.grid[i+1][:],self.grid[i, :] = superposition_layer(self.grid[i+1, :],self.grid[i, :])
            
    def right(self):
        for j in range(self.n-1):
            self.grid[:, j+1],self.grid[:, j] = superposition_layer(self.grid[:, j+1],self.grid[:, j])
        
    def left(self):
        for j in range(self.n-1,0,-1):
            self.grid[:, j-1],self.grid[:, j] = superposition_layer(self.grid[:, j-1],self.grid[:, j])
            
    def update_state(self):
        self.state = 0
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
    
    def update(self, mouv):
        if self.state == 1:
            mouv()
            self.next_state()
            self.update_state()
        else :
            self.end()
                                
    


#%% EXAMPLE

g = Game_2048(4)
print(g.grid)
nb_coups = 0
while g.state == 1:
    p = [g.up,g.down,g.right,g.left][np.random.randint(0,4)]
    #p = [g.up,g.down,g.right,g.left][nb_coups%4]
    g.update(p)
    nb_coups += 1
    
print("Game over, score: ",g.score())
print("nombre de coups: ",nb_coups)
print(g.grid)



