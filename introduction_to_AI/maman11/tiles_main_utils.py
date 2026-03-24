from typing import Optional
from introduction_to_AI.maman11.tiles_graphic_displayer import TilesGameGraphicDisplayer
from introduction_to_AI.maman11.tiles_game_state import TilesGameState
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a 3x3 tiles board from 9 numbers"
    )

    parser.add_argument(
        "tiles",
        type=int,
        nargs=9,
        help="9 numbers representing the tiles (row-wise)",
    )

    parser.add_argument('--graphic', '-gd', action='store_true')
    parser.add_argument('--alg', '-a', type=str, default=None)

    args = parser.parse_args()

    # Convert flat list into 3x3 list of lists
    tiles = args.tiles
    alg = args.alg
    add_graphic = args.graphic

    algs = ['bfs', 'manhattan']

    if not alg:
        print("cannot run without an algorithm")

    if alg not in algs:
        print(f"this {alg} algorithm is not implemented (options: {algs})")

    if add_graphic:
        print("run program with graphic")

    else:
        print("run program without graphic")

    board = [tiles[i:i + 3] for i in range(0, 9, 3)]

    return board, alg, add_graphic


def graphic_displayer_setup(graphic: bool, alg_name: str) -> Optional[TilesGameGraphicDisplayer]:
    if graphic:
        graphic_displayer = TilesGameGraphicDisplayer()
        graphic_displayer.title = f'Tile Game Solved By {alg_name.upper()}'
        return graphic_displayer

    return None


def display_state(state: TilesGameState, graphic_displayer: Optional[TilesGameGraphicDisplayer]):
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
