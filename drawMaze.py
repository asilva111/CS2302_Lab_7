'''
Created on Thu April 25 15:16:21 2019
CS 2302 - Andres Silva
> Teacher: Olac Fuentes
> TAs: Anindita Nath  & Maliheh Zargaran
> Lab #7
> Create a maze of nxn size and plot a solution using graph implementations.
> LAST MODIFIED: APRIL 28th, 2019
'''

import matplotlib.pyplot as plt
import numpy as np
import random
from dsf import *
import time

def draw_maze(EL,walls,maze_rows,maze_cols,cell_nums=False):
    fig, ax = plt.subplots()
    
    #Plot line from edge list 'EL'
    for l in EL:
        if l[1]-l[0] != 1: #vertical wall
            lx0 = (l[1]%maze_cols) +.5
            lx1 = lx0
            ly0 = (l[1]//maze_cols) -.5
            ly1 = ly0+1
        else:#horizontal wall
            lx0 = (l[0]%maze_cols) +.5
            lx1 = lx0+1
            ly0 = (l[1]//maze_cols) +.5
            ly1 = ly0  
        ax.plot([lx0,lx1],[ly0,ly1],linewidth=1,color='r') 
    
    
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
                ax.text((c+.5),(r+.5), str(cell), size = 10,
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
    while i < m and i != (r*c)-1:
        d = random.randint(0,len(W)-1) #random index
        if find(S,W[d][0]) != find(S,W[d][1]): #If the roots are different,
            union(S,W[d][0],W[d][1]) #Join the sets,
            EL.append(W.pop(d)) #Delete wall
            i += 1
    
    if i == (r*c)-1: #Handling the infinite loop, delete as many walls as possible, disregarding the DSF
        while i < m or i <= len(W):
            d = random.randint(0,len(W)-1) #random index
            union(S,W[d][0],W[d][1]) #Join the sets,
            EL.append(W.pop(d)) #Delete wall
            i += 1
      
    return EL


def EdgeList_to_AdjList(EL, size):     
    AL = []          
    for i in range(size):
        AL.append([])    

    for i in range(len(EL)):
        AL[EL[i][0]].append(EL[i][1])
        AL[EL[i][1]].append(EL[i][0])
    
    return AL


def BFS(AL,s):
    prev = np.zeros(len(AL), dtype = int)-1 #Initialize the prev array
    visited = [False] * len(AL) #Keep track of the visited nodes
    Q = [] #Create Queue
    
    Q.append(AL[0][0]) #Append source to Queue and mark it as visited
    visited[AL[0][0]] = True
    
    while Q:
        if prev[-1] >= 0: #If last node visited, loop is finished
            break
        
        s = Q.pop(0) #Get next element in Queue 
        
        for i in AL[s]: #For all adjacent vertex to current node,
            if visited[i] == False: #Mark it as visited
                visited[i] = True
                prev[i] = s #Mark the prev array at the neightboor location as s
                Q.append(i) #Enqueue the neightboor for future visit
           
    prev[0] = -1 #Make the source node the root.

    return prev #Return prev array


def DFS(AL,s):
    prev = np.zeros(len(AL), dtype=int)-1 #Initialize prev array 
    visited = [False] * len(AL)  #Initialize visited array
    Stack = [] #Create stack
    
    Stack.append(AL[0][0]) #Push source node and mark it as visited
    visited[AL[0][0]] = True
    
    while Stack:
        if prev[-1] >= 0: # Break loop at last vertex
            break
        s = Stack.pop() #retrieve next node to be visited
        for i in AL[s]:
            if visited[i] == False: #When visiting the neightboor, mark it as true
                visited[i] = True
                prev[i] = s #Keep track in the prev array
                Stack.append(i) #Push neightboor
        
        if Stack == []:
            S.append(AL[0][1])
    
    return prev


def prev_to_EL(prev):
    EL = [] #Create edge list
    
    i = len(prev)-1 #Start from last node
    while prev[i] >= 0: #While not reaching the end
        if i < prev[i]: #Decide direction of line
            edge = [i,prev[i]] #Create an edge form current index to prev[i]
        else:
            edge = [prev[i],i]
        
        i = prev[i] #Update index to content of array
        EL.append(edge) #append to edge list
    
    EL.append([0,i]) #Finally, create a node with 0 to last known index
    
    return EL
    


"""
MAIN __________________________________________________________________________
"""
def main():
    
    r = int(input("Please enter number of rows for the square maze\n"))
    c = r
    
    print("There are ", r*c, " cells", " and ", (r*c*2)," walls.")
    
    m = int(input("Please enter walls to be removed\n"))
        
    if m < (r*c) - 1:
        print("A path from source to destination is not guaranteed to exist, terminating program...")
        return
    
    elif m == (r*c) - 1:
        print("There is a unique path from source to destination")
    
    else:
        print("There is at least one path from source to destination")

    selection  = input("Please select method to find path:     BSF/DFS\n")
    
    

    W = wall_list(r,c)
    S = DisjointSetForest(r * c)   
    
    Edge_List = Maze_normal(r,c,S,W,m)
    
    AL = EdgeList_to_AdjList(Edge_List, r*c)
    
    if selection == "BSF":
        start = time.time()
        
        prev = BFS(AL,0)
        path = prev_to_EL(prev)
        
        end = time.time()
        print(end - start)

    
    elif selection == "DFS":
        start = time.time()
        
        prev = DFS(AL,0)
        path = prev_to_EL(prev)
        
        end = time.time()
        print(end - start)
        
    else:
        print("Invalid input, exiting..")
        return
        
    
    draw_maze(path,W,r,c) 



main()











#plt.close("all") 




