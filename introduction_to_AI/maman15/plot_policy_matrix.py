"""
Author: Omer Shraibshtein (205984271)
Date:   10/06/2026
Email:  omershreib@gmail.com
"""

import matplotlib.pyplot as plt
import numpy as np


ARROW_MAP = {
    '^': '↑',
    'v': '↓',
    '<': '←',
    '>': '→'
}

def prettify_for_display(symbol):
    result = symbol

    for old, new in ARROW_MAP.items():
        result = result.replace(old, new).replace("+", "")

    return result

def plot_policy_matrix(
        policy_matrix,
        filename,
        title="Policy",
        blocked_symbol="X",
        terminal_symbol="O"):
    """
    policy_matrix : 2D numpy array of strings

    Example cell values:
        "^"
        ">"
        "<+v"
        "O"
        "X"
    """

    rows, cols = policy_matrix.shape

    fig, ax = plt.subplots(figsize=(cols, rows))

    # Draw white background
    ax.imshow(
        np.zeros((rows, cols)),
        cmap="Greys",
        vmin=0,
        vmax=1
    )

    # Draw grid
    ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which="minor", color="black", linewidth=1)

    ax.tick_params(which="minor", bottom=False, left=False)

    # Draw symbols
    for row in range(rows):
        for col in range(cols):

            symbol = str(policy_matrix[row, col])

            color = "blue" if "+" in symbol else "black"

            if symbol == blocked_symbol:
                ax.add_patch(
                    plt.Rectangle(
                        (col - 0.5, row - 0.5),
                        1,
                        1,
                        color="black"
                    )
                )

            elif symbol == terminal_symbol:
                ax.add_patch(
                    plt.Rectangle(
                        (col - 0.5, row - 0.5),
                        1,
                        1,
                        color="lightgreen"
                    )
                )

            ax.text(
                col,
                row,
                prettify_for_display(symbol),
                ha="center",
                va="center",
                fontsize=16,
                fontweight="bold",
                color=color
            )

    ax.set_title(title)

    ax.set_xticks(range(cols))
    ax.set_yticks(range(rows))

    #plt.colorbar()
    plt.savefig(filename + '.jpg')

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    policy_matrix = np.array([
        ["O", ">", ">", ">", "O"],
        ["v", "v+>", ">", "^", "^"],
        ["v", "v", "X", "O", "^"],
        ["v", "<+v", "<", "<", "^"],
        ["O", "<", "<", "<", "O"]
    ], dtype=object)

    plot_policy_matrix(policy_matrix, "Optimal Policy")