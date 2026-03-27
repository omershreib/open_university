from __future__ import annotations

from introduction_to_AI.models import Problem


def reconstruct_actions_path(problem: Problem, path: list):
    """
    Convert a path of states into a list of action objects.

    Args:
        problem: a valid Problem object
        path: list of game states from initial state to a goal state

    Returns:
        an action lists that been induced by this path
    """
    if not path or len(path) < 2:
        return []

    actions = []

    for i in range(len(path) - 1):
        curr_state = path[i]
        next_state = path[i + 1]

        movement = problem.args_action(curr_state, next_state)
        actions.append(movement)

    return actions
