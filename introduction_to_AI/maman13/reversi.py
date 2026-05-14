"""
Author: Omer Shraibshtein (205984271)
Date:   14/05/2026
Email:  omershreib@gmail.com
"""

from introduction_to_AI.maman13.reversi_args_parser import parse_n_args
from introduction_to_AI.maman13.reversi_agents_factory import reversi_agent_factory
from introduction_to_AI.maman13.reversi_runner import ReversiGameRunner
from introduction_to_AI.maman13.reversi_cdp import ColorDiskPlayer


def reversi_main(verbose, methodical, red_agent_type, white_agent_type, ahead, graphic):
    print(f"verbose={verbose}, "
          f"methodical={methodical}, "
          f"red_agent={red_agent_type}, "
          f"white_agent={white_agent_type}, "
          f"ahead={ahead}, "
          f"graphic={graphic}")



    red_agent = reversi_agent_factory(agent_type=red_agent_type,
                                      player=ColorDiskPlayer.RED.value,
                                      depth=ahead)

    white_agent = reversi_agent_factory(agent_type=white_agent_type,
                                      player=ColorDiskPlayer.WHITE.value,
                                      depth=ahead)

    game = ReversiGameRunner(
        board_size=8,
        red_agent=red_agent,
        white_agent=white_agent,
        verbose=verbose,
        methodical=methodical,
        use_gui=graphic,
        gui_delay=0.03)

    game.play()


if __name__ == '__main__':
    reversi_main(*parse_n_args())

# run examples:
# python -m introduction_to_AI.maman13.reversi -v -red 'heuristic_score' -white 'hungry_score' --ahead 4 -g