import pytest
from smallgrad.backpropagation import Value

from tests.utils import create_values_dict


@pytest.mark.parametrize(
    "input, output, expected_gradients",
    [
        ({"a": -3, "b": 2}, -1, {"a": 1, "b": 1}),
        ({"a": 4, "b": -3}, 1, {"a": 1}),
    ],
)
def test_add(input, output, expected_gradients):
    values = create_values_dict(input)
    sum = values["a"] + values.get("b", input["b"])
    assert sum.data == output
    sum.backward()
    for var, expected_grad in expected_gradients.items():
        assert values[var].grad == expected_grad


@pytest.mark.parametrize(
    "input, output, expected_gradients",
    [
        ({"a": -3, "b": 2}, -5, {"a": 1, "b": -1}),
        ({"a": 4, "b": -3}, 7, {"a": 1}),
    ],
)
def test_sub(input, output, expected_gradients):
    values = create_values_dict(input)
    sub = values["a"] - values.get("b", input["b"])
    assert sub.data == output
    sub.backward()
    for var, expected_grad in expected_gradients.items():
        assert values[var].grad == expected_grad


@pytest.mark.parametrize(
    "input, output, expected_gradients",
    [
        ({"a": -3, "b": 2}, -6, {"a": 2, "b": -3}),
        ({"a": 4, "b": -3}, -12, {"a": -3}),
    ],
)
def test_mul(input, output, expected_gradients):
    values = create_values_dict(input)
    mul = values["a"] * values.get("b", input["b"])
    assert mul.data == output
    mul.backward()
    for var, expected_grad in expected_gradients.items():
        assert values[var].grad == expected_grad


@pytest.mark.parametrize(
    "input, output, expected_gradients",
    [
        ({"a": -3, "b": 2}, -1.5, {"a": 0.5, "b": 0.75}),
        ({"a": 4, "b": -3}, -1.3333333333333333, {"a": -0.3333333333333333}),
    ],
)
def test_div(input, output, expected_gradients):
    values = create_values_dict(input)
    div = values["a"] / values.get("b", input["b"])
    assert div.data == output
    div.backward()
    for var, expected_grad in expected_gradients.items():
        assert values[var].grad == expected_grad


@pytest.mark.parametrize(
    "a, b, output, expected_gradient",
    [
        (-3, 2, 9, -6),
        (4, 3, 64, 48),
    ],
)
def test_pow(a, b, output, expected_gradient):
    a = Value(data=a, label="a")
    pow = a**b
    assert pow.data == output
    pow.backward()
    a.grad == expected_gradient


@pytest.mark.parametrize(
    "input, output, expected_gradient",
    [
        (2, 2, 1),
        (-2.0, 0, 0),
        (1.3, 1.3, 1),
    ],
)
def test_relu(input, output, expected_gradient):
    a = Value(data=input, label="a")
    relu = a.relu()
    assert relu.data == output
    relu.backward()
    assert a.grad == expected_gradient


@pytest.mark.parametrize(
    "input, output, expected_gradient",
    [
        (2, 0.9640275800758169, 0.07065082485316443),
        (-2.0, -0.9640275800758168, 0.07065082485316465),
        (1.3, 0.8617231593133063, 0.25743319670309406),
    ],
)
def test_tanh(input, output, expected_gradient):
    a = Value(data=input, label="a")
    tanh = a.tanh()
    assert tanh.data == output
    tanh.backward()
    assert a.grad == expected_gradient


@pytest.mark.parametrize(
    "input, output, expected_gradient",
    [
        (2, 7.38905609893065, 7.38905609893065),
        (-2.0, 0.1353352832366127, 0.1353352832366127),
        (1.3, 3.6692966676192444, 3.6692966676192444),
    ],
)
def test_exp(input, output, expected_gradient):
    a = Value(data=input, label="a")
    exp = a.exp()
    assert exp.data == output
    exp.backward()
    assert a.grad == expected_gradient


@pytest.mark.parametrize(
    "input, output, expected_gradient",
    [
        (3, -3, -1),
        (-2, 2, -1),
    ],
)
def test_neg(input, output, expected_gradient):
    a = Value(data=input, label="a")
    z = -a
    assert z.data == output
    z.backward()
    assert a.grad == expected_gradient


@pytest.mark.parametrize(
    "input, output, expected_gradient",
    [
        (3, 6, 2),
        (-2, -4, 2),
    ],
)
def test_rmul(input, output, expected_gradient):
    a = Value(data=input, label="a")
    rmul = 2 * a
    assert rmul.data == output
    rmul.backward()
    assert a.grad == expected_gradient


@pytest.mark.parametrize(
    "input, expression, output, expected_gradients",
    [
        (
            {
                "a": -1,
                "b": 4,
                "c": 0.5,
            },
            lambda a, b, c: (a + b) * c + a**2,
            2.5,
            {"a": 0.5 + 2 * -1, "b": 0.5, "c": 3},
        ),
        (
            {
                "a": 0.5,
                "b": -2,
                "c": 3,
            },
            lambda a, b, c: (a - b) * c + b**3,
            -0.5,
            {"a": 3, "b": -3 + 3 * (-2) ** 2, "c": 0.5 - (-2)},
        ),
    ],
)
def test_complex_expression(input, expression, output, expected_gradients):
    values = create_values_dict(input)
    expr = expression(values["a"], values["b"], values["c"])
    assert expr.data == output
    expr.backward()
    for var, expected_grad in expected_gradients.items():
        assert values[var].grad == expected_grad
