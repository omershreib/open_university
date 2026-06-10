from utils import *

# SORTED_ACTIONS = [UP, DOWN, RIGHT, LEFT]
#
# def same_action(a1, a2):
#     return np.array_equal(a1, a2)

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

# def init_policy(mdp, init_mode="UP"):
#     policy = {}
#     utilities = init_utilities(mdp, {})
#
#     for state_key in utilities.keys():
#         pos = state_key_to_pos(state_key)
#
#         if not mdp.is_valid_pos(pos) or mdp.is_terminal_pos(pos):
#             continue
#
#         valid_actions = mdp.get_actions(pos)
#
#         if len(valid_actions) == 0:
#             continue
#
#         if init_mode == "UP":
#             chosen_action = None
#
#             for candidate_action in SORTED_ACTIONS:
#                 for valid_action in valid_actions:
#                     if same_action(candidate_action, valid_action):
#                         chosen_action = valid_action
#                         break
#
#                 if chosen_action is not None:
#                     break
#
#             policy[state_key] = chosen_action
#
#         elif init_mode == "ZERO":
#             policy[state_key] = 0
#
#         else:
#             raise ValueError("init_mode must be 'UP' or 'ZERO'")
#
#     return policy