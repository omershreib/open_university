from introduction_to_AI.agents import *
from introduction_to_AI.maman13.reversi_agents import ReversiHungryScoreAgent
from introduction_to_AI.maman13.reversi_game_problem import ReversiGameProblem
from introduction_to_AI.maman13.reversi_evaluators import ReversiEvaluator


def reversi_agent_factory(agent_type,
                          player: int,
                          evaluator: ReversiEvaluator,
                          depth: int = 2):
    if agent_type == ReversiHungryScoreAgent:
        return ReversiHungryScoreAgent(problem=ReversiGameProblem())

    if agent_type == MinMaxAgent:
        return MinMaxAgent(problem=ReversiGameProblem(),
                           evaluator=evaluator,
                           player=player,
                           depth=depth)

    raise Exception(f"reversi factory not supports {agent_type}")
