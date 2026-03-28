import matplotlib.pyplot as plt

# ['bfs', 'manhattan', 'misplaced', 'rowcol', 'lc', 'md_plus_lc', 'max_rowcol_man']

ALGORITHM_COLORS = {
    "bfs": "tab:blue",
    "manhattan": "tab:orange",
    "misplaced": "tab:green",
    "rowcol": "tab:red",
    "md_plus_lc": "tab:purple",
    "lc": "tab:brown",
    "max_rowcol_md": "tab:yellow"
}


def build_algorithm_colors(algorithm_order):
    cmap = plt.get_cmap("tab10")
    return {
        alg: cmap(i % 10)
        for i, alg in enumerate(algorithm_order)
    }

def _validate_performance_dict(performances: dict, name: str):
    if not isinstance(performances, dict):
        raise TypeError(f"{name} must be a dictionary")

    if not performances:
        raise ValueError(f"{name} is empty")

    required_keys = {"length", "expanded_nodes"}

    for alg, metrics in performances.items():
        if not isinstance(metrics, dict):
            raise TypeError(f"{name}['{alg}'] must be a dictionary")

        missing = required_keys - set(metrics.keys())
        if missing:
            raise ValueError(
                f"{name}['{alg}'] is missing required keys: {missing}"
            )


def _validate_same_algorithms(performance_dicts):
    base_algs = list(performance_dicts[0].keys())
    base_set = set(base_algs)

    for i, perf in enumerate(performance_dicts[1:], start=2):
        curr_set = set(perf.keys())
        if curr_set != base_set:
            raise ValueError(
                f"performances_{i} does not contain the same algorithms as performances_1.\n"
                f"performances_1: {sorted(base_set)}\n"
                f"performances_{i}: {sorted(curr_set)}"
            )

    return base_algs


def _plot_metric_subplot(ax, performances, metric, title, algorithm_order, log_scale=False):
    values = [performances[alg][metric] for alg in algorithm_order]
    colors = [ALGORITHM_COLORS.get(alg, "tab:gray") for alg in algorithm_order]

    bars = ax.bar(algorithm_order, values, color=colors)
    ax.set_title(title)
    ax.set_xlabel("Algorithm")
    ax.set_ylabel(metric.replace("_", " ").title())
    ax.tick_params(axis="x", rotation=30)

    if log_scale:
        ax.set_yscale("log")

    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            str(value),
            ha="center",
            va="bottom",
            fontsize=9,
        )
# def _plot_metric_subplot(ax, performances: dict, metric: str, title: str, algorithm_order, log_scale=False):
#     values = [performances[alg][metric] for alg in algorithm_order]
#
#     bars = ax.bar(algorithm_order, values)
#     ax.set_title(title)
#     ax.set_xlabel("Algorithm")
#     ax.set_ylabel(metric.replace("_", " ").title())
#     ax.tick_params(axis="x", rotation=30)
#
#     if log_scale:
#         ax.set_yscale("log")
#
#     for bar, value in zip(bars, values):
#         y = value
#         if log_scale and value > 0:
#             y = value
#
#         ax.text(
#             bar.get_x() + bar.get_width() / 2,
#             y,
#             str(value),
#             ha="center",
#             va="bottom",
#             fontsize=9,
#         )


def plot_results(
    performances_1: dict,
    performances_2: dict,
    performances_3: dict,
    performances_4: dict,
):
    """
    Plot 2 figures, each with 4 subplots (2x2), using the same algorithm order
    across all subplots.

    Parameters
    ----------
    performances_1, performances_2, performances_3, performances_4 : dict
        Each dictionary represents one starting board and must have this format:

        {
            'alg_name': {
                'length': path_length,
                'expanded_nodes': expanded_nodes
            },
            ...
        }

    Notes
    -----
    - Board 1 is assumed easiest
    - Board 4 is assumed hardest
    - The algorithm list is dynamic
    - All 4 dictionaries must contain the same set of algorithm names
    - The plotting order is taken from performances_1
    """

    performance_dicts = [
        performances_1,
        performances_2,
        performances_3,
        performances_4,
    ]

    for i, perf in enumerate(performance_dicts, start=1):
        _validate_performance_dict(perf, f"performances_{i}")

    #algorithm_order = _validate_same_algorithms(performance_dicts)
    algorithm_order = _validate_same_algorithms(performance_dicts)

    board_titles = [
        "Board #1",
        "Board #2",
        "Board #3",
        "Board #4",
    ]

    # -------- Figure 1: Length --------
    fig_len, axes_len = plt.subplots(2, 2, figsize=(16, 10))
    axes_len = axes_len.flatten()

    for ax, performances, title in zip(axes_len, performance_dicts, board_titles):
        _plot_metric_subplot(
            ax=ax,
            performances=performances,
            metric="length",
            title=f"Solution Length - {title}",
            algorithm_order=algorithm_order,
            log_scale=False
        )

    fig_len.suptitle("Solution Length Comparison Across Starting Boards", fontsize=16)
    fig_len.tight_layout(rect=[0, 0, 1, 0.96])

    # -------- Figure 2: Expanded Nodes --------
    fig_exp, axes_exp = plt.subplots(2, 2, figsize=(16, 10))
    axes_exp = axes_exp.flatten()

    for ax, performances, title in zip(axes_exp, performance_dicts, board_titles):
        _plot_metric_subplot(
            ax=ax,
            performances=performances,
            metric="expanded_nodes",
            title=f"Expanded Nodes - {title}",
            algorithm_order=algorithm_order,
            log_scale=True,
        )

    fig_exp.suptitle("Expanded Nodes Comparison Across Starting Boards", fontsize=16)
    fig_exp.tight_layout(rect=[0, 0, 1, 0.96])

    plt.show()