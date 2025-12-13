from models import Color
from game_board import ReversiGameBoard
from game_state import GameState
from agents import ReversiAgent


class ReversiGameRunner:
    def __init__(self, max_agent: ReversiAgent, min_agent: ReversiAgent, verbose: bool = True):
        self.agents = {
            Color.RED: max_agent,
            Color.WHITE: min_agent
        }

        self.verbose = verbose
        self.state = GameState(board=ReversiGameBoard.initial_game_setup(), player_turn=Color.RED)

    def current_agent(self) -> ReversiAgent:
        return self.agents[self.state.player_turn]

    def next_step(self) -> None:
        if self.state.is_terminal():
            return

        player = self.state.player_turn
        agent = self.current_agent()

        move = agent.choose_move(self.state)
        legal_moves = self.state.actions()

        if move not in legal_moves:
            raise ValueError(f"agent {agent} played illegal move {move}\nlegal moves: {legal_moves}")


    def terminal_test(self, state) -> bool:
        pass

    def calc_state_utility(self, state, player):
        pass

    def next_agent(self, state):
        pass
