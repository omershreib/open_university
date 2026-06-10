"""
Author: Omer Shraibshtein (205984271)
Date:   10/06/2026
Email:  omershreib@gmail.com
"""

from utils import *


def simplified_value_iteration(mdp, policy, epsilon=0.01):
    """
    Policy Evaluation stage.

    Runs:
        U[s] = q_value(mdp, s, policy[s], U)

    repeatedly until convergence.
    """

    utilities = init_utilities(mdp, {})
    threshold = stop_condition(mdp.gamma, epsilon)

    num_svi_iterations = 0

    while True:
        num_svi_iterations += 1
        delta = 0

        old_utilities = utilities.copy()

        for state_key, action in policy.items():
            pos = state_key_to_pos(state_key)

            if not mdp.is_valid_pos(pos) or mdp.is_terminal_pos(pos):
                continue

            utilities[state_key] = q_value(
                mdp,
                pos,
                action,
                old_utilities
            )

            delta = max(
                delta,
                abs(utilities[state_key] - old_utilities[state_key])
            )

        if delta <= threshold:
            break

    return utilities, num_svi_iterations
