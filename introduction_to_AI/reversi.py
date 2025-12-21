from runner import ReversiGameRunner
from agents import HungryAgent, HeuristicAgent
from evaluators import ScoreEvaluator

# Question - 1: game simulation using default agent
game = ReversiGameRunner(
    board_size=8,
    red_agent=HungryAgent(),
    white_agent=HungryAgent(),
    verbose=True,
    use_gui=True,
    gui_delay=0.02)


# Question - 2: game simulation using heuristic agents (no depth)
# game = ReversiGameRunner(
#     board_size=8,
#     red_agent=HeuristicAgent(evaluator=ScoreEvaluator()),
#     white_agent=HeuristicAgent(evaluator=ScoreEvaluator()),
#     verbose=True,
#     use_gui=True,
#     gui_delay=0.02)


# Question - 3: game simulation using heuristic agents (depth=2)
# game = ReversiGameRunner(
#     board_size=8,
#     red_agent=HeuristicAgent(evaluator=ScoreEvaluator(), depth=2),
#     white_agent=HeuristicAgent(evaluator=ScoreEvaluator(), depth=2),
#     verbose=True,
#     use_gui=True,
#     gui_delay=0.02)


if __name__ == "__main__":
    game.play()
