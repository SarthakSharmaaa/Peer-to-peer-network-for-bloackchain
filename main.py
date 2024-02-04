from node import CreateNodes,node

#get the input of number of nodes in n, z0, z1
n=input("Enter the number of nodes to be created : ")
z0=input("Enter z0 : ")
z1=input("Enter z1 : ")

nodes_list = CreateNodes(n,z0,z1)

for i in nodes_list:
    print(i.number,i.speed,i.cpu)
