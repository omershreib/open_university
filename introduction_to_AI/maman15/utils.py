"""
Author: Omer Shraibshtein (205984271)
Date:   10/06/2026
Email:  omershreib@gmail.com
"""

import numpy as np


def vector(x: int, y: int) -> np.array:
    return np.array([x, y])


# action (row, col)
UP = vector(-1, 0)
DOWN = vector(+1, 0)
LEFT = vector(0, -1)
RIGHT = vector(0, +1)

SORTED_ACTIONS = [UP, DOWN, RIGHT, LEFT]

directions_to_labels: dict = {str(UP): 'UP', str(DOWN): 'DOWN', str(LEFT): 'LEFT', str(RIGHT): 'RIGHT'}
labels_to_directions: dict = {'UP': UP, 'DOWN': DOWN, 'LEFT': LEFT, 'RIGHT': RIGHT}

state_to_key = lambda x, y: f"{x},{y}"


def state_key_to_pos(key: str):
    str_x_pos, str_y_pos = key.split(',')
    x_pos = int(str_x_pos)
    y_pos = int(str_y_pos)

    return x_pos, y_pos


def string_float(flt):
    return str(flt).replace('.', '')


def same_action(a1, a2):
    return np.array_equal(a1, a2)


def stop_condition(gamma, epsilon):
    if gamma == 0:
        return float("inf")

    if gamma == 1:
        return epsilon

    return epsilon * (1 - gamma) / gamma


def q_value(mdp, pos, action, utilities):
    total_sum = 0
    valid_actions = mdp.get_actions(pos)
    transition_model = mdp.get_transition_model(pos, valid_actions)

    action_label = directions_to_labels[str(action)]

    # print(action_label in transition_model.keys())
    if action_label in transition_model.keys():
        action_transition_model = transition_model[action_label]

        desire_pos = action_transition_model['desire_pos']
        desire_prob = action_transition_model['desire_prob']

        dig_left_pos = action_transition_model['dig_left_pos']
        dig_left_prob = action_transition_model['dig_left_prob']

        dig_right_pos = action_transition_model['dig_right_pos']
        dig_right_prob = action_transition_model['dig_right_prob']

        states = [desire_pos, dig_left_pos, dig_right_pos]
        probabilities = [desire_prob, dig_left_prob, dig_right_prob]

        for state, prob in zip(states, probabilities):
            key = state_to_key(*state)
            # print("state: ", state)
            if mdp.is_valid_pos(state):
                # print("add to total sum")
                total_sum += prob * (mdp.get_reward(state) + mdp.gamma * utilities[key])
                # print(f"total sum = {total_sum}")

        return total_sum


def init_utilities(mdp, u):
    for x in range(mdp.shape[0]):
        for y in range(mdp.shape[1]):
            u[state_to_key(x, y)] = 0

    return u
