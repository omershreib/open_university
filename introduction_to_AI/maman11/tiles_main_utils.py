import time
from typing import Optional, Tuple, List, Any
from introduction_to_AI.maman11.tiles_graphic_displayer import TilesGameGraphicDisplayer
from introduction_to_AI.maman11.tiles_game_state import TilesGameState
import argparse
import math


def parse_n_args() -> tuple[list[Any], str, int, bool]:
    """Argument Parser

    this function handle the receiving of user's input from terminal, and support any (n,n) legal board
    configuration for n >= 3 (tested on n=3 and n=4).

    The value of n is derived from the first n^2 arguments the user enter.
    For example:
        running `tiles 1 6 3 0 4 5 7 2 8`  will resolve n=3
        but running `tiles 4 1 2 3 8 5 7 0 9 10 6 11 12 13 14 15` will resolve n=4

    Returns:
        board:  list[list[int]] in the shape of (n,n)
                represents a starting initial Tiles board configuration.
        alg:    str
                the name of the algorithm to run
        n:  int
            define the shape of the Tiles game (also known as the "size" or the "upper-bound" of the rows/columns)
        add_graphi: bool

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

    parser.add_argument('--graphic', '-g', type=bool, action='store_true')
    parser.add_argument('--alg', '-a', type=str, required=True)

    args = parser.parse_args()

    tiles = args.tiles
    alg = args.alg.lower()
    add_graphic = args.graphic

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

    # parsing summary
    print(f"board size: {n}x{n}")
    print(f"algorithm: {alg}")
    print("graphics:", "ON" if add_graphic else "OFF")

    return board, alg, n, add_graphic


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


def display_state(state: TilesGameState, graphic_displayer: Optional[TilesGameGraphicDisplayer]):
    """Display State

    A wrapper function that handle the displacement of a given TilesGameState object.
    If a TilesGameGraphicDisplayer is given then visualize the board using matplotlib.
    Anyway, call state.display() that print the board on terminal.

    :param state: a given TilesGameState
    :param graphic_displayer: (optional) a TilesGameGraphicDisplayer object
    """
    if graphic_displayer:
        graphic_displayer.refresh(state.board)

    state.display()


def summarize_search(agent, path):
    print("find solution")
    print(f"tiles path: {path}")
    print(f"length: {len(path)}")
    print(f"expanded: {agent.expanded_nodes}")


def simulate_actions_path(problem, init_state, actions, agent, graphic_displayer=None):
    path = []
    curr_state = init_state
    for action in actions:
        board = problem.game_state.board
        tile_pos = action.tile_pos
        path.append(int(board[*tile_pos]))
        curr_state = problem.update(curr_state, action)

        display_state(curr_state, graphic_displayer)

        if problem.is_goal_state(curr_state):
            summarize_search(agent, path)
            break
    else:
        print("agent cannot find a solution")
