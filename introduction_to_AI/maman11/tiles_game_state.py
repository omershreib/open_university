"""
Author: Omer Shraibshtein (205984271)
Date:   06/04/2026
Email:  omershreib@gmail.com
"""


from __future__ import annotations

from introduction_to_AI.maman11.tiles_board import TilesBoard
from introduction_to_AI.models.state import State


class TilesGameState(State, TilesBoard):
    """Tiles Game State Suit Class"""
    def __init__(self, board, size):
        super().__init__(board_config=board, size=size)

    def get_key(self):
        return str(self.board)

    def get_value(self):
        return self.board

    def display(self):
        return self._display()

    def __repr__(self):
        return f"<TilesGameState: {self.get_key()}>"
