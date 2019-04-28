# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 16:17:23 2019

@author: andre
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 22:29:30 2019

@author: andre
"""

# Starting point for program to build and draw a maze
# Modify program using disjoint set forest to ensure there is exactly one
# simple path joiniung any two cells
# Programmed by Olac Fuentes
# Last modified March 28, 2019

import matplotlib.pyplot as plt
import numpy as np
import random
from dsf import *
import time

def draw_maze(walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    for w in walls:
        if w[1]-w[0] ==1: #vertical wall
            x0 = (w[1]%maze_cols)
            x1 = x0
            y0 = (w[1]//maze_cols)
            y1 = y0+1
        else:#horizontal wall
            x0 = (w[0]%maze_cols)
            x1 = x0+1
            y0 = (w[1]//maze_cols)
            y1 = y0  
        ax.plot([x0,x1],[y0,y1],linewidth=1,color='k')
    sx = maze_cols
    sy = maze_rows
    ax.plot([0,0,sx,sx,0],[0,sy,sy,0,0],linewidth=2,color='k')
    if cell_nums:
        for r in range(maze_rows):
            for c in range(maze_cols):
                cell = c + r*maze_cols   
                ax.text((c+.5),(r+.5), str(cell), size=10,
                        ha="center", va="center")
    ax.axis('off') 
    ax.set_aspect(1.0)

def wall_list(maze_rows, maze_cols):
    # Creates a list with all the walls in the maze
    w =[]
    for r in range(maze_rows):
        for c in range(maze_cols):
            cell = c + r*maze_cols
            if c!=maze_cols-1: #If not last column
                w.append([cell,cell+1]) # wall between adjacent columns
            if r!=maze_rows-1: #if not last row
                w.append([cell,cell+maze_cols]) # wall between adjacent rows
    return w



def Maze_normal(r,c,S,W,m):
    i = 0
    EL = []
    while i < m:
        d = random.randint(0,len(W)-1) #random index
        if find(S,W[d][0]) != find(S,W[d][1]): #If the roots are different,
            union(S,W[d][0],W[d][1]) #Join the sets,
            EL.append(W.pop(d)) #Delete wall
            i += 1
    
    if m < (r*c) - 1:
        print(" A path from source to destination is not guaranteed to exist")
    elif m == (r*c) - 1:
        print("The is a unique path from source to destination")
    else:
        print("There is at least one path from source to destination")
        
    return EL


def Maze_C(r,c,S,W):
    while num_of_sets(S) > 1:
        d = random.randint(0,len(W)-1) #random index
        if find_c(S,W[d][0]) != find_c(S,W[d][1]): #Use path compression
            union_by_size(S,W[d][0],W[d][1]) #and union by size
            W.pop(d)



def EdgeList_to_AdjList(EL, size):     
    AL = []          
    for i in range(size):
        AL.append([])    

    for i in range(len(EL)):
        AL[EL[i][0]].append(EL[i][1])
        AL[EL[i][1]].append(EL[i][0])
    
    return AL


plt.close("all") 



r = 2 #Define number of rows
c = r #Define number of columns


print("There are ", r*c, " cells" )
m = int(input("Please enter m\n"))

W = wall_list(r,c)
S = DisjointSetForest(r * c)   




start = time.time()

Edge_List = Maze_normal(r,c,S,W,m)
AL = EdgeList_to_AdjList(Edge_List, r*c)
print(AL)
draw_graph(AL)


end = time.time()

#print("Using using standard union and no compression - Time: ", end - start)


draw_maze(W,r,c) 




















