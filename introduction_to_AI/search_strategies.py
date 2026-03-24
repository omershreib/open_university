from introduction_to_AI.models import *
import itertools


def old_best_first_search(problem, f):
    """Best-First-Search Strategy
    implemented as depicted in the course book
    "Artificial Intelligent a Modern Approach 4th Edition (page 91)"

    :param problem:
    :param f:
    :return:
    """

    expand_counter = 0
    node: Node = make_node(state=problem.initial_state, path_cost=0)
    frontier = build_priority_queue([node], f)
    reached = {problem.initial_state.get_key(): node}

    while not is_empty(frontier):
        node = pop(frontier)

        if problem.is_goal_state(node.state):
            return node, expand_counter

        expand_counter += 1
        for child in expand(problem, node):
            child_state = child.state

            if child_state.get_key() not in reached or child.path_cost < reached[child_state.get_key()].path_cost:
                reached[child_state.get_key()] = child
                add(child, frontier)

    return False, expand_counter


def best_first_search(problem, f):
    counter = itertools.count()
    start = make_node(state=problem.initial_state, path_cost=0)
    frontier = [(f(start), next(counter), start)]
    reached = {start.state.get_key(): start}
    expand_counter = 0

    while frontier:
        _, _, node = pop(frontier)
        key = node.state.get_key()

        if reached[key] is not node:
            continue

        if problem.is_goal_state(node.state):
            return node, expand_counter

        expand_counter += 1

        for child in expand(problem, node):
            child_key = child.state.get_key()
            if child_key not in reached or child.path_cost < reached[child_key].path_cost:
                reached[child_key] = child
                add(frontier, (f(child), next(counter), child))

    return False, expand_counter


def astar_search(problem: Problem, evaluator: Evaluator):
    def f(node):
        g = node.path_cost
        h = evaluator.evaluate(node.state, problem.goal_state)
        return g + h

    return best_first_search(problem, f)
