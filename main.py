from node import CreateNodes,Node,StopNodes
from graph import gen_graph, propagate_data_until_convergence,plot_graph
import random
import numpy as np
import threading
import time
import asyncio

def uniform_dist_time(num):
    gen=random.randint(0,99) #with 100 discrete points
    uniform_distribution = np.random.uniform(10, 500, size=100)  # Generating 100 random numbers
    return uniform_distribution[gen]
    

def exp_distribution(t):
    gen=random.randint(0,99) #with 100 discrete points
    exponential_dist = np.random.exponential(scale=t, size=100)
    exponential_dist = np.round(exponential_dist, decimals=1) #randomly generating transaction time

    return exponential_dist[gen]

def interarrival_blocks(n,z1,blockInterval):
    fast=int(z1*n/100)
    slow=n-fast
    slowInterarrival=blockInterval*(9*fast+slow)
    fastInterarrival=blockInterval*(9*fast+slow)/10
    return slowInterarrival,fastInterarrival


# #get the input of number of nodes in n, z0, z1,Tx
# n=int(input("Enter the number of nodes to be created : "))
# z0=int(input("Enter z0 : "))
# z1=int(input("Enter z1 : "))
# t=int(input("Enter Tx : "))
# num=int(input("Choose a number from a uniform distribution :"))
n=20
z0=40
z1=60
t=1

nodes_list = CreateNodes(n,z0,z1)
StopNodes(nodes_list)
fin_graph=gen_graph(nodes_list)
#propagate_data_until_convergence(fin_graph)

for i in fin_graph:
    print(len(i.transaction_list))







