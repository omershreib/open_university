from __future__ import annotations
from typing import Optional
import math
import random
from models import Move, ColorDiscPlayer
from game_state import GameState
from evaluators import Evaluator, ScoreEvaluator


class ReversiAgent:
    def choose_move(self, state: GameState) -> Move:
        raise NotImplementedError


class RandomAgent(ReversiAgent):
    def __init__(self, seed: Optional[int] = None):
        self._random = random.Random(seed)

    def choose_move(self, state: GameState) -> Move:
        moves = state.actions()
        if moves:
            return self._random.choice(moves)

        return Move.pass_move()


class DeterministicAgent(ReversiAgent):

    def choose_move(self, state: GameState) -> Move:
        moves = state.actions()
        if moves:
            return moves[0]

        return Move.pass_move()


class HungryAgent(ReversiAgent):
    def choose_move(self, state: GameState) -> Move:
        agent_player = state.player_turn
        moves = state.actions()
        if not moves:
            return Move.pass_move()

        # best means the move that cause to the most increase in player score
        max_score = 0
        best_move = None

        if moves:
            for move in moves:
                move_state = state.update(move)
                move_score = move_state.score(agent_player)

                if move_score > max_score:
                    max_score = max_score
                    best_move = move

        return best_move


def alphabeta_decision(state: GameState, depth: int, eval_function: Evaluator) -> Move:
    root_player = state.player_turn
    best_move = None
    best_value = -math.inf
    alpha = -math.inf
    beta = math.inf

    for move in state.actions():
        next_state = state.update(move)
        value = alphabeta_value(next_state, depth - 1, alpha, beta, root_player, eval_function)
        if value > best_value:
            best_value = value
            best_move = move
        alpha = max(alpha, best_value)

    # should never be None because actions() always returns at least PASS
    return best_move if best_move is not None else Move.pass_move()


def alphabeta_value(state: GameState, depth: int, alpha: float, beta: float,
                    root_player: ColorDiscPlayer, eval_function: Evaluator) -> float:

    if depth == 0:
        return eval_function.evaluate(state, root_player)

    player = state.player_turn
    moves = state.actions()

    is_max = (player == root_player)
    if is_max:
        max_value = -math.inf
        for move in moves:
            max_value = max(max_value,
                            alphabeta_value(state.update(move), depth - 1, alpha, beta, root_player, eval_function))
            alpha = max(alpha, max_value)
            if alpha >= beta:
                break
        return max_value
    else:
        min_value = math.inf
        for move in moves:
            min_value = min(min_value,
                            alphabeta_value(state.update(move), depth - 1, alpha, beta, root_player, eval_function))
            beta = min(beta, min_value)
            if alpha >= beta:
                break

        return min_value


class HeuristicAgent(ReversiAgent):
    def __init__(self, evaluator: Evaluator, depth: int = 0):
        self.eval_function = evaluator
        self.depth = depth

    def choose_move(self, state: GameState) -> Move:
        return alphabeta_decision(state, self.depth, self.eval_function)


