from node import CreateNodes,Node,StopNodes
from graph import gen_graph, propagate_data_until_convergence,plot_graph
import random
import numpy as np
import threading
import time



# #get the input of number of nodes in n, z0, z1,Tx
# n=int(input("Enter the number of nodes to be created : "))
# z0=int(input("Enter z0 : "))
# z1=int(input("Enter z1 : "))
# t=int(input("Enter Tx : "))

n=5
z0=40
z1=60
t=2

exponential_dist = np.random.exponential(scale=t, size=100)
exponential_dist = np.round(exponential_dist, decimals=1) #randomly generating transaction time


nodes_list = CreateNodes(n,z0,z1)
fin_graph=gen_graph(nodes_list)


#generate transactions at random time
for i in range(20):
    gen=random.randint(0,99) #with 100 discrete points
    gen1=random.randint(0,n-1) #transaction creating node
    gen2=random.randint(0,n-1)  #transaction recieving node

    amount=random.randint(500,600) #amount spent

    #nodes_list[gen1].transaction(gen2,amount,exponential_dist[gen])
    
    t = threading.Thread(target=nodes_list[gen1].thread_handler , args=(gen2,amount) )

    t.start()
    print("transaction ", i+1, " generated and sleeping for ", exponential_dist[gen])
    time.sleep(exponential_dist[gen])
    t.join(timeout=1)
    print("main thread joined")

StopNodes(nodes_list)

propagate_data_until_convergence(fin_graph)







for i in fin_graph:
    print(i.transaction_list)






