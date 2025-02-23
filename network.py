import networkx as nx

"""
would be cool to add a function that retrieves/removes nodes from a certain cluster.
"""
class network():
    def __init__(self, graph=None):
        
        if graph is None:
            self.graph = nx.Graph()
        else:
            self.graph = graph

    def add_node(self, input, category_in):
        #category_in = input("Add a category for this node: "
        self.graph.add_node(input, category = category_in)

    def add_conn(self, node1, node2):
        self.graph.add_edge(node1, node2)
    
    def remove_node(self, input):
        self.graph.remove_node(input)
    
    def remove_edge(self, node1, node2):
        self.graph.remove_edge(node1,node2)

    def get_nodes(self):
        return list(self.graph.nodes(data=True))