import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

class Peer:
    def __init__(self, peer_id):
        self.peer_id = peer_id
        self.connections = set()

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

    # Convert the graph to an adjacency matrix
    adjacency_matrix = nx.to_numpy_array(graph)

    return graph, adjacency_matrix

# Example usage:
num_peers = 10
min_connections = 3
max_connections = 6

generated_graph, adjacency_matrix = generate_connected_graph(num_peers, min_connections, max_connections)

# Print the graph visualization
print("\nAdjacency Matrix:")
print(adjacency_matrix)
pos = nx.spring_layout(generated_graph)
nx.draw(generated_graph, pos, with_labels=True, font_weight='bold', node_color='skyblue', node_size=800, font_size=10)
plt.title("Generated Graph Visualization")
plt.show()


