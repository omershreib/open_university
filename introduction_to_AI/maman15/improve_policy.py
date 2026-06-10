"""
Author: Omer Shraibshtein (205984271)
Date:   10/06/2026
Email:  omershreib@gmail.com
"""

from utils import *


def improve_policy(mdp, policy, utilities):
    """
    Policy Improvement stage.

    Returns:
        True  if policy did not change
        False if policy changed
    """

    unchanged = True

    for state_key in list(policy.keys()):
        pos = state_key_to_pos(state_key)

        if not mdp.is_valid_pos(pos) or mdp.is_terminal_pos(pos):
            continue

        old_action = policy[state_key]

        best_actions = []
        best_qvalue = float("-inf")

        for action in mdp.get_actions(pos):
            curr_qvalue = q_value(mdp, pos, action, utilities)

            if curr_qvalue > best_qvalue:
                best_qvalue = curr_qvalue
                best_actions = [action]

            elif curr_qvalue == best_qvalue:
                best_actions.append(action)

        # choose first action according to systematic order: UP, DOWN, RIGHT, LEFT
        chosen_action = None

        for candidate_action in SORTED_ACTIONS:
            for best_action in best_actions:
                if same_action(candidate_action, best_action):
                    chosen_action = best_action
                    break

            if chosen_action is not None:
                break

        if not same_action(old_action, chosen_action):
            policy[state_key] = chosen_action
            unchanged = False

    return unchanged
