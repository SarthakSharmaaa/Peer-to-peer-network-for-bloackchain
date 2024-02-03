import sys
import networkx as nx
import numpy as np

if len(sys.argv)!=4:
    print("Usage Error!")
    sys.exit(1)

nodes=sys.argv[1]
z0=sys.argv[2]
z1=sys.argv[3]
mean_time=sys.argv[4]
