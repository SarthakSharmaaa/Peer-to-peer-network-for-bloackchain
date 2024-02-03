import random

def linkspeedmatrix(n,adjacency_matrix):
    cij = [[0 for i in range(n)] for j in range(n)]

    for i in range(n):
        for j in range(n):
            if nodes[i].speed and nodes[j].speed and adjacency_matrix[i][j]==1:
                cij[i, j] = 100  
            elif (not nodes[i].speed or not nodes[j].speed) and adjacency_matrix[i][j]==1:
                cij[i, j] = 5   
    return cij

def speedoflightpropagationdelay(n,adjacency_matrix):
    pij = [[0 for i in range(n)] for j in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j and adjacency_matrix[i][j]==1:
                pij[i, j] = random.uniform(0.01, 0.5)
    
    return pij

    