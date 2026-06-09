from utils import *
from policy_evaluation import policy_evaluation
import random


def init_random_policy(mdp):
    policy = {}

    utilities = init_utilities(mdp, {})

    for state_key in utilities.keys():
        pos = state_key_to_pos(state_key)

        if not mdp.is_valid_pos(pos):
            continue

        actions = mdp.get_actions(pos)

        if len(actions) > 0:
            policy[state_key] = random.choice(actions)

    return policy


def policy_iteration(mdp, evaluation_iterations=20):
    utilities = init_utilities(mdp, {})
    policy = init_random_policy(mdp)

    index = 0

    while True:
        index += 1
        print(f"policy iteration #{index}")

        utilities = policy_evaluation(
            policy,
            utilities,
            mdp,
            iterations=evaluation_iterations
        )

        unchanged = True

        for state_key in list(policy.keys()):
            pos = state_key_to_pos(state_key)

            if not mdp.is_valid_pos(pos):
                continue

            old_action = policy[state_key]
            old_qvalue = q_value(mdp, pos, old_action, utilities)

            best_action = old_action
            best_qvalue = old_qvalue

            for action in mdp.get_actions(pos):
                curr_qvalue = q_value(mdp, pos, action, utilities)

                if curr_qvalue > best_qvalue:
                    best_qvalue = curr_qvalue
                    best_action = action

            if best_action != old_action:
                policy[state_key] = best_action
                unchanged = False

        if unchanged:
            break

    return utilities, policy
