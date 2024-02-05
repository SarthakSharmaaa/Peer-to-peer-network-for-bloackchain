from node import CreateNodes,Node
from graph import gen_graph
import random
import numpy as np



#get the input of number of nodes in n, z0, z1,Tx
n=int(input("Enter the number of nodes to be created : "))
z0=int(input("Enter z0 : "))
z1=int(input("Enter z1 : "))
t=int(input("Enter Tx : "))

exponential_dist = np.random.exponential(scale=t, size=100)

nodes_list = CreateNodes(n,z0,z1)

for i in range(20):
    gen=random.randint(1,100) #with 100 discrete points
    gen1=random.randint(0,n-1) #transaction creating node
    gen2=random.randint(0,n-1)  #transaction recieving node

    amount=random.randint(500,600) #amount spent

    nodes_list[gen1].transaction(gen2,amount,gen)

gen_graph(nodes_list)


