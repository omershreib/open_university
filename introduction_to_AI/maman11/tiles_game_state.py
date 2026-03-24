from __future__ import annotations

from introduction_to_AI.models import Node
from introduction_to_AI.maman11.tiles_board import TilesBoard
import numpy as np


class TilesGameState(TilesBoard):
    """Tiles Game State Suit Class"""
    def __init__(self, board):
        super().__init__(board_config=board)

    def get_key(self):
        return str(self.board)

    def __repr__(self):
        return f"<TilesGameState: {self.get_key()}>"
