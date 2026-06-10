"""
Author: Omer Shraibshtein (205984271)
Date:   10/06/2026
Email:  omershreib@gmail.com
"""

from utils import *


def get_stop_condition(gamma, epsilon):
    if gamma == 0:
        return float("inf")   # stop after one iteration

    if gamma == 1:
        return epsilon        # no AIMA discounted bound

    return epsilon * (1 - gamma) / gamma


def value_iteration(mdp, epsilon=1, max_iters=10_000):
    print(f"run value_iteration with epsilon={epsilon}")

    U_prime = init_utilities(mdp, {})
    policy_dict = {}

    #stop_condition = epsilon * (1 - mdp.gamma) / mdp.gamma
    stop_condition = get_stop_condition(mdp.gamma, epsilon)
    index = 0

    while index < max_iters:
        index += 1
        print(f"value iteration #{index}")

        U = U_prime.copy()
        delta = 0

        for state_key in list(U.keys()):
            pos = state_key_to_pos(state_key)

            if not mdp.is_updatable_pos(pos):
                continue

            best_actions = []
            best_value = float("-inf")

            for action in mdp.get_actions(pos):
                curr_value = q_value(mdp, pos, action, U)

                if curr_value == best_value:
                    best_actions.append(action)

                if curr_value > best_value:
                    best_value = curr_value
                    best_actions = []
                    best_actions.append(action)

            U_prime[state_key] = best_value
            policy_dict[state_key] = best_actions

            delta = max(delta, abs(U_prime[state_key] - U[state_key]))

        print(f"delta: {delta} ; stop-condition (<=) {stop_condition}")

        if delta <= stop_condition:
            break

    return index, U_prime, policy_dict
