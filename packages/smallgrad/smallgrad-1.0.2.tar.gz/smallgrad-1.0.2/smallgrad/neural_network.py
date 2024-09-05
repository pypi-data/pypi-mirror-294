import random

from smallgrad.backpropagation import Value


class Neuron:
    def __init__(self, nin, activation="relu"):
        self.weights = []
        for i in range(nin):
            weight = Value(random.uniform(-1, 1))
            weight.label = f"w_{i} with id {id(weight)}"
            self.weights.append(weight)
        self.bias = Value(random.uniform(-1, 1))
        self.bias.label = f"bias with id {id(self.bias)}"
        self.activation = activation

    def __call__(self, x):
        output = sum((wi * xi for wi, xi in zip(self.weights, x)), self.bias)
        if self.activation == "relu":
            output = output.relu()
        elif self.activation == "tanh":
            output = output.tanh()
        return output


class Layer:
    def __init__(self, nin, nout, activation="relu"):
        self.neurons = [Neuron(nin, activation=activation) for _ in range(nout)]

    def __call__(self, x):
        output = [n(x) for n in self.neurons]
        return output if len(output) > 1 else output[0]


class MLP:
    def __init__(self, nin, nouts, activation="relu"):
        in_outs = [nin] + nouts
        self.layers = [
            Layer(in_outs[i], in_outs[i + 1], activation=activation)
            for i in range(len(nouts))
        ]

    def __call__(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
