"""DIY Neural Net
Sept. 26, 2019"""

import math
from matrix import Matrix,transpose,multiply



def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def dsigmoid(y):
    return y * (1 - y)


class NeuralNetwork(object):
    def __init__(self, input_nodes,hidden_nodes,output_nodes,
                 learningrate):
        self.input_nodes = input_nodes #int
        self.hidden_nodes = hidden_nodes #int
        self.output_nodes = output_nodes #int

        self.weights_ih = Matrix(self.hidden_nodes,self.input_nodes)
        self.weights_ho = Matrix(self.output_nodes,self.hidden_nodes)
        self.weights_ih.randomize()
        self.weights_ho.randomize()

        self.lr = learningrate

    def activation_function(self,x):
        """The Sigmoid Function"""
        out = [0]*len(x)
        for i, element in enumerate(x):
            #print("element:",element)
            out[i] = sigmoid(x[i][0])
            #print(out)
        return out

    #train the neural network
    def train(self,inputs_list,targets_list):
        #convert inputs list to 2d array
        inputs = inputs_list.transpose()
        targets = targets_list.transpose()

        #calculate signals into hidden layer
        hidden_inputs = multiply(self.weights_ih,inputs)
        hidden_outputs = self.activation_function(hidden_inputs)

        #calculate signals entering final output layer
        final_inputs = multiply(self.weights_ho,hidden_outputs)
        #calculate signals exiting final output layer
        final_outputs = self.activation_function(final_inputs)

        #output layer error is the target - actual
        output_errors = targets - final_outputs
        #hidden layer error is the output_errors, split by weights,
        #recombined at hidden nodes
        hidden_errors = multiply(transpose(self.weights_ho),output_errors)

        #update the weights for the links between the hidden and output layers
        self.weights_ho += self.lr  * multiply((output_errors*final_inputs *\
                                                (1.0 - final_outputs)),
                                               transpose(hidden_outputs))

        #update the weights for the links between the input and hidden layers
        self.weights_ih += self.lr * multiply((hidden_errors * hidden_outputs *\
                                               (1.0 - hidden_outputs)),
                                              transpose(inputs))

    def query(self,inputs_list):
        #convert inputs list to 2d array
        
