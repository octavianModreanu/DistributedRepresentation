import numpy as np

class matrix():

    def __init__(self, node_matrix = None):
        
        if node_matrix is None:
            self._node_matrix = []
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
    
    
    # Right now there is a binary activation function -> It is or it is not
    # in the activation_nodes set.
    
    # Bug: the function only stores activated nodes once per call,
    # once it reaches the next input, the set is empty -> I think that's fine for now
    # since a new input should try and activate all nodes again but good to keep in mind
    # if i ever want to change that behavior
    def activation(self, input, activated_nodes = None, graph = None):
        if activated_nodes is None:
            activated_nodes = set()
            

        if input in activated_nodes:
            return
        
        print(f"\n Trying to propagate node {input}'s activation...")
        activated_nodes.add(input)

        for neighbor in self.adj_list[input]:
            if neighbor not in activated_nodes:
                
                print(f"{input} is propagating to connected nodes:")

                print(f"  -> {neighbor}")
                #activation function
                
                #weight change
                weight = graph[input][neighbor].get("weight", 0)
                category = graph.nodes[input].get("category")
                category_neighbour = graph.nodes[neighbor].get("category")
                if category == category_neighbour:
                    new_weight = weight - 0.1
                elif weight < 1:
                    new_weight = weight + 0.1
                elif weight >= 1:
                    return print ("Weight is already at maximum strength")
                
                graph[input][neighbor]['weight'] = new_weight
                print(f"  -> Weight changed to {new_weight}")
                
                self.activation(neighbor, activated_nodes, graph= graph)
            else:
                print(f"{neighbor} is already activated\n")
    
    def load_matrix (self, graph):
        self._node_matrix = list(graph.nodes())
        self.adj_list = {node: [] for node in self._node_matrix}
        for u, v in graph.edges():
            self.adj_list[u].append(v)
            self.adj_list[v].append(u)
        return print(f"Loaded matrix with {len(self._node_matrix)} nodes.")