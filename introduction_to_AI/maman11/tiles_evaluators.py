import math

from typing import Any, Dict, List, Optional, Tuple
from introduction_to_AI.models.evaluator import Evaluator
from introduction_to_AI.maman11.tiles_game_state import TilesGameState
from introduction_to_AI.maman11.tile_movement import labels_to_directions
from introduction_to_AI.common import vector


class TilesManhattanEvaluator(Evaluator):
    def evaluate(self, curr_state: TilesGameState, goal_state: TilesGameState) -> int:
        distance: int = 0
        n = curr_state.size
        square_n = int(math.pow(n, 2))

        for i in range(1, square_n):
            curr_x, curr_y = curr_state.args_tile_pos(i)
            goal_x, goal_y = goal_state.args_tile_pos(i)
            distance += self._f(curr_x, goal_x, curr_y, goal_y)

        return distance

    @staticmethod
    def _f(x1, x2, y1, y2):
        return abs(x1 - x2) + abs(y1 - y2)


class TilesMisplacedEvaluator(Evaluator):
    def evaluate(self, curr_state: TilesGameState, goal_state: TilesGameState):
        count = 0
        n = curr_state.size
        for i in range(n):
            for j in range(n):
                if curr_state.board[i][j] != 0 and curr_state.board[i][j] != goal_state.board[i][j]:
                    count += 1
        return count


class TilesRowColEvaluator(Evaluator):
    def evaluate(self, curr_state: TilesGameState, goal_state: TilesGameState):
        n = curr_state.size
        square_n = int(math.pow(n, 2))
        score = 0

        for i in range(1, square_n):
            curr_x, curr_y = curr_state.args_tile_pos(i)
            goal_x, goal_y = goal_state.args_tile_pos(i)

            if curr_x != goal_x:
                score += 1

            if curr_y != goal_y:
                score += 1

        return score


class TilesMaxMDRowCol(Evaluator):
    def __init__(self):
        self.md_evaluator = TilesManhattanEvaluator()
        self.rowcol_evaluator = TilesRowColEvaluator()

    def evaluate(self, curr_state: TilesGameState, goal_state: TilesGameState):
        md = self.md_evaluator.evaluate(curr_state, goal_state)
        rowcol = self.rowcol_evaluator.evaluate(curr_state, goal_state)

        return max(md, rowcol)


class TilesLinearConflictEvaluator(Evaluator):
    def evaluate(self, curr_state: TilesGameState, goal_state: TilesGameState):
        n = curr_state.size
        square_n = n * n
        lc_counter = 0

        for i in range(1, square_n):
            i_curr_row, i_curr_col = curr_state.args_tile_pos(i)
            i_goal_row, i_goal_col = goal_state.args_tile_pos(i)

            for j in range(i + 1, square_n):
                j_curr_row, j_curr_col = curr_state.args_tile_pos(j)
                j_goal_row, j_goal_col = goal_state.args_tile_pos(j)

                # Row conflict:
                # same current row, both belong in that row,
                # but current order is reversed relative to goal order
                if (
                        i_curr_row == j_curr_row and
                        i_goal_row == i_curr_row and
                        j_goal_row == j_curr_row
                ):
                    if (i_curr_col < j_curr_col and i_goal_col > j_goal_col) or \
                            (i_curr_col > j_curr_col and i_goal_col < j_goal_col):
                        lc_counter += 1

                # Column conflict:
                # same current column, both belong in that column,
                # but current order is reversed relative to goal order
                if (
                        i_curr_col == j_curr_col and
                        i_goal_col == i_curr_col and
                        j_goal_col == j_curr_col
                ):
                    if (i_curr_row < j_curr_row and i_goal_row > j_goal_row) or \
                            (i_curr_row > j_curr_row and i_goal_row < j_goal_row):
                        lc_counter += 1

        return lc_counter


class TilesMDPlusLCEvaluator(Evaluator):
    def __init__(self):
        self.md_evaluator = TilesManhattanEvaluator()
        self.lc_evaluator = TilesLinearConflictEvaluator()

    def evaluate(self, curr_state: TilesGameState, goal_state: TilesGameState):
        md = self.md_evaluator.evaluate(curr_state, goal_state)
        lc = self.lc_evaluator.evaluate(curr_state, goal_state)
        return md + 2 * lc


# if __name__ == '__main__':
#     from tiles_main_utils import build_board
#
#     board = build_board([0, 7, 8, 2, 1, 5, 6, 4, 3])
#     state = TilesGameState(board=board, size=3)
#
#     goal_board = build_board([0, 1, 2, 3, 4, 5, 6, 7, 8])
#     goal_state = TilesGameState(board=goal_board, size=3)
#
#     print(TilesMDPlusLCEvaluator().evaluate(state, goal_state))
#     print(TilesManhattanEvaluator().evaluate(state, goal_state))