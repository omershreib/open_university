import numpy as np
from pprint import pprint
from .mdp import MDP
from .value_iteration import value_iteration
from .plot_value_iteration import plot_value_iteration
from .policy_translation import policy_translation
from .utils import *

if __name__ == '__main__':

    EPSILON = 10

    mdp = MDP(datafile='maman15/input0.npz', gamma=0.9, p=0.8)

    print("\n=== states ===")
    pprint(mdp.states)

    print("\n=== rewards ===")
    pprint(mdp.rewards)

    num_iterations, utilities, policy_dict = value_iteration(mdp, epsilon=EPSILON)

    utilities_matrix = np.empty(mdp.shape)
    policy_matrix = np.empty(mdp.shape, dtype=object)

    for key, value in utilities.items():
        pos = state_key_to_pos(key)
        utilities_matrix[*pos] = value

    for x in range(mdp.shape[0]):
        for y in range(mdp.shape[1]):
            pos = [x, y]
            pos_policy = policy_translation(mdp, pos, None)

            if pos_policy is not None:
                policy_matrix[*pos] = pos_policy

    for key, actions in policy_dict.items():
        pos = state_key_to_pos(key)

        pos_policy = policy_translation(mdp, pos, actions)
        policy_matrix[*pos] = pos_policy

    print("\n=== UTILITY MATRIX ===")
    pprint(utilities_matrix)

    print("\n=== POLICY MATRIX ===")
    pprint(policy_matrix)

    np.save("utilities_matrix_input0", utilities_matrix)
    np.save("policy_matrix_input0", policy_matrix)

    plot_value_iteration(num_iterations, utilities_matrix, f"figures/input0_eps_{EPSILON}_")



