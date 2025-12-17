import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from typing import Optional, Tuple
from models import ColorDiscPlayer


class ReversiGraphicDisplay:
    def __init__(self, board_size: int = 8, title: str = "Reversi (Red vs White)",
                 interactive: bool = True, delay: float = 0.01):
        self.board_size = board_size
        self.title = title
        self.interactive = interactive
        self.delay = delay

        self.fig = None
        self.ax = None

        self._disc_artists = []
        self._score_text = None          
        self._status_text = None         
        self._terminal_text = None       

        self.board_color = "#2e8b57"
        self.grid_color = "black"

        if self.interactive:
            plt.ion()

    def initial_graphic_display(self) -> None:
        fig, ax = plt.subplots(figsize=(6, 6))

        # Reserve space at the top for title + terminal message + overlays
        fig.subplots_adjust(top=0.82)

        # Figure-level title (won't collide with axes text)
        fig.suptitle(self.title, fontsize=14, y=0.98)

        # Figure-level terminal banner (only used at game over)
        self._terminal_text = fig.text(
            0.5, 0.90, "",
            ha="center", va="center",
            fontsize=12, color="black"
        )

        # Draw the board grid
        for row in range(self.board_size):
            for column in range(self.board_size):
                ax.add_patch(Rectangle(
                    (row, column), 1, 1,
                    facecolor=self.board_color,
                    edgecolor=self.grid_color,
                    linewidth=1
                ))

        ax.set_aspect("equal")
        ax.set_xlim(0, self.board_size)
        ax.set_ylim(0, self.board_size)
        ax.set_xticks(range(self.board_size + 1))
        ax.set_yticks(range(self.board_size + 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.tick_params(length=0)

        # Axes-level overlays (safe now because top space is reserved)
        self._score_text = ax.text(
            0.02, 1.02, "",
            transform=ax.transAxes,
            fontsize=12, va="bottom", ha="left", color="black"
        )
        self._status_text = ax.text(
            0.98, 1.02, "",
            transform=ax.transAxes,
            fontsize=12, va="bottom", ha="right", color="black"
        )

        self.fig, self.ax = fig, ax
        self._refresh()

    def _color_to_face(self, player: ColorDiscPlayer) -> str:
        if player == ColorDiscPlayer.RED:
            return "red"
        if player == ColorDiscPlayer.WHITE:
            return "white"
        raise ValueError(f"unknown player color: {player}")

    def clear_discs(self) -> None:
        for a in self._disc_artists:
            a.remove()
        self._disc_artists.clear()

    def add_disc(self, player: ColorDiscPlayer, disc_cell: Tuple[int, int]) -> None:
        row, column = disc_cell
        disc = Circle(
            (column + 0.5, row + 0.5),
            0.38,
            facecolor=self._color_to_face(player),
            edgecolor="black",
            linewidth=1.5
        )
        self.ax.add_patch(disc)
        self._disc_artists.append(disc)

    def render_board(self, board) -> None:
        self.clear_discs()
        for row in range(self.board_size):
            for column in range(self.board_size):
                cell = (row, column)
                player = board.get_player_cell(row, column)

                if player is None:
                    continue

                self.add_disc(player, cell)

    def update_score(self, board) -> None:
        red = board.calc_score(ColorDiscPlayer.RED)
        white = board.calc_score(ColorDiscPlayer.WHITE)
        self._score_text.set_text(f"Score  RED: {red}   WHITE: {white}")

    def update_status(self, player: ColorDiscPlayer, player_move: Optional[object] = None) -> None:
        if player_move is None:
            self._status_text.set_text(f"Turn: {player.name}")
            return

        is_pass = getattr(player_move, "is_pass", False)
        row = getattr(player_move, "row", None)
        column = getattr(player_move, "column", None)
        cell = (row, column)

        if is_pass or row is None or column  is None:
            self._status_text.set_text(f"Turn: {player.name} | Movement: PASS")
        else:
            self._status_text.set_text(f"Turn: {player.name} | Movement: {cell}")

    def show_terminal(self, board, utility_red: int, utility_white: int) -> None:
        red = board.calc_score(ColorDiscPlayer.RED)
        white = board.calc_score(ColorDiscPlayer.WHITE)

        if red > white:
            winner = "RED"
        elif white > red:
            winner = "WHITE"
        else:
            winner = "DRAW"

        # Put game-over info in the figure-level banner (below the title)
        if self._terminal_text is not None:
            self._terminal_text.set_text(
                f"GAME OVER — Winner: {winner} | RED Utility: {utility_red}  WHITE Utility: {utility_white}"
            )

        # Optional: clear the normal in-game status text to reduce clutter
        self._status_text.set_text("")

    def update(self, state, player_move: Optional[object] = None, terminal: bool = False,
               red_utility: Optional[int] = None, white_utility: Optional[int] = None) -> None:
        self.render_board(state.board)
        self.update_score(state.board)

        if terminal:
            if red_utility is None or white_utility is None:
                raise ValueError("terminal=True requires utility_red and utility_white")
            self.show_terminal(state.board, red_utility, white_utility)
            plt.pause(1)

        else:
            # Clear any previous terminal banner during normal play
            if self._terminal_text is not None:
                self._terminal_text.set_text("")
            self.update_status(state.player_turn, player_move)

        self._refresh()

    def set_speed(self, delay: float) -> None:
        """Seconds per ply when interactive=True."""
        self.delay = delay

    def _refresh(self) -> None:
        if self.fig is None:
            return
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
        if self.interactive:
            plt.pause(self.delay)

    @staticmethod
    def display() -> None:
        plt.show()
