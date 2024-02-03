import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class Peer:
    def __init__(self, peer_id):
        self.peer_id = peer_id
        self.connections = set()

# Function to generate a connected graph with random connections
def generate_connected_graph(num_peers, min_connections, max_connections):
    graph = nx.barabasi_albert_graph(num_peers, m=min_connections)
    nodes = [Peer(peer_id=i) for i in range(num_peers)]
    graph = nx.Graph()

    # Add nodes
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

    return graph

# Simulation parameters
num_peers = 10
min_connections = 3
max_connections = 6

# Generate a connected graph with random connections
graph = generate_connected_graph(num_peers, min_connections, max_connections)

# Visualize the graph
pos = nx.spring_layout(graph)  # Layout for visualization
nx.draw(graph, pos, with_labels=True, font_weight='bold', node_color='skyblue', edge_color='gray')
plt.show()
