from __future__ import annotations

from introduction_to_AI.models import Node
from introduction_to_AI.maman11.tiles_board import TilesBoard
import numpy as np


class TilesGameState(Node, TilesBoard):
    """Tiles Game State Suit Class"""
    def __init__(self, board, parent=None, action=None, path_cost=1):
        TilesBoard.__init__(self)
        self.board = board

        Node.__init__(self, state=self, parent=parent, action=action, depth=0, path_cost=path_cost)

    def get_key(self):
        return str(self.board)

    def __repr__(self):
        return f"<TilesGameState: {self.get_key()}>"
