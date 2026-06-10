"""
Author: Omer Shraibshtein (205984271)
Date:   10/06/2026
Email:  omershreib@gmail.com
"""
import matplotlib.pyplot as plt


def plot_policy_iteration_history(
        svi_iterations_history,
        filename,
        title):

    plt.figure(figsize=(8, 5))

    plt.plot(
        range(1, len(svi_iterations_history) + 1),
        svi_iterations_history,
        marker="o"
    )

    plt.xlabel("Policy Iteration Number")
    plt.ylabel("Simplified Value Iteration Iterations")
    plt.title(title)

    plt.grid(True)

    plt.savefig(filename, bbox_inches="tight")
    plt.close()