import math
from collections import deque

import graphviz


class Value:
    def __init__(
        self,
        data,
        label="",
        children=(),
    ):
        self.data = data
        self.grad = 0
        self.children = set(children)
        self.label = label
        self._backward = lambda: None

    def __add__(self, other):
        other = (
            other
            if isinstance(other, Value)
            else Value(other, label=f"number summed to {self.label}")
        )
        sum = Value(self.data + other.data, label="+")
        sum.children.add(self)
        sum.children.add(other)

        def _backward():
            self.grad += sum.grad
            other.grad += sum.grad

        sum._backward = _backward
        return sum

    def __mul__(self, other):
        other = (
            other
            if isinstance(other, Value)
            else Value(other, label=f"number multiplied to {self.label}")
        )
        mul = Value(self.data * other.data, label="*")
        mul.children.add(self)
        mul.children.add(other)

        def _backward():
            self.grad += other.data * mul.grad
            other.grad += self.data * mul.grad

        mul._backward = _backward
        return mul

    def __pow__(self, other):
        assert isinstance(
            other, (int, float)
        ), "only supporting int/float powers for now"
        out = Value(self.data**other, label=f"**{other}")
        out.children.add(self)

        def _backward():
            self.grad += (other * self.data ** (other - 1)) * out.grad

        out._backward = _backward
        return out

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self * other**-1

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + (-other)

    def tanh(self):
        x = self.data
        t = (math.exp(2 * x) - 1) / (math.exp(2 * x) + 1)
        out = Value(t, label="tanh")
        out.children.add(self)

        def _backward():
            self.grad += (1 - out.data**2) * out.grad

        out._backward = _backward
        return out

    def exp(self):
        out = Value(math.exp(self.data), label="exp")
        out.children.add(self)

        def _backward():
            self.grad += out.data * out.grad

        out._backward = _backward
        return out

    def relu(self):
        out = Value(max(0, self.data), label="relu")
        out.children.add(self)

        def _backward():
            self.grad += (self.data > 0) * out.grad

        out._backward = _backward
        return out

    def backward(self):
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v.children:
                    build_topo(child)
                topo.append(v)

        build_topo(self)
        self.grad = 1.0
        for v in reversed(topo):
            v._backward()

    def print_graph(self, filename="Computational_graph", directory=".", format="pdf"):
        dot = graphviz.Digraph(
            comment="Computational Graph", graph_attr={"rankdir": "LR"}
        )
        root = self

        def bfs(root):
            nodes, edges = set(), set()
            queue = deque()
            queue.append(root)
            while len(queue) > 0:
                node = queue.popleft()
                node_id = id(node)
                if node not in nodes:
                    dot.node(
                        f"{node_id}",
                        f"{node.label}\ndata: {node.data}\ngrad: {node.grad}",
                    )
                    nodes.add(node)
                    for child in node.children:
                        child_id = id(child)
                        edges.add((child, node))
                        queue.append(child)
                        dot.edge(f"{child_id}", f"{node_id}")

        bfs(root)
        output_path = dot.render(
            filename=filename, directory=directory, format=format, cleanup=True
        )
        print(f"Graph saved to: {output_path}")

    def __repr__(self):
        return f"Value {self.data}, label: {self.label}, grad: {self.grad}"
