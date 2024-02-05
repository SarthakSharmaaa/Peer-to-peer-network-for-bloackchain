import networkx as nx
import random
import matplotlib.pyplot as plt

def gen_graph(node_objects):
    # Create an undirected graph
    graph = nx.Graph()

    # Add nodes to the graph
    graph.add_nodes_from(node_objects)

    # Connect nodes based on the desired connectivity constraints
    for i, node in enumerate(node_objects):
        # Calculate the current degree of the node
        current_degree = graph.degree(node)

        # Connect the node to ensure minimum 3 connectivity
        while current_degree < 3:
            # Choose a random node from the remaining nodes
            remaining_nodes = set(node_objects) - set(graph.neighbors(node))
            if remaining_nodes:
                random_node = random.choice(list(remaining_nodes))
                graph.add_edge(node, random_node)
                current_degree += 1
            else:
                break  # No remaining nodes to connect

        # Limit the degree to a maximum of 6 connectivity
        while current_degree > 6:
            # Choose a random neighbor and remove the edge
            neighbor = random.choice(list(graph.neighbors(node)))
            graph.remove_edge(node, neighbor)
            current_degree -= 1

    # Plot the graph
    pos = nx.spring_layout(graph)  # Adjust layout for better visualization
    nx.draw(graph, pos, with_labels=True, font_weight='bold')
    plt.show()
