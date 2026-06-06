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

    #print(action_label in transition_model.keys())
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
            #print("state: ", state)
            if mdp.is_valid_pos(state):
                #print("add to total sum")
                total_sum += prob * (mdp.get_reward(state) + mdp.gamma * utilities[key])
                #print(f"total sum = {total_sum}")

        return total_sum


def value_iteration(mdp: MDP, epsilon=1000):
    U = init_utilities(mdp, {})
    U_prime = init_utilities(mdp, {})
    policy_dict = {}

    stop_condition = epsilon * (1 - mdp.gamma) / mdp.gamma
    index = 0

    while True:
        index += 1
        print(f"value iteration #{index}")

        U = U_prime.copy()
        delta = 0

        for state_key in list(U.keys()):
            pos = state_key_to_pos(state_key)

            if not mdp.is_valid_pos(pos):
                continue

            best_action = None
            best_value = float("-inf")

            for action in mdp.get_actions(pos):
                curr_value = q_value(mdp, pos, action, U)

                if curr_value > best_value:
                    best_value = curr_value
                    best_action = action

            U_prime[state_key] = best_value
            policy_dict[state_key] = best_action

            delta = max(delta, abs(U_prime[state_key] - U[state_key]))

        print(f"delta: {delta} ; stop-condition (<=) {stop_condition}")

        if delta <= stop_condition:
            break

    return U_prime, policy_dict
