from introduction_to_AI.maman13.reversi_args_parser import parse_n_args
from introduction_to_AI.maman13.reversi_agents_factory import reversi_agent_factory
from introduction_to_AI.maman13.reversi_evaluators import ReversiScoreEvaluator
from introduction_to_AI.agents import *
from introduction_to_AI.maman13.reversi_runner import ReversiGameRunner
from introduction_to_AI.maman13.reversi_cdp import ColorDiskPlayer


def reversi_main(verbose, methodical, red_agent, white_agent, ahead, graphic):
    print(f"verbose={verbose}, "
          f"methodical={methodical}, "
          f"red_agent={red_agent}, "
          f"white_agent={white_agent}, "
          f"ahead={ahead}, "
          f"graphic={graphic}")

    exit()


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
        use_gui=False,
        gui_delay=0.02)

    game.play()


if __name__ == '__main__':
    import sys
    print(sys.path)
    exit()
    #reversi_main(True, 'A', 'B', 2, 2, False)
    reversi_main(*parse_n_args())
