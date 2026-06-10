from run_policy_iteration import run_policy_iteration
from utils import string_float
from mdp import MDP


def run_question_3(**kwargs):
    figures_folder = kwargs.get("figures_folder")
    numpy_results_folder = kwargs.get("numpy_results_folder")
    student_name = kwargs.get("student_name")
    datafile = kwargs.get("datafile")

    #epsilon = 1
    epsilon = 0.001

    # === Question 3: Policy Iteration ===
    print("Run Question 3 - Policy Iteration\n")

    mdp = MDP(datafile=datafile, gamma=0.9, p=0.8)

    value_plot_filename = f"{figures_folder}/PolicyIteration_Values_{student_name}"
    value_plot_title = "Policy Iteration: {i}\n" + student_name
    value_matrix_filename = f"{numpy_results_folder}/value_matrix_3"

    policy_plot_filename = f"{figures_folder}/PolicyIteration_Policy_{student_name}"
    policy_plot_title = f"Policy Matrix For Question 3\n{student_name}"
    policy_matrix_filename = f"{numpy_results_folder}/policy_matrix_3"

    svi_plot_filename = f"{figures_folder}/PolicyIteration_SVI_Iterations_{student_name}"
    svi_plot_title = f"Policy Iteration - Simplified Value Iteration Count\n{student_name}"
    svi_history_filename = f"{numpy_results_folder}/svi_iterations_history_3"

    run_policy_iteration(
        mdp=mdp,
        epsilon=epsilon,
        value_plot_filename=value_plot_filename,
        value_plot_title=value_plot_title,
        policy_plot_filename=policy_plot_filename,
        policy_plot_title=policy_plot_title,
        value_matrix_filename=value_matrix_filename,
        policy_matrix_filename=policy_matrix_filename,
        svi_plot_filename=svi_plot_filename,
        svi_plot_title=svi_plot_title,
        svi_history_filename=svi_history_filename
    )

