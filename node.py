import networkx as nx
import numpy as np
import random

class Node:
    def __init__(self, nodeid, speed, cpu, balance):
        self.nodeid = nodeid
        self.speed = speed
        self.cpu = cpu
        self.balance = balance 
        self.connections = set()

def generate_nodes(n, z0, z1):
    nodes_list = [Node(nodeid=i, speed=None, cpu=None, balance=random.randint(0, 10)) for i in range(n)]
    slow = int(z0 * n)
    fast = n - slow
    low = int(z1 * n)
    high = n - low

    random.shuffle(nodes_list)
    for i in range(slow):
        nodes_list[i].speed = 0
    for i in range(slow, n):
        nodes_list[i].speed = 1

    random.shuffle(nodes_list)
    for i in range(low):
        nodes_list[i].cpu = 0
    for i in range(low, n):
        nodes_list[i].cpu = 1

    return nodes_list

def generate_connected_graph(n, min_connections, max_connections, z0, z1):
    graph = nx.barabasi_albert_graph(n, m=min_connections)

    nodes_list = generate_nodes(n, z0, z1)
    for node in nodes_list:
        graph.nodes[node.nodeid]['connections'] = node.connections
    for node in graph.nodes():
        while graph.degree[node] < min_connections:
            peers_to_connect = np.random.choice(list(set(graph.nodes()) - {node}), min_connections - graph.degree[node], replace=False)
            for peer in peers_to_connect:
                graph.add_edge(node, peer)
                graph.nodes[node]['connections'].add(peer)
                graph.nodes[peer]['connections'].add(node)
    adjacency_matrix = nx.to_numpy_array(graph)
    return graph, adjacency_matrix

n = 10
min_connections = 3
max_connections = 6
z0 = 0.7
z1 = 0.4

generated_graph, adjacency_matrix = generate_connected_graph(n, min_connections, max_connections, z0, z1)
print("Adjacency Matrix:")
print(adjacency_matrix)
