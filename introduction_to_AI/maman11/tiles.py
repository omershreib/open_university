from typing import Callable
from introduction_to_AI.models import *
from introduction_to_AI.maman11.tiles_game_problem import TilesGameProblem
from introduction_to_AI.agents import AStarAgent, BFSAgent
from introduction_to_AI.maman11.tiles_evaluators import TilesManhattanEvaluator, TilesMisplacedEvaluator
from introduction_to_AI.maman11.tiles_main_utils import *
import random

SEED = 8
SLEEP = 0.2
random.seed(SEED)


def make_bfs_agent(problem):
    return BFSAgent(problem=problem)


def make_manhattan_agent(problem):
    return AStarAgent(problem, TilesManhattanEvaluator())


def make_misplaced_agent(problem):
    return AStarAgent(problem, TilesMisplacedEvaluator())


ALGORITHMS = {
    "bfs": make_bfs_agent,
    "manhattan": make_manhattan_agent,
    "misplaced": make_misplaced_agent,
}


def run_tiles_algorithm(start_board: list[list[int]], alg: str, size: int, add_graphic: bool, agent_factory: Callable):
    graphic_displayer = graphic_displayer_setup(add_graphic, alg_name=alg, size=size)
    init_state = TilesGameState(board=start_board, size=size)
    problem = TilesGameProblem(initial_state=init_state)

    display_state(init_state, graphic_displayer)

    agent = agent_factory(problem)
    actions = agent.solve(init_state)

    simulate_actions_path(problem, init_state, actions, agent, graphic_displayer)


def tiles_main(board, alg, n, add_graphic):
    if alg == "all":
        print("test all algorithms")
        for this_alg in ALGORITHMS:
            print(f"\n==== test {this_alg} ====\n")
            run_tiles_algorithm(board, this_alg, n, add_graphic, ALGORITHMS[this_alg])
        return

    if alg not in ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {alg}")

    run_tiles_algorithm(board, alg, n, add_graphic, ALGORITHMS[alg])


if __name__ == '__main__':
    tiles_main(*parse_n_args())