import networkx as nx
import numpy as np

class Node:
    def __init__(self,nodeid,speed,cpu,balance):
        self.nodeid=nodeid
        self.speed=speed
        self.cpu=cpu
        self.balance=balance 

slow=int(z0*n) 
fast=n-slow
low=int(z1*n)
high=n-low

def generate_connected_graph(num_peers, min_connections, max_connections):
    graph = nx.barabasi_albert_graph(num_peers, m=min_connections)
    nodes = [Node(nodeid=i, speed=np.random.choice([True, False]), cpu=np.random.choice([True, False])) for i in range(num_peers)]

    # Add nodes to the graph
    graph.add_nodes_from(nodes)

    # Add edges to ensure the desired degree range
    for node in graph.nodes():
        while graph.degree[node] < min_connections:
            # Connect to random peers
            peers_to_connect = np.random.choice(list(set(graph.nodes()) - {node}), min_connections - graph.degree[node], replace=False)

            # Add edges to the graph
            for peer in peers_to_connect:
                graph.add_edge(node, peer)
                node.connections.add(peer)
                peer.connections.add(node)

    # Convert the graph to an adjacency matrix
    adjacency_matrix = nx.to_numpy_array(graph)

    return graph, adjacency_matrix



    
    
    