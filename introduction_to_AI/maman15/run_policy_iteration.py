from utils import *
from policy_iteration import policy_iteration
from policy_translation import policy_translation
from plot_value_iteration import plot_value_iteration
from plot_policy_matrix import plot_policy_matrix
from pprint import pprint
import numpy as np


def run_policy_iteration(mdp,
                         init_mode,
                         value_plot_filename,
                         policy_plot_filename,
                         value_plot_title,
                         policy_plot_title,
                         value_matrix_filename,
                         policy_matrix_filename):

    num_iterations, utilities, policy_dict = policy_iteration(
        mdp,
        init_mode=init_mode
    )

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

    np.save(value_matrix_filename, utilities_matrix)
    np.save(policy_matrix_filename, policy_matrix)

    plot_value_iteration(
        num_iterations,
        utilities_matrix,
        filename=value_plot_filename,
        title=value_plot_title
    )

    plot_policy_matrix(
        policy_matrix,
        filename=policy_plot_filename,
        title=policy_plot_title
    )