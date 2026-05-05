from reversi_main_utils import parse_n_args



def reversi_main(num, display_all_actions, methodical, red_agent, white_agent, ahead):
    print(num, display_all_actions, methodical, red_agent, white_agent, ahead)


if __name__ == '__main__':
    reversi_main(*parse_n_args())