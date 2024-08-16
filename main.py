from node import CreateNodes,Node,StopNodes,CreateBlocks,StopBlockCreation,Print_chain,StopCheckList,handleList
from graph import gen_graph, propagate_data_until_convergence,propagate_data_until_convergence_block,plot_graph
import random
import numpy as np
import time


def uniform_dist_time(num):
    gen=random.randint(0,99) #with 100 discrete points
    uniform_distribution = np.random.uniform(0.01, 0.5, size=100)  # Generating 100 random numbers
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
# num=int(input("Choose a number from a uniform distribution :"))\
# interarival_block = int(input("Enter interarival time : "))
n=10
z0=50
z1=50
t=1
blockInterval=2
pij=uniform_dist_time(5)

print("simulating please wait")
nodes_list = CreateNodes(n,z0,z1,pij)

StopNodes(nodes_list)
fin_graph=gen_graph(nodes_list)
propagate_data_until_convergence(fin_graph)

CreateBlocks(fin_graph)
time.sleep(5)

StopBlockCreation(fin_graph)
time.sleep(5)

propagate_data_until_convergence_block(fin_graph)

time.sleep(5)

handleList(fin_graph)


StopCheckList(fin_graph)

for i in fin_graph:
    print("total no. of blocks in " , i.number ," is ",len(i.block_chain))
    print("no. of valid transactions in a node", i.number ," is " , len(i.transaction_list))
    print("end of node")

plot_graph(fin_graph)

print("the end")

# list_num=1
# l=[]
# for i in fin_graph:
#     count = 0
#     id=i.longest_chain
#     while id!=i.genesis.blockID:
#             count+=1
#             x=id + " " + str(i.block_chain[id].create_time_stamp)
#             l.append(x)
#             id=i.block_chain[id].parent
#     with open('my_list' + str(list_num) + '.txt', 'w') as file:
#         for item in l:
#             file.write(str(item) + '\n')
#     l.clear()
#     list_num+=1







