from introduction_to_AI.maman11.tiles_board import TilesBoard
from introduction_to_AI.maman11.tiles_models import TilesGameProblem, TilesGameState

if __name__ == '__main__':

    # init tiles game board
    board = TilesBoard()
    init_state = TilesGameState(state=board,parent=None, action=None, path_cost=1)

    print("init board")
    board.display()

    print("\n")

    tiles_problem = TilesGameProblem(initial_state=init_state)

    actions = tiles_problem.get_actions(init_state)
    action = actions[0]

    new_state = tiles_problem.update(state=init_state, action=action)

    print("parent stage board")
    new_state.parent.display()

    print("\n")

    print("new stage board")
    new_state.state.display()




