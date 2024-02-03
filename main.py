import sys

if len(sys.argv)!=4:
    print("Usage Error!")
    sys.exit(1)

nodes=sys.argv[1]
z0=sys.argv[2]
z1=sys.argv[3]
mean_time=sys.argv[4]

class Node:
    def __init__(self,nodeid,speed,cpu,coin):
        self.nodeid=nodeidid
        self.speed=spped
        self.cpu=cpu
        self.coin=coin 

slow=int(z0*n) 
fast=n-slow
low=int(z1*n)
high=n-low

for i in range(n):