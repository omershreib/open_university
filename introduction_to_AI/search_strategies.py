from introduction_to_AI.models import *


def best_first_search(problem, f):
    expand_counter = 0
    node: Node = make_node(state=problem.initial_state)
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


def astar_search(problem: Problem, evaluator: Evaluator):
    def f(node):
        g = node.path_cost
        h = evaluator.evaluate(node.state, problem.goal_state)
        return g + h

    return best_first_search(problem, f)
