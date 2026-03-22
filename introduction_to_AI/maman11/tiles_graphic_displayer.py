import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class TilesGameGraphicDisplayer:
    """
    A simple matplotlib-based visualizer for a 3x3 tiles game board.

    Expected board format:
        - numpy 2D array
        - shape == (3, 3)

    Example:
        board = np.array([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0],   # 0 can represent the empty tile
        ])

        viewer = TilesGameGraphicDisplayer()
        viewer.refresh(board)
    """

    def __init__(self, delay=0.2, empty_value=0, title="Tiles Game"):
        self.empty_value = empty_value
        self.title = title
        self.delay = delay
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.ax.set_aspect("equal")
        plt.ion()  # interactive mode on

    def refresh(self, board: np.ndarray) -> None:
        """
        Refresh the display with a new 3x3 board.

        Args:
            board: numpy array of shape (3, 3)
        """
        self._validate_board(board)

        self.ax.clear()
        self.ax.set_xlim(0, 3)
        self.ax.set_ylim(0, 3)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_title(self.title)

        for row in range(3):
            for col in range(3):
                value = board[row, col]

                # Convert array coordinates to plot coordinates
                # so row 0 appears at the top
                x = col
                y = 2 - row

                is_empty = value == self.empty_value

                rect = Rectangle(
                    (x, y),
                    1,
                    1,
                    fill=not is_empty,
                    linewidth=2,
                    edgecolor="black",
                    facecolor="lightgray" if not is_empty else "white",
                )
                self.ax.add_patch(rect)

                if not is_empty:
                    self.ax.text(
                        x + 0.5,
                        y + 0.5,
                        str(value),
                        ha="center",
                        va="center",
                        fontsize=20,
                        fontweight="bold",
                    )

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(self.delay)

    def show(self) -> None:
        """Show the window in blocking mode."""
        plt.ioff()
        plt.show()

    @staticmethod
    def _validate_board(board: np.ndarray) -> None:
        if not isinstance(board, np.ndarray):
            raise TypeError("board must be a numpy.ndarray")
        if board.shape != (3, 3):
            raise ValueError(f"board must have shape (3, 3), got {board.shape}")