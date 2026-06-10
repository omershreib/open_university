"""
Author: Omer Shraibshtein (205984271)
Date:   10/06/2026
Email:  omershreib@gmail.com
"""

from init_policy import init_policy_up
from simplified_value_iteration import simplified_value_iteration
from improve_policy import improve_policy


def policy_iteration(mdp, epsilon=0.01):
    """
    Full Policy Iteration according to the homework requirements.

    Each outer iteration contains:
        1. Policy Evaluation using Simplified Value Iteration
        2. Policy Improvement

    After every policy improvement, expected utilities are reset to 0
    automatically because simplified_value_iteration creates a fresh utilities
    dictionary each time.
    """

    policy = init_policy_up(mdp)

    num_policy_iterations = 0
    svi_iterations_history = []

    while True:
        num_policy_iterations += 1

        print(f"policy iteration #{num_policy_iterations}")

        utilities, num_svi_iterations = simplified_value_iteration(
            mdp,
            policy,
            epsilon=epsilon
        )

        svi_iterations_history.append(num_svi_iterations)

        print(f"simplified value iteration iterations: {num_svi_iterations}")

        unchanged = improve_policy(
            mdp,
            policy,
            utilities
        )

        if unchanged:
            break

    return num_policy_iterations, utilities, policy, svi_iterations_history
