from __future__ import annotations

from typing import Optional, Any
from introduction_to_AI.models import *
from introduction_to_AI.maman11.tiles_graphic_displayer import TilesGameGraphicDisplayer
from introduction_to_AI.main_utils import display_state
from introduction_to_AI.maman11.tiles_game_problem import TilesGameProblem
import argparse
import math


def parse_n_args() -> tuple[list[Any], str, int, bool, bool]:
    """Argument Parser

    this function handle the receiving of user's input from terminal, and support any (n,n) legal board
    configuration for n >= 3 (tested on n=3 and n=4).

    The value of n is derived from the first n^2 arguments the user enter.
    For example:
        running `tiles 1 6 3 0 4 5 7 2 8`  will resolve n=3
        but running `tiles 4 1 2 3 8 5 7 0 9 10 6 11 12 13 14 15` will resolve n=4

    Note:   yes, I know that the maman expected to handle only the classic 8-Puzzle case of
            n=3, but for the sport I attempted to solve the general case (for ANY n>=3)

    :returns:
        board:  represents a starting initial Tiles board configuration.
        alg:    the name of the algorithm to run
        size:   the square n^2 shape of the Tiles game
        add_graphic: true or false, depending on the existence/absence of the -g flag
                    (optional setup to add matplot lib visualization)
        verbose: true or false, depending on the existence/absence of the -v flag
                    (optional setup to print the solution path of the Tiles game to the terminal)

    """
    parser = argparse.ArgumentParser(
        description="Create an n x n tiles board from n^2 numbers"
    )

    parser.add_argument(
        "tiles",
        type=int,
        nargs="+",
        help="n^2 numbers representing the tiles (row-wise)",
    )

    parser.add_argument('--graphic', '-g', action='store_true', help="run with graphic displayer")
    parser.add_argument('--verbose', '-v', action='store_true', help="enable verbose")
    parser.add_argument('--alg', '-a', type=str, required=True, help="choose and algorithm")

    args = parser.parse_args()

    tiles = args.tiles
    alg = args.alg.lower()
    add_graphic = args.graphic
    verbose = args.verbose

    # validate perfect square
    length = len(tiles)
    n = int(math.sqrt(length))

    if n * n != length:
        raise ValueError(f"number of tiles ({length}) must form a perfect square (e.g., 9, 16, 25, ...)")

    # validate algorithm
    supported_algorithms = ['bfs', 'manhattan', 'misplaced', 'all']

    if alg not in supported_algorithms:
        raise ValueError(f"algorithm '{alg}' not implemented (options: {supported_algorithms})")

    # validate a legal tile input (0..n^2-1)
    expected = set(range(length))
    if set(tiles) != expected:
        raise ValueError(f"tiles must contain all values from 0 to {length - 1} exactly once")

    # build board
    board = [tiles[i:i + n] for i in range(0, length, n)]

    # parsing summary (on debug)
    # print(f"board size: {n}x{n}")
    # print(f"algorithm: {alg}")
    # print("graphics: ", "ON" if add_graphic else "OFF")
    # print("verbose: ", "ON" if verbose else "OFF")

    return board, alg, n, add_graphic, verbose


def graphic_displayer_setup(graphic: bool, alg_name: str, size: int) -> Optional[TilesGameGraphicDisplayer]:
    """Graphic Displayer Setup

    :param graphic: true if graphic displayer is ON, otherwise false
    :param alg_name: the name of the supported algorithm (or 'all' if the user want to run all of them)
    :param size: define the square (size^2) shape of the tiles game
    :return: A TilesGameGraphicDisplayer object if graphic is True, None otherwise.
    """
    if graphic:
        graphic_displayer = TilesGameGraphicDisplayer(size=size)
        graphic_displayer.title = f'Tile Game Solved By {alg_name.upper()}'
        return graphic_displayer

    return None


# def display_state(state: TilesGameState, graphic_displayer: Optional[TilesGameGraphicDisplayer], verbose):
#     """Display State
#
#     manage the visual/terminal display of a given TilesGameState object.
#     this is an optional function that will do nothing if both graphic_displayer and verbose equal to false
#
#     :param state: a given TilesGameState
#     :param graphic_displayer: (optional) a TilesGameGraphicDisplayer object
#     :param verbose: (optional) if true, print the result of state.display() to the terminal (false by default)
#     """
#     if graphic_displayer:
#         graphic_displayer.refresh(state.get_value())
#
#     if verbose:
#         state.display()


def summarize_search(agent: AtomicAgent, path):
    print(f"algorithm: {agent.algorithm_name}")
    print(f"tiles path: {path}")
    print(f"length: {len(path)}")
    print(f"expanded: {agent.expanded_nodes}")


def simulate_actions_path(problem: TilesGameProblem,
                          init_state: State,
                          actions,
                          agent: AtomicAgent,
                          graphic_displayer=None,
                          verbose: bool = False):
    path = []
    curr_state = init_state
    for action in actions:
        board = problem.game_state.board
        tile_pos = action.tile_pos
        path.append(int(board[*tile_pos]))
        curr_state = problem.update(curr_state, action)

        display_state(curr_state, graphic_displayer, verbose)

        if problem.is_goal_state(curr_state):
            summarize_search(agent, path)
            break
    else:
        print("agent cannot find a solution")
