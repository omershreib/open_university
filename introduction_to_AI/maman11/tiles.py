from typing import Callable
from introduction_to_AI.maman11.tiles_game_problem import TilesGameProblem
from introduction_to_AI.maman11.tiles_game_state import TilesGameState
from introduction_to_AI.agents import AStarAgent, BFSAgent
from introduction_to_AI.maman11.tiles_evaluators import TilesManhattanEvaluator, TilesMisplacedEvaluator
from introduction_to_AI.maman11.tiles_main_utils import *
from introduction_to_AI.main_utils import display_state
import random

SEED = 8
SLEEP = 0.2
random.seed(SEED)


def make_bfs_agent(problem):
    return BFSAgent(problem=problem)


def make_manhattan_agent(problem):
    return AStarAgent(problem=problem, algorithm_name='manhattan', evaluator=TilesManhattanEvaluator())


def make_misplaced_agent(problem):
    return AStarAgent(problem=problem, algorithm_name='misplaced', evaluator=TilesMisplacedEvaluator())


ALGORITHMS = {
    "bfs": make_bfs_agent,
    "manhattan": make_manhattan_agent,
    "misplaced": make_misplaced_agent,
}


def run_tiles_algorithm(start_board: list[list[int]],
                        alg: str,
                        size: int,
                        add_graphic: bool,
                        agent_factory: Callable,
                        verbose: bool = False):
    """Tiles Game Runner (Solved by A Given Algorithm)

    simulate a solution attempt of the Tiles game following a given algorithm/heuristic, and than
    print the result to the terminal as required in maman #11.

    :param start_board: a parsed stating board configuration that defines that initial state of the Tiles game.
    :param alg: the name of the algorithm to be applied.
    :param size: the square size (n,n) of the board.
    :param add_graphic: if true, run with a graphic displayer
    :param agent_factory: a callable function from ALGORITHMS that return an algorithm agent
    :param verbose: if true, print the result of state.display() to the terminal (false by default)
    """
    graphic_displayer = graphic_displayer_setup(add_graphic, alg_name=alg, size=size)
    init_state = TilesGameState(board=start_board, size=size)
    problem = TilesGameProblem(initial_state=init_state)

    display_state(init_state, graphic_displayer, verbose)

    agent = agent_factory(problem)
    actions = agent.solve(init_state)

    simulate_actions_path(problem, init_state, actions, agent, graphic_displayer)


def tiles_main(board, alg, n, add_graphic, add_verbose):
    if alg == "all":
        print("test all algorithms")
        for this_alg in ALGORITHMS:
            print(f"\n==== test {this_alg} ====\n")
            run_tiles_algorithm(board, this_alg, n, add_graphic, ALGORITHMS[this_alg], add_verbose)
        return

    if alg not in ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {alg}")

    run_tiles_algorithm(board, alg, n, add_graphic, ALGORITHMS[alg])


if __name__ == '__main__':
    tiles_main(*parse_n_args())
