import networkx as nx
import random
import matplotlib.pyplot as plt


def share_data(graph, node):
    # Get neighbors of the current node
    neighbors = list(graph.neighbors(node))

    data=node.transaction_list

    # Share 'transaction' data with neighbors, excluding lists already present
    for neighbor in neighbors:
        for d in data:
            if d not in neighbor.transaction_list:
                neighbor.transaction_list.append(d) 


def propagate_data_until_convergence(graph):
    previous_data = {node: None for node in graph}

    current_data = {node: node.transaction_list.copy() for node in graph}

    while current_data != previous_data:
        previous_data = current_data.copy()

        for node in graph:
            share_data(graph, node)

        current_data = {node: node.transaction_list.copy() for node in graph}




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
                # Avoid self-loops
                if random_node != node:
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

    return graph
    

def plot_graph(graph):
    # Plot the graph
    pos = nx.spring_layout(graph)  # Adjust layout for better visualization
    node_labels = {node: node.number for node in graph.nodes()}  # Use "number" as node label
    nx.draw(graph, pos, with_labels=True, font_weight='bold', labels=node_labels)
    plt.show()