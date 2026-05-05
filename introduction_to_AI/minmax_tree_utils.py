from __future__ import annotations

from typing import Optional
import math
from .models.problem import Problem
from .models.state import State
from .models.move import Move
from .models.evaluator import Evaluator



def alphabeta_decision(problem: Problem, state: State, depth: int, evaluator: Evaluator) -> Move:
    root_player = state.player_turn
    best_move = None
    best_value = -math.inf
    alpha = -math.inf
    beta = math.inf

    for move in problem.get_actions(state):
        next_state = problem.update(state, move)
        value = alphabeta_value(problem, next_state, depth - 1, alpha, beta, root_player, evaluator)
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, best_value)

    # should never be None because actions() always returns at least PASS
    return best_move if best_move is not None else Move.pass_move()


def alphabeta_value(problem: Problem, state: State, depth: int, alpha: float, beta: float,
                    root_player, evaluator: Evaluator) -> float:
    if depth == 0:
        return evaluator.evaluate(state, root_player)

    player = state.player_turn
    moves = problem.get_actions(state)

    is_max = (player == root_player)
    if is_max:
        max_value = -math.inf
        for move in moves:
            max_value = max(max_value,
                            alphabeta_value(problem, problem.update(state, move), depth - 1, alpha, beta, root_player,
                                            evaluator))
            alpha = max(alpha, max_value)
            if alpha >= beta:
                break
        return max_value
    else:
        min_value = math.inf
        for move in moves:
            min_value = min(min_value,
                            alphabeta_value(problem, problem.update(state, move), depth - 1, alpha, beta, root_player,
                                            evaluator))
            beta = min(beta, min_value)
            if alpha >= beta:
                break

        return min_value
