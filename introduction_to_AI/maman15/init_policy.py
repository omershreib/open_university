"""
Author: Omer Shraibshtein (205984271)
Date:   10/06/2026
Email:  omershreib@gmail.com
"""

from utils import *

def init_policy_up(mdp):
    policy = {}
    utilities = init_utilities(mdp, {})

    for state_key in utilities.keys():
        pos = state_key_to_pos(state_key)

        if not mdp.is_valid_pos(pos) or mdp.is_terminal_pos(pos):
            continue

        valid_actions = mdp.get_actions(pos)

        if len(valid_actions) == 0:
            continue

        chosen_action = None

        for candidate_action in SORTED_ACTIONS:
            for valid_action in valid_actions:
                if same_action(candidate_action, valid_action):
                    chosen_action = valid_action
                    break

            if chosen_action is not None:
                break

        policy[state_key] = chosen_action

    return policy