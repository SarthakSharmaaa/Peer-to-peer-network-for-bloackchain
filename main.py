from node import CreateNodes,Node
from graph import gen_graph, propagate_data_until_convergence
import random
import numpy as np
import threading



# #get the input of number of nodes in n, z0, z1,Tx
# n=int(input("Enter the number of nodes to be created : "))
# z0=int(input("Enter z0 : "))
# z1=int(input("Enter z1 : "))
# t=int(input("Enter Tx : "))

n=20
z0=40
z1=60
t=2

exponential_dist = np.random.exponential(scale=t, size=100)
exponential_dist = np.round(exponential_dist, decimals=1) * 10


nodes_list = CreateNodes(n,z0,z1)

for i in range(20):
    gen=random.randint(0,99) #with 100 discrete points
    gen1=random.randint(0,n-1) #transaction creating node
    gen2=random.randint(0,n-1)  #transaction recieving node

    amount=random.randint(500,600) #amount spent

    nodes_list[gen1].transaction(gen2,amount,exponential_dist[gen])

fin_graph=gen_graph(nodes_list)

propagate_data_until_convergence(fin_graph)

for node in fin_graph.nodes():
    print(len(node.transaction_list))


