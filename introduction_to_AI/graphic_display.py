import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from typing import Optional, Tuple

from models import ColorDiscPlayer


class ReversiGraphicDisplay:
    def __init__(self, board_size: int = 8, interactive: bool = True, delay: float = 0.01,
                 title: str = "Reversi (Red vs White)"):
        self.board_size = board_size
        self.interactive = interactive
        self.delay = delay
        self.title = title

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

        # Reserve top area for figure title + terminal banner + overlays
        fig.subplots_adjust(top=0.82)
        fig.suptitle(self.title, fontsize=14, y=0.98)

        self._terminal_text = fig.text(
            0.5, 0.90, "",
            ha="center", va="center",
            fontsize=12, color="black"
        )

        # Draw grid
        for r in range(self.board_size):
            for c in range(self.board_size):
                ax.add_patch(Rectangle(
                    (c, r), 1, 1,
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

        self._score_text = ax.text(0.02, 1.02, "", transform=ax.transAxes,
                                   fontsize=12, va="bottom", ha="left", color="black")
        self._status_text = ax.text(0.98, 1.02, "", transform=ax.transAxes,
                                    fontsize=12, va="bottom", ha="right", color="black")

        self.fig, self.ax = fig, ax
        self._refresh()

    def set_speed(self, delay: float) -> None:
        self.delay = delay

    def _refresh(self) -> None:
        if self.fig is None:
            return
        self.fig.canvas.draw_idle()
        self.fig.canvas.flush_events()
        if self.interactive:
            plt.pause(self.delay)

    def display(self) -> None:
        plt.show()

    # ------- drawing helpers -------

    def _bit_to_rc(self, b: int) -> Tuple[int, int]:
        i = b.bit_length() - 1
        return divmod(i, self.board_size)

    def _color_to_face(self, player: ColorDiscPlayer) -> str:
        return "red" if player == ColorDiscPlayer.RED else "white"

    def clear_discs(self) -> None:
        for a in self._disc_artists:
            a.remove()
        self._disc_artists.clear()

    def add_disc(self, player: ColorDiscPlayer, r: int, c: int) -> None:
        disc = Circle(
            (c + 0.5, r + 0.5),
            0.38,
            facecolor=self._color_to_face(player),
            edgecolor="black",
            linewidth=1.5
        )
        self.ax.add_patch(disc)
        self._disc_artists.append(disc)

    def render_state(self, state) -> None:
        self.clear_discs()

        red_bits = state.red_bitboard.bitboard
        white_bits = state.white_bitboard.bitboard

        # iterate set bits (fast bit iteration)
        bb = red_bits
        while bb:
            lsb = bb & -bb
            r, c = self._bit_to_rc(lsb)
            self.add_disc(ColorDiscPlayer.RED, r, c)
            bb ^= lsb

        bb = white_bits
        while bb:
            lsb = bb & -bb
            r, c = self._bit_to_rc(lsb)
            self.add_disc(ColorDiscPlayer.WHITE, r, c)
            bb ^= lsb

    # ------- overlays -------

    def update_score(self, state) -> None:
        red = state.score(ColorDiscPlayer.RED)
        white = state.score(ColorDiscPlayer.WHITE)
        self._score_text.set_text(f"Score  RED: {red}   WHITE: {white}")

    def update_status(self, state, last_move: Optional[int]) -> None:
        turn = state.player_turn.name
        if last_move is None:
            self._status_text.set_text(f"Turn: {turn} | Last: PASS")
        else:
            r, c = self._bit_to_rc(last_move)
            self._status_text.set_text(f"Turn: {turn} | Last: ({r},{c})")

    def show_terminal(self, state, utility_red: int, utility_white: int) -> None:
        red = state.score(ColorDiscPlayer.RED)
        white = state.score(ColorDiscPlayer.WHITE)
        if red > white:
            winner = "RED"
        elif white > red:
            winner = "WHITE"
        else:
            winner = "DRAW"

        self._terminal_text.set_text(
            f"GAME OVER — Winner: {winner} | U(RED)={utility_red}  U(WHITE)={utility_white}"
        )
        self._status_text.set_text("")  # optional

    # ------- public update -------

    def update(self, state, last_move: Optional[int] = None, terminal: bool = False,
               utility_red: Optional[int] = None, utility_white: Optional[int] = None) -> None:
        self.render_state(state)
        self.update_score(state)

        if terminal:
            if utility_red is None or utility_white is None:
                raise ValueError("terminal=True requires utility_red and utility_white")
            self.show_terminal(state, utility_red, utility_white)
        else:
            # clear any previous terminal banner
            if self._terminal_text is not None:
                self._terminal_text.set_text("")
            self.update_status(state, last_move)

        self._refresh()
