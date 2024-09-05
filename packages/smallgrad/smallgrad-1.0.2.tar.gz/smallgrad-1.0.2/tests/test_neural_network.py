import random

import pytest
from smallgrad.backpropagation import Value
from smallgrad.neural_network import MLP, Layer, Neuron


@pytest.fixture(autouse=True)
def set_seed():
    random.seed(42)


@pytest.mark.parametrize(
    "input, expected_weights, expected_bias",
    [
        (
            3,
            [
                0.2788535969157675,
                -0.9499784895546661,
                -0.4499413632617615,
            ],
            -0.5535785237023545,
        )
    ],
)
def test_neuron_initialization(input, expected_weights, expected_bias):
    neuron = Neuron(nin=input)
    for weight, expected_weight in zip(neuron.weights, expected_weights):
        assert weight.data == expected_weight
    assert neuron.bias.data == expected_bias


@pytest.mark.parametrize(
    "input_dim, input_neuron, activation_function, expected_output",
    [
        (2, [0.77, -0.8], "relu", 0.5247586980071124),
        (2, [0.5, -0.3], "relu", 0),
        (3, [0.3, 0.8, -0.6], "tanh", -0.7442502896564978),
    ],
)
def test_neuron_forward(input_dim, input_neuron, activation_function, expected_output):
    neuron = Neuron(nin=input_dim, activation=activation_function)
    x = [Value(data=input) for input in input_neuron]
    output = neuron(x)
    assert output.data == expected_output


def test_layer_initialization():
    layer = Layer(nin=3, nout=2)
    assert len(layer.neurons) == 2
    assert isinstance(layer.neurons[0], Neuron)


@pytest.mark.parametrize(
    "input_dim, output_dim, input_neuron, expected_outputs",
    [
        (2, 3, [0.77, -0.8], [0.5247586980071124, 0, 1.1086980414289371]),
    ],
)
def test_layer_forward_pass(input_dim, output_dim, input_neuron, expected_outputs):
    layer = Layer(nin=input_dim, nout=output_dim)
    x = [Value(data=input) for input in input_neuron]
    outputs = layer(x)
    for output, expected_output in zip(outputs, expected_outputs):
        assert output.data == expected_output


def test_mlp_initialization():
    mlp = MLP(nin=3, nouts=[4, 2])
    assert len(mlp.layers) == 2
    assert isinstance(mlp.layers[0], Layer)


@pytest.mark.parametrize(
    "input_dim, output_dim, input_neuron, expected_outputs",
    [
        (3, [4, 2], [0.77, -0.8, 0.8], [0.6152882955422708, 0, 0]),
    ],
)
def test_mlp_forward_pass(input_dim, output_dim, input_neuron, expected_outputs):
    mlp = MLP(nin=3, nouts=[4, 2])
    x = [Value(data=input) for input in input_neuron]
    outputs = mlp(x)
    for output, expected_output in zip(outputs, expected_outputs):
        assert output.data == expected_output
