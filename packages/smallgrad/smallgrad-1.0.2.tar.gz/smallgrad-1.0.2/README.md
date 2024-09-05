# smallgrad

smallgrad is a minimalistic engine that implements backpropagation from scratch for neural networks. It allows users to visualize the computational graph along with the gradients and includes a script for building a Multi-Layer Perceptron (MLP) and visualize its computational graph.

# Features
- **Backpropagation from Scratch**: Implements a simple and understandable version of backpropagation, making it a great learning resource.
- **Visualize Computational Graph**: Visualizes the computational graph and gradients during the forward and backward pass.
- **MLP Builder Script**: Easily build Multi-Layer Perceptrons (MLPs) and visualize their learning process.
# Installation
If you want the latest updates:
```
git clone https://github.com/lorenzo-delsignore/smallgrad.git
cd smallgrad
pip install -e .
```
If you want the stable version:
```
pip install smallgrad
```
To render the computational graph, you also need an external dependency [Graphviz](https://www.graphviz.org/).

If you want to install the dependency with conda you use the following command: ```conda install -c conda-forge pygraphviz```.

You can install smallgrad also with Docker, in which contains also the external Graphviz dependency:
```
cd smallgrad
docker -t smallgrad .
```
# Usage
To use smallgrad, you can run the provided script to create an MLP and visualize the computational graph:
```
usage: smallgrad [-h] [--save_dir SAVE_DIR] --input INPUT [INPUT ...] --output OUTPUT [OUTPUT ...] [--activation ACTIVATION]
```
## Options:
- **save_dir**: Directory to save the visualization of the computational graph.
- **input**: Specify the input features for the MLP.
- **output**: Specify the output dimensions of each hidden and output layer of the MLP.
- **activation**: Choose the activation function (only relu and tanh are supported at the moment) for the MLP layers.

## Example Usage:
```
smallgrad --input 2 4 --output 3 1 --activation relu --save_dir ./graphs
```
With Docker:
```
docker run --rm --name smallgrad -v host_path_to_save:/graphs smallgrad --input 1 1 --output 2 1 --activation relu --save_dir /graphs
```
