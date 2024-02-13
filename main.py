from node import CreateNodes,Node,StopNodes
from graph import gen_graph, propagate_data_until_convergence,plot_graph
import random
import numpy as np
import threading
import time



def uniform_dist_time(num):
    gen=random.randint(0,99) #with 100 discrete points
    uniform_distribution = np.random.uniform(10, 500, size=100)  # Generating 100 random numbers
    return uniform_distribution[gen]
    

def exp_distribution(t):
    gen=random.randint(0,99) #with 100 discrete points
    exponential_dist = np.random.exponential(scale=t, size=100)
    exponential_dist = np.round(exponential_dist, decimals=1) #randomly generating transaction time

    return exponential_dist[gen]

# #get the input of number of nodes in n, z0, z1,Tx
# n=int(input("Enter the number of nodes to be created : "))
# z0=int(input("Enter z0 : "))
# z1=int(input("Enter z1 : "))
# t=int(input("Enter Tx : "))
# num=int(input("Choose a number from a uniform distribution :"))
n=5
z0=40
z1=60
t=2


nodes_list = CreateNodes(n,z0,z1)
fin_graph=gen_graph(nodes_list)


#generate transactions at random time
for i in range(20):
    
    gen1=random.randint(0,n-1) #transaction creating node
    gen2=random.randint(0,n-1)  #transaction recieving node

    amount=random.randint(500,600) #amount spent

    #nodes_list[gen1].transaction(gen2,amount,exponential_dist[gen])
    
    th = threading.Thread(target=nodes_list[gen1].thread_handler , args=(gen2,amount) )

    th.start()
    time_between_transactions=exp_distribution(t)
    print("transaction ", i+1, " generated and sleeping for ", time_between_transactions)
    time.sleep(time_between_transactions)
    th.join(timeout=1)

StopNodes(nodes_list)

propagate_data_until_convergence(fin_graph)


for i in fin_graph:
    print(len(i.transaction_list))







