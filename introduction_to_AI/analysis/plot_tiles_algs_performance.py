import matplotlib.pyplot as plt


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


def _plot_metric_subplot(ax, performances: dict, metric: str, title: str,
                         algorithm_order, log_scale=False):
    values = [performances[alg][metric] for alg in algorithm_order]

    bars = ax.bar(algorithm_order, values)
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


def _find_bfs_key(performances: dict, preferred_key: str = "bfs") -> str:
    if preferred_key in performances:
        return preferred_key

    lowered = {k.lower(): k for k in performances.keys()}
    if preferred_key.lower() in lowered:
        return lowered[preferred_key.lower()]

    raise ValueError(
        f"Could not find '{preferred_key}' in performances keys: {list(performances.keys())}"
    )


def plot_results(
    performances_1: dict,
    performances_2: dict,
    performances_3: dict,
    performances_4: dict,
    optimal_alg: str = "bfs",
):
    """
    Plot 3 figures:

    1. Solution length comparison across algorithms for each board
    2. Expanded nodes comparison across algorithms for each board
    3. Optimal solution length per board, taken from BFS

    Parameters
    ----------
    performances_1 ... performances_4 : dict
        Each dictionary represents one starting board:
        {
            'alg_name': {
                'length': path_length,
                'expanded_nodes': expanded_nodes
            },
            ...
        }

    optimal_alg : str
        Algorithm name used as the optimal baseline. Default: 'bfs'
    """

    performance_dicts = [
        performances_1,
        performances_2,
        performances_3,
        performances_4,
    ]

    for i, perf in enumerate(performance_dicts, start=1):
        _validate_performance_dict(perf, f"performances_{i}")

    algorithm_order = _validate_same_algorithms(performance_dicts)

    board_titles = [
        "Board 1 (Easiest)",
        "Board 2",
        "Board 3",
        "Board 4 (Hardest)",
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
            log_scale=False,
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

    # -------- Figure 3: Optimal Solution Length Per Board (from BFS) --------
    bfs_keys = [_find_bfs_key(perf, optimal_alg) for perf in performance_dicts]
    optimal_lengths = [
        perf[bfs_key]["length"]
        for perf, bfs_key in zip(performance_dicts, bfs_keys)
    ]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(board_titles, optimal_lengths)
    plt.title(f"Optimal Solution Length Per Board ({optimal_alg.upper()} baseline)")
    plt.xlabel("Board Difficulty")
    plt.ylabel("Optimal Path Length")
    plt.xticks(rotation=15)

    for bar, value in zip(bars, optimal_lengths):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value,
            str(value),
            ha="center",
            va="bottom",
            fontsize=10,
        )

    plt.tight_layout()
    plt.show()