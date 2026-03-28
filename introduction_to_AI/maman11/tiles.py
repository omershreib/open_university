from typing import Callable
from introduction_to_AI.analysis.plot_tiles_algs_performance import plot_results
from introduction_to_AI.agents import AStarAgent, BFSAgent
from introduction_to_AI.maman11.tiles_evaluators import *
from introduction_to_AI.maman11.tiles_main_utils import *
from introduction_to_AI.main_utils import display_state


def make_bfs_agent(problem):
    return BFSAgent(problem=problem)


def make_manhattan_agent(problem):
    return AStarAgent(problem=problem, algorithm_name='manhattan', evaluator=TilesManhattanEvaluator())


def make_misplaced_agent(problem):
    return AStarAgent(problem=problem, algorithm_name='misplaced', evaluator=TilesMisplacedEvaluator())


def make_rowcol_agent(problem):
    return AStarAgent(problem=problem, algorithm_name='rowcol', evaluator=TilesRowColEvaluator())


def make_max_rowcol_md_agent(problem):
    return AStarAgent(problem=problem, algorithm_name='max_rowcol_md', evaluator=TilesMaxMDRowCol())


def make_lc_agent(problem):
    return AStarAgent(problem=problem, algorithm_name="linear_conflict", evaluator=TilesLinearConflictEvaluator())


def make_md_plus_lc_agent(problem):
    return AStarAgent(problem=problem, algorithm_name="md_plus_lc", evaluator=TilesMDPlusLCEvaluator())


ALGORITHMS = {
    "bfs": make_bfs_agent,
    "manhattan": make_manhattan_agent,
    "misplaced": make_misplaced_agent,
    "rowcol": make_rowcol_agent,
    "max_rowcol_md": make_max_rowcol_md_agent,
    "linear_conflict": make_lc_agent,
    "md_plus_lc": make_md_plus_lc_agent
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

    return simulate_actions_path(problem, init_state, actions, agent, graphic_displayer)


def tiles_main(board: list, alg: str, size: int, add_graphic: bool, add_verbose: bool):
    """Tiles Main

    :param board: a parsed stating board configuration that defines that initial state of the Tiles game.
    :param alg: the name of the algorithm to be applied.
    :param size: the square size (n,n) of the board.
    :param add_graphic: if true, run with a graphic displayer
    :param add_verbose: if true, print the result of state.display() to the terminal (false by default)

    the default option (running tiles without any flag) is alg == "bfs_manhattan".
    this solves that Tiles game EXACTLY as maman #11 requires (without graphic display or verbose)
    with 2 implemented algorithms:
      1. BFS
      2. A* applied with manhattan-distance heuristic

    Note: I added a detailed graphical visualization for debugging purposes.
          however, since it's much nicer to simulate this game using matplotlib,
          I'm leaving it as an option for the benefit of this maman tester.
    """

    # if alg == "bfs_manhattan":
    #     name = 'bfs'
    #     run_tiles_algorithm(board, name, size, add_graphic, ALGORITHMS[name])
    #
    #     name = 'manhattan'
    #     run_tiles_algorithm(board, name, size, add_graphic, ALGORITHMS[name])
    #     exit(0)

    if alg == "all":
        print("test all algorithms")
        for this_alg in ALGORITHMS:
            run_tiles_algorithm(board, this_alg, size, add_graphic, ALGORITHMS[this_alg], add_verbose)

        return

    if alg not in ALGORITHMS:
        raise ValueError(f"Unknown algorithm: {alg}")

    _, path_length, expanded_nodes = run_tiles_algorithm(board, alg, size, add_graphic, ALGORITHMS[alg])
    return {'length': path_length, 'expanded_nodes': expanded_nodes}


if __name__ == '__main__':
    # tiles_main(*parse_n_args())

    #all_performances = read_json('all_boards_algs_performances.json')
    #plot_results(*all_performances)

    #exit()

    board_1 = build_board([1, 2, 0, 3, 4, 5, 6, 7, 8])
    board_2 = build_board([1, 4, 0, 5, 8, 2, 3, 6, 7])
    board_3 = build_board([1, 6, 3, 0, 4, 5, 7, 2, 8])
    board_4 = build_board([6, 4, 8, 7, 5, 1, 2, 3, 0])

    boards = [board_1, board_2, board_3, board_4]
    algs = ['bfs', 'manhattan', 'misplaced', 'rowcol', 'linear_conflict', 'md_plus_lc', 'max_rowcol_md']

    all_performances = []

    for init_board in boards:
        performance: dict = {}

        for this_alg in algs:
            performance[this_alg] = tiles_main(board=init_board,
                                               alg=this_alg,
                                               size=len(init_board),
                                               add_graphic=False,
                                               add_verbose=False)

        # pprint(performance)
        all_performances.append(performance)

    save_dict_as_json(filename='all_boards_algs_performances.json', data=all_performances)

    plot_results(*all_performances)

    # some crazy examples
    #  python -m introduction_to_AI.maman11.tiles 1 6 3 0 4 5 7 2 8
    #  python -m introduction_to_AI.maman11.tiles 6 4 8 7 5 1 2 3 0 -a 'all'
    # python -m introduction_to_AI.maman11.tiles 4 1 2 3 8 5 7 0 9 10 6 11 12 13 14 15 -a 'bfs' -g
