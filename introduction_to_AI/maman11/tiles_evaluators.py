from introduction_to_AI.models import Evaluator
from introduction_to_AI.maman11.tiles_game_state import TilesGameState


class TilesManhattanEvaluator(Evaluator):
    def evaluate(self, curr_state: TilesGameState, goal_state: TilesGameState) -> int:
        distance: int = 0

        for i in range(1, 9):
            curr_x, curr_y = curr_state.args_tile_pos(i)
            goal_x, goal_y = goal_state.args_tile_pos(i)
            distance += self._f(curr_x, goal_x, curr_y, goal_y)

        return distance

    @staticmethod
    def _f(x1, x2, y1, y2):
        return abs(x1 - x2) + abs(y1 - y2)
