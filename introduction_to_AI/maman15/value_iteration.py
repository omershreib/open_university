from .mdp import MDP, directions_to_labels

state_to_key = lambda x, y: f"{x},{y}"


def state_key_to_pos(key: str):
    str_x_pos, str_y_pos = key.split(',')
    x_pos = int(str_x_pos)
    y_pos = int(str_y_pos)

    return x_pos, y_pos


def init_utilities(mdp, u):
    for x in range(mdp.shape[0]):
        for y in range(mdp.shape[1]):
            u[state_to_key(x, y)] = 0

    return u


def q_value(mdp, pos, action, utilities):
    total_sum = 0
    valid_actions = mdp.get_actions(pos)
    transition_model = mdp.get_transition_model(pos, valid_actions)

    action_label = directions_to_labels[str(action)]

    print(action_label in transition_model.keys())
    if action_label in transition_model.keys():
        action_transition_model = transition_model[action_label]

        desire_pos = action_transition_model['desire_pos']
        desire_prob = action_transition_model['desire_prob']

        dig_left_pos = action_transition_model['dig_left_pos']
        dig_left_prob = action_transition_model['dig_left_prob']

        dig_right_pos = action_transition_model['dig_left_pos']
        dig_right_prob = action_transition_model['dig_right_prob']

        states = [desire_pos, dig_left_pos, dig_right_pos]
        probabilities = [desire_prob, dig_left_prob, dig_right_prob]

        for state, prob in zip(states, probabilities):
            key = state_to_key(*state)
            print("state: ", state)
            if mdp.is_valid_pos(state):
                print("add to total sum")
                total_sum += prob * (mdp.get_reward(state) + mdp.gamma * utilities[key])
                print(f"total sum = {total_sum}")

        return total_sum


def value_iteration(mdp: MDP, epsilon=0.01):
    pre_qcalc_utilities = {}
    post_qcalc_utilities = {}
    policy_dict = {}

    delta = 0

    pre_qcalc_utilities = init_utilities(mdp, pre_qcalc_utilities)
    post_qcalc_utilities = init_utilities(mdp, post_qcalc_utilities)

    state_keys = pre_qcalc_utilities.keys()

    for state_key in state_keys:

        best_qvalue_action = None
        best_qvalue = 0
        pos = state_key_to_pos(state_key)

        if not mdp.is_valid_pos(pos):
            continue

        valid_actions = mdp.get_actions(pos)

        for action in valid_actions:
            print("action: ", action)
            curr_qvalue = q_value(mdp, pos, action, pre_qcalc_utilities)

            print(f"qvalues (best vs current): {best_qvalue} {curr_qvalue}")
            if best_qvalue < curr_qvalue:
                best_qvalue = curr_qvalue
                best_qvalue_action = action

        print(best_qvalue, best_qvalue_action)
        post_qcalc_utilities[state_key] = best_qvalue
        policy_dict[state_key] = best_qvalue_action

        # post_qcalc_utilities[state_key] = max([
        #                                        for action in valid_actions])

        abs_utilities = abs(pre_qcalc_utilities[state_key] - post_qcalc_utilities[state_key])
        delta = max(delta, abs_utilities)

    if delta <= (epsilon * (1 - mdp.gamma)) / mdp.gamma:
        return post_qcalc_utilities, policy_dict
