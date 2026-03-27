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


# todo: likely not admissible
class TilesWrongNeighbors(Evaluator):

    @staticmethod
    def build_reduction_grid(board: List[List[int]]) -> List[List[Optional[Any]]]:
        """
        Wrap an n x n tiles grid with one extra outer layer.

        Example for n=3 and board:
            [[0, 1, 2],
             [3, 4, 5],
             [6, 7, 8]]

        returns:
            [
                [None, 'a', 'b', 'c', None],
                ['l',     0,   1,   2, 'd'],
                ['k',     3,   4,   5, 'e'],
                ['j',     6,   7,   8, 'f'],
                [None, 'i', 'h', 'g', None],
            ]
        """
        n = len(board)
        if n == 0 or any(len(row) != n for row in board):
            raise ValueError("board must be a non-empty square grid")

        # number of border labels needed = 4 * n
        border_labels = [chr(ord("a") + i) for i in range(4 * n)]

        top = border_labels[:n]
        right = border_labels[n:2 * n]
        bottom = border_labels[2 * n:3 * n][::-1]
        left = border_labels[3 * n:4 * n][::-1]

        reduced = [[None for _ in range(n + 2)] for _ in range(n + 2)]

        # top / bottom
        for j in range(n):
            reduced[0][j + 1] = top[j]
            reduced[n + 1][j + 1] = bottom[j]

        # left / right
        for i in range(n):
            reduced[i + 1][0] = left[i]
            reduced[i + 1][n + 1] = right[i]

        # inner board
        for i in range(n):
            for j in range(n):
                reduced[i + 1][j + 1] = board[i][j]

        return reduced

    @staticmethod
    def get_neighbors_from_reduction_grid(reduced_grid: List[List[Optional[Any]]], tile: int) -> Tuple[
        Any, Any, Any, Any]:
        """
        Return (left, right, up, down) neighbors of `tile` in the reduced grid.

        Example:
            tile = 2
            returns (1, 'd', 'c', 5)
        """
        rows = len(reduced_grid)
        cols = len(reduced_grid[0]) if rows else 0

        tile_pos = None
        for i in range(rows):
            for j in range(cols):
                if reduced_grid[i][j] == tile:
                    tile_pos = (i, j)
                    break
            if tile_pos is not None:
                break

        if tile_pos is None:
            raise ValueError(f"tile {tile} not found in reduced grid")

        i, j = tile_pos
        left = reduced_grid[i][j - 1]
        right = reduced_grid[i][j + 1]
        up = reduced_grid[i - 1][j]
        down = reduced_grid[i + 1][j]

        return left, right, up, down

    def evaluate(self, curr_state: TilesGameState, goal_state: TilesGameState):
        n = curr_state.size
        square_n = int(math.pow(n, 2))

        curr_reduction_grid = self.build_reduction_grid(curr_state.board)
        goal_reduction_grid = self.build_reduction_grid(goal_state.board)

        total_score = 0

        for i in range(1, square_n):
            for curr_dir, goal_dir in zip(self.get_neighbors_from_reduction_grid(curr_reduction_grid, i),
                                          self.get_neighbors_from_reduction_grid(goal_reduction_grid, i)):
                if curr_dir != goal_dir:
                    total_score += 1

        return total_score


class TilesMaxRowColAndWrongNeighbors(Evaluator):
    def evaluate(self, curr_state, goal_state):
        h1 = TilesRowColEvaluator().evaluate(curr_state, goal_state)
        h2 = TilesWrongNeighbors().evaluate(curr_state, goal_state)

        return max(h1, h2)


class TilesMaxRowColAndManhattan(Evaluator):
    def evaluate(self, curr_state, goal_state):
        h1 = TilesManhattanEvaluator().evaluate(curr_state, goal_state)
        h2 = TilesRowColEvaluator().evaluate(curr_state, goal_state)

        return max(h1, h2)


class TilesMaxManhattanAndWrongNeighbors(Evaluator):
    def evaluate(self, curr_state, goal_state):
        h1 = TilesManhattanEvaluator().evaluate(curr_state, goal_state)
        h2 = TilesWrongNeighbors().evaluate(curr_state, goal_state)

        return max(h1, h2)
        # return 4*max(h1, h2)
        # return 8*max(h1, h2)
        # return 16 * max(h1, h2)


class TilesMaxMisplacedAndWrongNeighbors(Evaluator):
    def evaluate(self, curr_state, goal_state):
        h1 = TilesMisplacedEvaluator().evaluate(curr_state, goal_state)
        h2 = TilesWrongNeighbors().evaluate(curr_state, goal_state)

        return max(h1, h2)
        # return h1 + 4*h2
        # return 16*max(h1, h2)
        # return 16*max(h1, h2)


class TilesMaxMispAndManhattan(Evaluator):
    def evaluate(self, curr_state: TilesGameState, goal_state: TilesGameState):
        h1 = TilesMisplacedEvaluator().evaluate(curr_state, goal_state)
        h2 = TilesManhattanEvaluator().evaluate(curr_state, goal_state)

        # excellent
        return max(h1, h2)
        # return h1 + 4*h2
        # return 16*max(h1, h2)
        # return 16 * max(h1, h2)
