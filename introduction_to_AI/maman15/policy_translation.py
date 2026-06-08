from collections import deque
from .utils import *

UP_SYMBOL = '^'
DOWN_SYMBOL = 'v'
RIGHT_SYMBOL = '>'
LEFT_SYMBOL = '<'
INDIFFERENCE_SYMBOL = '+'
TERMINAL_SYMBOL = 'O'
BLOCK_SYMBOL = 'X'


def get_action_symbol(action):
    label = directions_to_labels[str(action)]

    if label == 'UP':
        return UP_SYMBOL

    if label == 'DOWN':
        return DOWN_SYMBOL

    if label == 'LEFT':
        return LEFT_SYMBOL

    if label == 'RIGHT':
        return RIGHT_SYMBOL

    raise Exception(f"invalid action: {action}")


def get_pos_symbol(mdp, pos):
    pos_type = mdp.get_pos_type(pos)

    if pos_type == 'terminal':
        return TERMINAL_SYMBOL

    if pos_type == 'block':
        return BLOCK_SYMBOL

    return None


def policy_translation(mdp, pos, actions):
    symbols = deque()
    curr_pos_symbol = get_pos_symbol(mdp, pos)

    if curr_pos_symbol is not None:
        return curr_pos_symbol

    if actions is None:
        return

    for action in actions:
        action_symbol = get_action_symbol(action)

        if action_symbol in [UP_SYMBOL, RIGHT_SYMBOL]:
            symbols.append(action_symbol)

        if action_symbol in [DOWN_SYMBOL, LEFT_SYMBOL]:
            symbols.appendleft(action_symbol)

    return f"{INDIFFERENCE_SYMBOL}".join(symbols)
