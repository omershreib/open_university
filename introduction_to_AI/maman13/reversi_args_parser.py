import argparse


def parse_n_args():
    parser = argparse.ArgumentParser(
        description="Run Reversi Game Simulation Using Heuristic Evaluators"
    )

    parser.add_argument("num",
                        type=int,
                        help="initialize game with a minimum number of disks")

    parser.add_argument("--display_all_actions",
                        "-d",
                        action="store_true",
                        help="display game action step-by-step")

    parser.add_argument("--methodical",
                        "-m",
                        type=int,
                        help="set how many game stages (from start) to display, before jumping towards the final stage")

    parser.add_argument("--red_agent",
                        "-red",
                        type=str,
                        help="select the agent used by the maximum (red) player")

    parser.add_argument("--white_agent",
                        "-white",
                        type=str,
                        help="select the agent used by the minimum (white) player")

    parser.add_argument("--ahead",
                        "-a",
                        type=int,
                        default=2,
                        help="set the depth of minmax tree (will be applied on both players)")

    args = parser.parse_args()
    num = args.num
    display_all_actions = args.display_all_actions
    methodical = args.methodical
    red_agent = args.red_agent
    white_agent = args.white_agent
    ahead = args.ahead

    # todo: check agents support

    return num, display_all_actions, methodical, red_agent, white_agent, ahead
