from __future__ import annotations

from introduction_to_AI.models import Node
from introduction_to_AI.maman11.tiles_board import TilesBoard
import numpy as np

class TilesGameState(Node):
    def __init__(self, state: TilesBoard, parent=None, action=None, path_cost=1):
        super().__init__(state=state, parent=parent, action=action, path_cost=path_cost)

    def get_tiles_board(self) -> TilesBoard:
        return self.state

    def get_board(self) -> np.array:
        return self.state.board


    def __repr__(self):
        return f"{self.get_board()}"
