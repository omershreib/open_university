"""
Author: Omer Shraibshtein (205984271)
Date:   10/06/2026
Email:  omershreib@gmail.com
"""

from run_value_iteration import run_value_iteration
from utils import string_float
from mdp import MDP


def run_question_2(**kwargs):
    # === Question 2.a setup ===
    figures_folder = kwargs.get("figures_folder")
    numpy_results_folder = kwargs.get("numpy_results_folder")
    student_name = kwargs.get("student_name")
    datafile = kwargs.get("datafile")
    epsilon = kwargs.get("epsilon")

    print("Run Question 2.a\n")
    value_plot_filename = f"{figures_folder}/ValueIteration_Values_{student_name}"
    value_plot_title = "Value Iteration: {i}\n" + student_name
    value_matrix_filename = f"{numpy_results_folder}/value_matrix_2a"

    policy_plot_filename = f"{figures_folder}/ValueIteration_Policy_{student_name}"
    policy_plot_title = f"Policy Matrix For Question 2.a\n{student_name}"
    policy_matrix_filename = f"{numpy_results_folder}/policy_matrix_2a"



    mdp = MDP(datafile=datafile, gamma=0.9, p=0.8)

    run_value_iteration(mdp=mdp,
                        epsilon=epsilon,
                        value_plot_filename=value_plot_filename,
                        value_plot_title=value_plot_title,
                        policy_plot_filename=policy_plot_filename,
                        policy_plot_title=policy_plot_title,
                        value_matrix_filename=value_matrix_filename,
                        policy_matrix_filename=policy_matrix_filename)

    # === Question 2.b setup (changing gamma) ===
    for gamma in [0, 0.25, 0.5, 0.75, 1]:
        print(f"Run Question 2.b (gamma={gamma})\n")
        mdp = MDP(datafile=datafile, gamma=gamma, p=0.8)

        string_float_gamma = string_float(mdp.gamma)
        value_plot_filename = f"{figures_folder}/ValueIteration_Values_gamma{string_float_gamma}_{student_name}"
        value_plot_title = "Value Iteration: {i} (Gamma=" + str(mdp.gamma) + ")\n" + student_name
        value_matrix_filename = f"{numpy_results_folder}/value_matrix_2b_gamma{string_float_gamma}"

        policy_plot_filename = f"{figures_folder}/ValueIteration_Policy_gamma{string_float_gamma}_{student_name}"
        policy_plot_title = f"Policy Matrix (Gamma={string_float_gamma})\n{student_name}"
        policy_matrix_filename = f"{numpy_results_folder}/policy_matrix_2b_gamma{string_float_gamma}"

        run_value_iteration(mdp=mdp,
                            epsilon=epsilon,
                            value_plot_filename=value_plot_filename,
                            value_plot_title=value_plot_title,
                            policy_plot_filename=policy_plot_filename,
                            policy_plot_title=policy_plot_title,
                            value_matrix_filename=value_matrix_filename,
                            policy_matrix_filename=policy_matrix_filename)

    # === Question 2.c setup (changing p) ===
    for prob in [0.4, 0.6, 0.8, 1]:
        print(f"Run Question 2.c (p={prob})\n")
        mdp = MDP(datafile=datafile, gamma=0.9, p=prob)

        string_float_p = string_float(mdp.p)
        value_plot_filename = f"{figures_folder}/ValueIteration_Values_p{string_float_p}_{student_name}"
        value_plot_title = "Value Iteration: {i} (P=" + str(mdp.p) + ")\n" + student_name
        value_matrix_filename = f"{numpy_results_folder}/value_matrix_2c_p{string_float_p}"

        policy_plot_filename = f"{figures_folder}/ValueIteration_Policy_p{string_float_p}_{student_name}"
        policy_plot_title = f"Policy Matrix (P={string_float_p})\n{student_name}"
        policy_matrix_filename = f"{numpy_results_folder}/policy_matrix_2c_p{string_float_p}"

        run_value_iteration(mdp=mdp,
                            epsilon=epsilon,
                            value_plot_filename=value_plot_filename,
                            value_plot_title=value_plot_title,
                            policy_plot_filename=policy_plot_filename,
                            policy_plot_title=policy_plot_title,
                            value_matrix_filename=value_matrix_filename,
                            policy_matrix_filename=policy_matrix_filename)
