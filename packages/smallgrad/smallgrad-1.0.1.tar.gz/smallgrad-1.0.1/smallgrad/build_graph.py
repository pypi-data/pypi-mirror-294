import argparse

from smallgrad.neural_network import MLP


def main():
    parser = argparse.ArgumentParser(
        description="Build a computational graph and apply backpropoagation to an MLP"
    )
    parser.add_argument(
        "--save_dir", "-s", type=str, help="Directory to save the Computational Graph"
    )
    parser.add_argument(
        "--input", "-i", required=True, nargs="+", type=float, help="Input of the MLP"
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        nargs="+",
        type=int,
        help="A list of neurons output",
    )
    parser.add_argument(
        "--activation",
        "-a",
        type=str,
        default="relu",
        help="Activation function to use for each layer of the MLP: 'relu' or 'tanh' (default: 'relu')",
    )
    args = parser.parse_args()
    if args.activation not in ("relu", "tanh"):
        parser.error(f"Unsupported activation function: {args.activation}")
    x = args.input
    n = MLP(len(x), args.output, activation=args.activation)
    output = n(x)
    output.backward()
    output.print_graph(directory=args.save_dir)


if __name__ == "__main__":
    main()
