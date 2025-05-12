import networkx as nx
import numpy as np
from Matrices import matrix

"""
would be cool to add a function that retrieves/removes nodes from a certain cluster.
Just an idea but maybe i could make separate matrices based on attributes though
i think that's for later to think about

Bugs:
    The matrix might add nodes from previous loaded saves 
        -> It should refresh with each load
        -> Some kind of save/load functionality should be in place for the backend as well
    I think I should initialize every array with numpy not just the connection one
    The refreshing of conn_matrix could delete existing connections already stored in the matrix
"""
class network():

    def __init__(self, graph=None):
        
        if graph is None:
            self.graph = nx.Graph()
        else:
            self.graph = graph
        self.matrix = matrix()


    def add_node(self, input, category_in):
        self.graph.add_node(input, category = category_in)
        
        # Adds node into the backend
        if input not in self.matrix.node_matrix:
            self.matrix.append_to_matrix(input)

    def add_conn(self, node1, node2):
        # This checks if attributes are the same, which case the weights are inhibitory
        # else the weights are excitatory
        # Updates connections in the backend

        attr1 = self.graph.nodes[node1].get("category")
        attr2 = self.graph.nodes[node2].get("category")
        if attr1 == attr2:
            self.graph.add_edge(node1, node2, weight= -0.1)
            self.matrix.new_connection(node1=node1, node2=node2)
        else:
            self.graph.add_edge(node1, node2, weight= 0.1)
            self.matrix.new_connection(node1=node1, node2=node2)
        
        # Adds nodes to the backend 
        if node1 not in self.matrix.node_matrix:
            self.matrix.append_to_matrix(node1)
        if node2 not in self.matrix.node_matrix:
            self.matrix.append_to_matrix(node2)
    
    def update_weight(self, node1, node2, weight):
        if self.graph.has_edge(node1, node2):
            self.graph[node1][node2]['weight'] = weight
    
    def remove_node(self, input):
        self.graph.remove_node(input)
        # I need to update the backend here as well to remove the node in the matrix
    
    def remove_edge(self, node1, node2):
        self.graph.remove_edge(node1,node2)
        # Over here too

    # When adding a node, it should have some kind of category.
    # Maybe adding a pop-up or a message to add the category of the new node
    def node_activation(self, input):
        for i in input:
            if i not in self.matrix.node_matrix:
                print(f"Node {i} not found in matrix.")
                #self.matrix.append_to_matrix(i)
                #self.graph.add_node(i)
            else:
                self.matrix.activation(i, graph=self.graph)
                
    def load_from_file(self, file_path):
        self.graph = nx.read_graphml(file_path)
        self.current_graph_path = file_path
        self.matrix.load_matrix(graph=self.graph)

# I don't think im using this function anymore I should look around see if i can delete it
    def get_nodes(self):
        return list(self.graph.nodes(data=True))