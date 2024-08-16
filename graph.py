import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np
import threading
import asyncio


def share_data(graph, node):
    # Get neighbors of the current node
    # Share 'transaction' data with neighbors, excluding lists already present

    neighbors = list(graph.neighbors(node))

    data=node.transaction_list

    for neighbor in neighbors:
        for d in data:
            if d not in neighbor.transaction_list:
                node.simulate_latency(neighbor,d) 


def propagate_data_until_convergence(graph):

    # IT is used to broadcast the data
    previous_data = {node: None for node in graph}

    current_data = {node: node.transaction_list.copy() for node in graph}

    while current_data != previous_data:
        previous_data = current_data.copy()

        for node in graph:
            share_data(graph, node)

        current_data = {node: node.transaction_list.copy() for node in graph}

def gen_graph(node_objects):
    # Create an undirected graph with minimum degree 3 and maximum degree 6 with nodes as node objects
    graph = nx.Graph()
    graph.add_nodes_from(node_objects)
    for i, node in enumerate(node_objects):
        current_degree = graph.degree(node)

        while current_degree < 3:
            remaining_nodes = set(node_objects) - set(graph.neighbors(node))
            if remaining_nodes:
                random_node = random.choice(list(remaining_nodes))
                if random_node != node:
                    graph.add_edge(node, random_node)
                    current_degree += 1
            else:
                break  

        while current_degree > 6:
            neighbor = random.choice(list(graph.neighbors(node)))
            graph.remove_edge(node, neighbor)
            current_degree -= 1

    return graph


def share_data_block(graph, node):
    # Get neighbors of the current node
    # Share 'transaction' data with neighbors, excluding keys already present

    neighbors = list(graph.neighbors(node))

    data=node.block_chain.copy()

    for neighbor in neighbors:
        for key, value in data.items():
            if key not in neighbor.block_chain:
                node.attach_block(neighbor,value)

def propagate_data_until_convergence_block(graph):

    #It is used to broadcast the block
    previous_data = {node: None for node in graph}

    current_data = {node: node.block_chain.copy() for node in graph}

    while current_data != previous_data:
        previous_data = current_data.copy()

        for node in graph:
            share_data_block(graph, node)

        current_data = {node: node.block_chain.copy() for node in graph}


def plot_graph(G):

    
    pos = nx.spring_layout(G) 
    node_labels = {node: node.number for node in G.nodes()} 
    nx.draw(G, pos, with_labels=False, node_size=500, node_color='skyblue', edge_color='gray')  
    nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=12, font_color='black')  

    plt.savefig("10_nodes")