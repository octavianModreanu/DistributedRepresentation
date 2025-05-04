#arg1 = self.activationentry.get()
from network import network
import numpy as np

class matrix():

    def __init__(self, node_matrix = None, connection_matrix = None):
        
        if node_matrix is None:
            self._node_matrix = [1,2]
        else:
            self._node_matrix = node_matrix

        self._length = len(self._node_matrix)

        if connection_matrix is None:
            self._connection_matrix = np.zeros((self._length,self._length))
        else:
            self._connection_matrix = connection_matrix

        # Maps the values of the node map to indexes
        self.node_to_index = {node: idx for idx, node in enumerate(self._node_matrix)}

    @property
    def node_matrix(self):
        return self._node_matrix
    
    # I might need to update the connection matrix here since it makes everything 0 again
    @node_matrix.setter
    def node_matrix(self, value):
        self._node_matrix = value
        self._length = len(value)
        self._connection_matrix = np.zeros((self._length, self._length))
        self.node_to_index = {node: idx for idx, node in enumerate(self._node_matrix)}
    
    @property
    def connection_matrix(self):
        return self._connection_matrix
    
    @connection_matrix.setter
    def connection_matrix(self, value):
        self._connection_matrix = value

    def append_to_matrix(self, new_node):
        
        self._node_matrix.append(new_node)
        self._length = len(self._node_matrix)
        new_matrix = np.zeros((self._length, self._length))
        new_matrix[:self._length-1, :self._length-1] = self._connection_matrix
        self._connection_matrix = new_matrix


        self.node_to_index = {node: idx for idx, node in enumerate(self._node_matrix)}

    # There's a problemo here. I didn't see this coming but having
    # a list and a matrix makes it difficult to map the connections in the matrix
    def new_connection(self, node1,node2):
        if node1 != node2:
            
            idx1 = self.node_to_index[node1]
            idx2 = self.node_to_index[node2]
            self._connection_matrix[idx1][idx2] = 1
            self._connection_matrix[idx2][idx1] = 1
                    

        else:
            return print("A node cannot be connected to itself")


    

    #def activation(self, arg1):
     #   correct_length = 0
        

      #  while correct_length == 0:
       #     if len(arg1) == self.length:
                #correct_length = 1
            
        #    else:
                # This needs to call the text field in the GUI
         #       print("The activation string needs to be the length of the input nodes")

matrix = matrix()

matrix.append_to_matrix(3)
matrix.append_to_matrix(4)
matrix.new_connection(1,4)
print(matrix.node_matrix)
print(matrix.connection_matrix)
