import argparse


REVERSI_AGENTS_SUPPORT = ['heuristic_score', 'hungry_score']

def parse_n_args():
    parser = argparse.ArgumentParser(
        description="Run Reversi game simulation using different rivals agents",
        epilog=f"Agents supported: {REVERSI_AGENTS_SUPPORT}"
    )

    # parser.add_argument("num",
    #                     type=int,
    #                     help="initialize game with a minimum number of disks")

    # verbose is displayAllActions (a better flag name)
    parser.add_argument("--verbose",
                        "-v",
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

    parser.add_argument('--graphic',
                        '-g',
                        action='store_true',
                        help="run with graphic displayer")


    args = parser.parse_args()
    #num = args.num
    verbose = args.verbose
    methodical = args.methodical
    red_agent = args.red_agent
    white_agent = args.white_agent
    ahead = args.ahead
    graphic = args.graphic

    # validate agent type spelling
    for agent in [red_agent, white_agent]:
        if agent not in REVERSI_AGENTS_SUPPORT:
            print(f"unknown agent {agent}")



    return verbose, methodical, red_agent, white_agent, ahead, graphic
