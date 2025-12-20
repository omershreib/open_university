from __future__ import annotations
import math
import random
from models import Move, ColorDiscPlayer
from game_state import GameState
from evaluators import Evaluator, ScoreEvaluator


class ReversiAgent:
    def choose_move(self, state: GameState) -> Move:
        raise NotImplementedError


class RandomAgent(ReversiAgent):
    def __init__(self, seed: int | None = None):
        self._random = random.Random(seed)

    def choose_move(self, state: GameState) -> Move:
        moves = state.actions()
        if moves:
            return self._random.choice(moves)

        return Move.pass_move()


# --------- Alpha-Beta (depth-limited minimax) ---------

def alphabeta_decision(state: GameState, depth: int, evaluator: Evaluator) -> Move:
    root_player = state.player_turn
    best_move = None
    best_val = -math.inf
    alpha = -math.inf
    beta = math.inf

    for move in state.actions():
        nxt = state.movement_result(move)
        val = alphabeta_value(nxt, depth - 1, alpha, beta, root_player, evaluator)
        if val > best_val:
            best_val = val
            best_move = move
        alpha = max(alpha, best_val)

    # should never be None because actions() always returns at least PASS
    return best_move if best_move is not None else Move.pass_move()


def alphabeta_value(state: GameState, depth: int, alpha: float, beta: float,
                    root_player: ColorDiscPlayer, evaluator: Evaluator) -> float:
    if state.is_terminal():
        # terminal utility: disc difference for root_player
        return state.board.calc_score(root_player) - state.board.calc_score(root_player.opposition())

    if depth == 0:
        return evaluator.evaluate(state, root_player)

    to_move = state.player_turn
    moves = state.actions()

    is_max = (to_move == root_player)
    if is_max:
        v = -math.inf
        for m in moves:
            v = max(v, alphabeta_value(state.movement_result(m), depth - 1, alpha, beta, root_player, evaluator))
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v
    else:
        v = math.inf
        for m in moves:
            v = min(v, alphabeta_value(state.movement_result(m), depth - 1, alpha, beta, root_player, evaluator))
            beta = min(beta, v)
            if alpha >= beta:
                break
        return v


class AlphaBetaAgent(ReversiAgent):
    def __init__(self, depth: int = 3, evaluator: Evaluator | None = None):
        self.depth = depth
        self.evaluator = evaluator if evaluator is not None else ScoreEvaluator()

    def choose_move(self, state: GameState) -> Move:
        return alphabeta_decision(state, self.depth, self.evaluator)
