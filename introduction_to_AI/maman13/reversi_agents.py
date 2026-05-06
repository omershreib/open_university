from __future__ import annotations

from introduction_to_AI.agents import HungryAgent
from introduction_to_AI.maman13.reversi_game_problem import ReversiGameProblem
from introduction_to_AI.maman13.reversi_game_state import ReversiGameState
from introduction_to_AI.maman13.reversi_move import ReversiMove


class ReversiHungryScoreAgent(HungryAgent):

    def __init__(self, problem: ReversiGameProblem):
        super().__init__(problem)

    def choose_move(self, state: ReversiGameState) -> ReversiMove:
        agent_player = state.player_turn
        moves = self.problem.get_actions(state)
        if moves[0] == ReversiMove.pass_move():
            return ReversiMove.pass_move()

        # best means the move that cause to the most increase in player score
        max_score = 0
        best_move = None

        if moves:
            for move in moves:
                move_state = self.problem.update(state, move)
                move_score = move_state.score(agent_player)

                if move_score > max_score:
                    max_score = max_score
                    best_move = move

        return best_move
