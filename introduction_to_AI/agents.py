from game_state import GameState
from models import Move

class ReversiAgent:
    def choose_move(self, state: GameState) -> Move:
        raise NotImplementedError
