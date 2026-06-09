import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Run MDP algorithms")

    parser.add_argument(
        "filename",
        help="Path to the input .npz file"
    )

    parser.add_argument(
        "algorithm",
        choices=["ValueIteration", "PolicyIteration"],
        help="Algorithm to run"
    )

    return parser.parse_args()