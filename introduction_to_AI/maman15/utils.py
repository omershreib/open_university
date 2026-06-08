import numpy as np

def vector(x: int, y: int) -> np.array:
    return np.array([x, y])


# action (row, col)
UP = vector(-1, 0)
DOWN = vector(+1, 0)
LEFT = vector(0, -1)
RIGHT = vector(0, +1)

MDP_DIRECTIONS = [LEFT, RIGHT, UP, DOWN]

directions_to_labels: dict = {str(UP): 'UP', str(DOWN): 'DOWN', str(LEFT): 'LEFT', str(RIGHT): 'RIGHT'}
labels_to_directions: dict = {'UP': UP, 'DOWN': DOWN, 'LEFT': LEFT, 'RIGHT': RIGHT}


state_to_key = lambda x, y: f"{x},{y}"

def state_key_to_pos(key: str):
    str_x_pos, str_y_pos = key.split(',')
    x_pos = int(str_x_pos)
    y_pos = int(str_y_pos)

    return x_pos, y_pos