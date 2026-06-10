"""
Author: Omer Shraibshtein (205984271)
Date:   10/06/2026
Email:  omershreib@gmail.com
"""

from utils import *

def policy_evaluation(policy, utilities, mdp, iterations=20):
    """
    Approximate policy evaluation.

    Updates U according to the current policy:
        U[s] = Q_VALUE(mdp, s, policy[s], U)
    """


    for _ in range(iterations):
        new_utilities = utilities.copy()

        for state_key, action in policy.items():
            pos = state_key_to_pos(state_key)

            if not mdp.is_valid_pos(pos):
                continue

            new_utilities[state_key] = q_value(mdp, pos, action, utilities)

        utilities = new_utilities

    return utilities