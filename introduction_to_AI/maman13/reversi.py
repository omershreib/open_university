from introduction_to_AI.maman13.reversi_args_parser import parse_n_args
from introduction_to_AI.maman13 import reversi_agent_factory
from introduction_to_AI.maman13.reversi_evaluators import ReversiScoreEvaluator
from introduction_to_AI.agents import *
from introduction_to_AI.maman13 import ReversiGameRunner, ColorDiskPlayer


def reversi_main(num, display_all_actions, methodical, red_agent, white_agent, ahead):
    print(num, display_all_actions, methodical, red_agent, white_agent, ahead)

    red_agent = reversi_agent_factory(MinMaxAgent,
                                      ColorDiskPlayer.RED.value,
                                      ReversiScoreEvaluator())

    white_agent = reversi_agent_factory(MinMaxAgent,
                                        ColorDiskPlayer.WHITE.value,
                                        ReversiScoreEvaluator())

    game = ReversiGameRunner(
        board_size=8,
        red_agent=red_agent,
        white_agent=white_agent,
        verbose=True,
        use_gui=True,
        gui_delay=0.02)

    game.play()


if __name__ == '__main__':
    reversi_main(5, True, 10, 'A', 'B', 2)
    #reversi_main(*parse_n_args())
