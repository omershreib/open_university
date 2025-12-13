import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from models import Color


class ReversiGraphicDisplay:

    def __init__(self, board_size):
        self.fig = None
        self.ax = None
        self.board_size = board_size

    def initial_graphic_display(self):
        # create empty n x n reversi grid game board
        qubic_range = range(self.board_size)
        fig, ax = plt.subplots(figsize=(6, 6))
        board_color = "#2e8b57"
        grid_color = "black"

        for row in qubic_range:
            for column in qubic_range:
                ax.add_patch(Rectangle((column, row), 1, 1, facecolor=board_color, edgecolor=grid_color, linewidth=1))

        self.ax = ax
        self.fig = fig

    def add_disc(self, player: Color, point: tuple[int, int]) -> None:
        print(f"add {player} disc player on point {point}")
        x, y = point
        self.ax.add_patch(Circle((y + 0.5, x + 0.5), 0.38, facecolor=player, edgecolor="black", linewidth=1.5))

    def display(self):
        n = self.board_size

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
