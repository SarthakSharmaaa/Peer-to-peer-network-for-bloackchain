import networkx as nx
import random
import matplotlib.pyplot as plt
import time
import numpy as np


def random_time(t):
    exponential_dist = np.random.exponential(scale=t, size=100)
    exponential_dist = np.round(exponential_dist, decimals=1) #randomly generating transaction time
    gen=random.randint(0,99)
    return exponential_dist[gen]


def simulate_latency(node,neighbor):
    #ρij + |m|/cij + dij
    p=5
    m=10
    c=0
    if node.speed == "fast" and neighbor.speed=="fast":
        c=100
    else:
        c=5
    d=random_time(96/c)
    time_to_sleep=p+(m/c)+d
    return 1

def share_data(graph, node):
    # Get neighbors of the current node
    neighbors = list(graph.neighbors(node))

    data=node.transaction_list

    # Share 'transaction' data with neighbors, excluding lists already present
    for neighbor in neighbors:
        for d in data:
            if d not in neighbor.transaction_list:
                time.sleep(simulate_latency(node,neighbor))
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



def plot_graph(G):

    # Plot the undirected graph without edge labels
    pos = nx.spring_layout(G)  # Define the layout of the graph
    node_labels = {node: node.number for node in G.nodes()}  # Use "number" as node label
    nx.draw(G, pos, with_labels=False, node_size=500, node_color='skyblue', edge_color='gray')  # Draw nodes without labels
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=12, font_color='black')  # Draw node labels

    # Display the plot
    plt.show()