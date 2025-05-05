#arg1 = self.activationentry.get()
from network import network
import numpy as np

class matrix():

    def __init__(self, node_matrix = None):
        
        if node_matrix is None:
            self._node_matrix = [1,2]
        else:
            self._node_matrix = node_matrix

        self._length = len(self._node_matrix)

        # Initialize the adjacency list as an empty dictionary
        self.adj_list = {node: [] for node in self._node_matrix}

    @property
    def node_matrix(self):
        return self._node_matrix
    
    # I might need to update the connection matrix here since it makes everything 0 again
    @node_matrix.setter
    def node_matrix(self, value):
        self._node_matrix = value
        self.adj_list = {node: [] for node in self._node_matrix}

    
    def append_to_matrix(self, new_node):
        
        # Appends a new node to the backend matrix and expands the connection matrix
        self._node_matrix.append(new_node)
        self.adj_list[new_node] = []


        self.node_to_index = {node: idx for idx, node in enumerate(self._node_matrix)}

    def new_connection(self, node1,node2):
        if node1 != node2:

            if node2 not in self.adj_list[node1]:
                self.adj_list[node1].append(node2)
            if node1 not in self.adj_list[node2]:
                self.adj_list[node2].append(node1)

        else:
            return print("A node cannot be connected to itself")
    
    # what if it would activate a node, and then it checks what's it connected with,
    # then it activates those follow-up connections and adjusts weights
    def activation(self, input, activated_nodes = None):
        if activated_nodes is None:
            activated_nodes = set()

        if input in activated_nodes:
            return
        
        print(f"Trying to activate node {input}...")

        for neighbor in self.adj_list[input]:
            if neighbor not in activated_nodes:
                
                print(f"Activating node {input} and propagating to connected nodes:")
                activated_nodes.add(input)

                print(f"  -> {neighbor}")
                #activation function
                #weight change
                
                self.activation(neighbor, activated_nodes)
            else:
                print(f"Node {input}'s connections are already activated\n")
                
        
        

# These stuff go in GUI after im finished with all this
matrix = matrix()

input = [1,4,1,5]
matrix.append_to_matrix(3)
matrix.append_to_matrix(4)
matrix.new_connection(1,4)
matrix.new_connection(1,3)
matrix.new_connection(1,2)
print(matrix.node_matrix)
for node, neighbors in matrix.adj_list.items():
    print(f"  Node {node}: Connected to {neighbors}")

for node in input:
    if node in matrix.node_matrix:
        matrix.activation(node)
    else:
        print(f"Node {node} not found in node matrix.")