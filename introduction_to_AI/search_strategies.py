from introduction_to_AI.models import *
from introduction_to_AI.common import make_node, pop, push, expand
import itertools


def best_first_search(problem, f, h=None):
    """Best First Search Strategy

    basically, implemented EXACTLY as described in the course book (page 91)
    the main differance is that I build every nodes-item enter the frontier
    with a key-breaker tie-break in the case of f(node_1) == f(node_2)

    Arg:
        :param problem: a Problem object (discussed in details in the course book - chapter 3, read pages 81 - 87)
        :param f: an evaluation function (during A* run: f(node) = g(node) + h(node))
        :param h: (optional) a heuristic function. use only during debug

    Returns:
         if found a path from start-node towards a goal-node
         then returns a pair of (goal-node, num-of-expands)

         otherwise, returns (false, num-of-expands)
    """
    counter = itertools.count()
    start = make_node(state=problem.initial_state, path_cost=0)

    # make a priority suit for every node enter the frontier
    # in the form of: <f(node), numeric-tie-breaker, node>
    frontier = [(f(start), next(counter), start)]
    reached = {start.state.get_key(): start}
    expand_counter = 0

    # return true if the frontier is not empty
    while frontier:
        _, _, node = pop(frontier)

        if problem.is_goal_state(node.state):
            return node, expand_counter

        # key = node.state.get_key()
        #
        # if reached[key] is not node:
        #     continue

        # consistency check of heuristic during debug (make sure that h is not None)
        # print(f"path-cost: {node.path_cost}, h(n): {h(node.state, problem.goal_state)}, f(n): {f(node)}")
        # print(node.path_cost, h(node.state, problem.goal_state), f(node))

        # if problem.is_goal_state(node.state):
        #     return node, expand_counter

        expand_counter += 1

        for child in expand(problem, node):
            child_key = child.state.get_key()
            if child_key not in reached.keys() or child.path_cost < reached[child_key].path_cost:
                reached[child_key] = child
                push(frontier, (f(child), next(counter), child))

    return False, expand_counter


def astar_search(problem: Problem, evaluator: Evaluator):
    def f(node):
        g = node.path_cost
        h = evaluator.evaluate(node.state, problem.goal_state)
        return g + h

    return best_first_search(problem, f, evaluator.evaluate)
