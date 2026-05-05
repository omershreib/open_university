from introduction_to_AI.agents import *
from introduction_to_AI.maman13 import ReversiGameProblem
from introduction_to_AI.maman13.reversi_evaluators import ReversiEvaluator


def reversi_agent_factory(agent_type,
                          player: int,
                          evaluator: ReversiEvaluator,
                          depth: int = 2):

    print(agent_type, MinMaxAgent)

    if agent_type == MinMaxAgent:
        return MinMaxAgent(problem=ReversiGameProblem(),
                           evaluator=evaluator,
                           player=player,
                           depth=depth)

    raise Exception(f"reversi factory not supports {agent_type}")
