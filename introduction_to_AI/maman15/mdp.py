# from set_parrent_as_cwd import change_to_parent_directory
# change_to_parent_directory()

#from __future__ import annotations

# from pprint import pprint
# from policy_translation import policy_translation
# from value_iteration import value_iteration
# from plot_value_iteration import plot_value_iteration
# from plot_policy_matrix import plot_policy_matrix
from utils import *
import numpy as np
import random


class MDP:
    def __init__(self, datafile: str, gamma, p):
        # super().__init__()

        data = np.load(datafile)

        self.states = data['states']
        self.rewards = data['rewards']
        self.terminal_state = -1
        self.shape = self.states.shape
        self.directions = SORTED_ACTIONS

        self.gamma = gamma
        self.p = p

    def get_pos_type(self, pos):
        if not self.is_legal_pos(pos):
            return 'illegal'

        if self.is_terminal_pos(pos):
            return 'terminal'

        if self.is_blocked_pos(pos):
            return 'block'

        return 'state'

    @staticmethod
    def get_dig_actions(direction):
        dig_actions = {'dig_left': None, 'dig_right': None}
        label = directions_to_labels[str(direction)]

        if label == 'UP' or label == 'DOWN':
            dig_actions['dig_left'] = LEFT
            dig_actions['dig_right'] = RIGHT

        if label == 'LEFT':
            dig_actions['dig_left'] = DOWN
            dig_actions['dig_right'] = UP

        if label == 'RIGHT':
            dig_actions['dig_left'] = UP
            dig_actions['dig_right'] = DOWN

        return dig_actions

    def is_blocked_pos(self, pos):
        pos_x, pos_y = pos
        return self.states[pos_x, pos_y] == 0

    def is_terminal_pos(self, pos):
        pos_x, pos_y = pos
        return self.states[pos_x, pos_y] == self.terminal_state

    def is_legal_pos(self, pos):
        pos_x, pos_y = pos
        return (0 <= pos_x < self.shape[0]) and (0 <= pos_y < self.shape[1])

    def is_valid_pos(self, pos):
        """state position is inside board and not blocked"""
        return self.is_legal_pos(pos) and not self.is_blocked_pos(pos)

    def is_updatable_pos(self, pos):
        """state position is valid and not terminal"""
        return self.is_valid_pos(pos) and not self.is_terminal_pos(pos)

    def get_transition_model(self, pos, desire_actions):

        transition_model = {}

        for desire_action in desire_actions:
            dig_actions = self.get_dig_actions(desire_action)
            key = directions_to_labels[str(desire_action)]

            desire_pos = (vector(*pos) + desire_action).tolist()
            dig_left_pos = (vector(*pos) + dig_actions['dig_left']).tolist()
            dig_right_pos = (vector(*pos) + dig_actions['dig_right']).tolist()

            is_dig_left_valid = self.is_valid_pos(dig_left_pos)
            is_dig_right_valid = self.is_valid_pos(dig_right_pos)

            failed_prob = (1 - self.p) / 2

            # transition model baseline
            transition_model[key] = {'desire_pos': desire_pos,
                                     'desire_prob': self.p,
                                     'dig_left_pos': dig_left_pos,
                                     'dig_left_prob': failed_prob,
                                     'dig_right_pos': dig_right_pos,
                                     'dig_right_prob': failed_prob}

            if is_dig_left_valid and is_dig_right_valid:
                continue

            if is_dig_left_valid and not is_dig_right_valid:
                transition_model[key]['desire_prob'] = self.p + failed_prob
                transition_model[key]['dig_right_prob'] = 0
                continue

            if not is_dig_left_valid and is_dig_right_valid:
                transition_model[key]['desire_prob'] = self.p + failed_prob
                transition_model[key]['dig_left_prob'] = 0
                continue

            if not is_dig_left_valid and not is_dig_right_valid:
                transition_model[key]['desire_prob'] = 1
                transition_model[key]['dig_left_prob'] = 0
                transition_model[key]['dig_right_prob'] = 0

        return transition_model

    def get_actions(self, pos):
        assert self.is_legal_pos(pos), f"illegal current position: {pos}, mdp shape: {self.shape}"
        assert not self.is_blocked_pos(pos), f"current position cannot be a blocked position: {pos}"

        valid_actions = []

        for direction in self.directions:
            action_pos = vector(*pos) + direction

            if self.is_valid_pos(action_pos):
                valid_actions.append(direction)

        return valid_actions

    def get_reward(self, pos):
        pos_x, pos_y = pos
        return self.rewards[pos_x, pos_y]

    def update(self, pos, action):
        empty_result = []
        valid_actions = self.get_actions(pos)
        transition_model = self.get_transition_model(pos, valid_actions)

        action_label = directions_to_labels[action]

        if action_label not in transition_model.keys():
            return empty_result

        else:
            action_transition_model = transition_model[action_label]

            desire_pos = action_transition_model['desire_pos']
            desire_prob = action_transition_model['desire_prob']

            dig_left_pos = action_transition_model['dig_left_pos']
            dig_left_prob = action_transition_model['dig_left_prob']

            dig_right_pos = action_transition_model['dig_right_pos']
            dig_right_prob = action_transition_model['dig_right_prob']

            states = [desire_pos, dig_left_pos, dig_right_pos]
            weights = [desire_prob, dig_left_prob, dig_right_prob]

            chosen_pos = random.choices(states, weights=weights, k=1)[0]

            return chosen_pos, self.get_reward(chosen_pos)


if __name__ == '__main__':
    from run_question_2 import run_question_2
    from run_question_3 import run_question_3
    from parse_args import parse_args

    args = parse_args()

    datafile = args.filename
    algorithm = args.algorithm

    student_name = "Omer_Shraibshtein"
    #datafile = 'input_2026b.npz'
    figures_folder = 'figures'
    numpy_results_folder = 'npz_results'

    if algorithm == "ValueIteration":
        run_question_2(student_name=student_name,
                       datafile=datafile,
                       figures_folder=figures_folder,
                       numpy_results_folder=numpy_results_folder)


    elif args.algorithm == "PolicyIteration":

        run_question_3(student_name=student_name,
                       datafile=datafile,
                       figures_folder=figures_folder,
                       numpy_results_folder=numpy_results_folder)