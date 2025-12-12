import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle


class ReversiPlayer:
    def __init__(self, name):
        self.name = name
        self.total_score = 0


class ReversiManager:
    def __init__(self):
        self.state_space = None
        self.initial_state = None
        self.players = ['Red', 'White']
        self.actions = None
        self.transition_model = None
        self.terminal_state = None
        self.utility = None
        self.current_move = 0

    def calc_players_utility(self):
        pass


class ReversiGameBoard:
    def __init__(self, qubic_size):
        self.fig = None
        self.ax = None
        self.player_1_color = 'black'
        self.player_2_color = 'white'
        self.n = qubic_size
        self.is_empty_board = False

        self.build_empty_game_board()

    def _check_valid_n(self):
        if self.n % 2 != 0:
            print('invalid qubic size. must be even (8,10,12,...)')

    def add_disc_figure(self, point, color):
        print(f"add {color} disc player on point {point}")
        x, y = point
        self.ax.add_patch(Circle((y + 0.5, x + 0.5), 0.38, facecolor=color, edgecolor="black", linewidth=1.5))

    def build_empty_game_board(self):
        # create empty n x n reversi grid game board
        n = self.n
        fig, ax = plt.subplots(figsize=(6, 6))
        board_color = "#2e8b57"
        grid_color = "black"

        for row in range(n):
            for column in range(n):
                ax.add_patch(Rectangle((column, row), 1, 1, facecolor=board_color, edgecolor=grid_color, linewidth=1))

        self.ax = ax
        self.fig = fig
        self.is_empty_board = True

    def init_game_state(self):
        if not self.is_empty_board:
            self.build_empty_game_board()

        top_left_center = int(self.n / 2) - 1
        player_1_init_top_point = (top_left_center, top_left_center)
        player_1_init_bottom_point = (top_left_center + 1, top_left_center + 1)
        player_2_init_top_point = (top_left_center + 1, top_left_center)
        player_2_init_bottom_point = (top_left_center, top_left_center + 1)

        self.add_disc_figure(player_1_init_top_point, self.player_1_color)
        self.add_disc_figure(player_1_init_bottom_point, self.player_1_color)
        self.add_disc_figure(player_2_init_top_point, self.player_2_color)
        self.add_disc_figure(player_2_init_bottom_point, self.player_2_color)

    def show_current_game_board(self):
        n = self.n

        self.ax.set_aspect("equal")
        self.ax.set_xlim(0, n)
        self.ax.set_ylim(0, n)
        self.ax.set_xticks(range(n + 1))
        self.ax.set_yticks(range(n + 1))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.tick_params(length=0)
        self.ax.set_title("Reversi (Othello) — Initial State", pad=12)

        plt.show()


if __name__ == '__main__':
    board = ReversiGameBoard(8)
    board.init_game_state()
    board.show_current_game_board()
