"""
Author: Omer Shraibshtein (205984271)
Date:   14/05/2026
Email:  omershreib@gmail.com
"""

from introduction_to_AI.agents import *
from introduction_to_AI.maman13.reversi_agents import ReversiHungryScoreAgent
from introduction_to_AI.maman13.reversi_game_problem import ReversiGameProblem
from introduction_to_AI.maman13.reversi_evaluators import ReversiScoreEvaluator


def reversi_agent_factory(agent_type, player: int, depth: int = 2):

    if agent_type == 'hungry_score':
        return ReversiHungryScoreAgent(problem=ReversiGameProblem())

    if agent_type == 'heuristic_score':
        return MinMaxAgent(problem=ReversiGameProblem(),
                           evaluator=ReversiScoreEvaluator(),
                           player=player,
                           depth=depth)

    raise Exception(f"reversi factory not supports {agent_type}")
