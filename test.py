"""
So the purpose of this is to take a string input, process it and recognise where everything should go
Like i have my Example file ready with all the (inhibitory) connections
My problem right now is how do i represent "Sam" on the input layer
    -> One-hot encoding for the sake of simplicity
    -> Embeddings, which is a lot more complicated

Go hard or go home I say. But at first i think i want to do a one-hot just to get something working
Then i can improve it and make the embedding
"""
import networkx as nx
import itertools

a ="Sam 20 Burglar single Shark HighSchool"
b = a.split(" ")
g = nx.Graph()
for _ in b:
    g.add_node(_)
# Connect each pair of nodes with an edge of weight 0.1
for node1, node2 in itertools.combinations(g.nodes(), 2):
    g.add_edge(node1, node2, weight=0.1)

# Verify
for edge in g.edges(data=True):
    print(edge)