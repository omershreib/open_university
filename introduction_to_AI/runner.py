from __future__ import annotations
from typing import Optional, Dict, List, Tuple

from bitboard import get_occupied_bitmask
from models import ColorDiscPlayer, Move  # your enums + Move class
from agents import ReversiAgent  # choose_move(state)->Move
from game_state import GameState  # your bitboard GameState
from bitboard_calculator import BitBoardCalculator
from graphic_display import ReversiGraphicDisplay


class ReversiGameRunner(BitBoardCalculator):
    """Reversi Game Runner

    the purpose of this runner class is to orchestrate the entire game
    """

    def __init__(
            self,
            board_size: int,
            red_agent: ReversiAgent,
            white_agent: ReversiAgent,
            verbose: bool = True,
            use_gui: bool = True,
            gui_delay: float = 0.05,
    ):
        """

        :param board_size: Reversi board size (for the classic 8 x 8 board, type board_size = 8)
        :param red_agent: Reversi agent class object for the maximum red player
        :param white_agent: Reversi agent class object for the minimum white player
        :param verbose: if true, print game progress to terminal
        :param use_gui: if true, enable graphic display of this game
        :param gui_delay: control delay progress of graphic display in seconds
        """
        super().__init__(board_size=board_size)

        self.verbose = verbose
        self.board_size = board_size
        self.current_turn: int = 0

        self.agents: Dict[ColorDiscPlayer, ReversiAgent] = {
            ColorDiscPlayer.RED: red_agent,
            ColorDiscPlayer.WHITE: white_agent,
        }

        self.state: GameState = GameState(
            red_bitboard=None,
            white_bitboard=None,
            player_turn=None,
            board_size=board_size,
            consecutive_passes=0,
        ).initial()

        # for debug, save players moves
        self.moves_history: List[Tuple[ColorDiscPlayer, Move]] = []
        self.scores_history: List[Tuple[int, int]] = []

        self.graphical_display = None
        if use_gui:
            self.graphical_display = ReversiGraphicDisplay(
                board_size=board_size,
                interactive=True,
                delay=gui_delay,
            )
            self.graphical_display.initial_graphic_display()
            self.graphical_display.update(self.state)

    def move2bit(self, move: Move) -> Optional[int]:
        if move.is_pass:
            return None
        return self.cell2bit((move.row, move.column))

    def bit2move(self, bit: Optional[int]) -> Move:
        if bit is None:
            return Move.pass_move()

        row, column = self.bit2cell(bit)
        return Move(row, column)

    def legal_moves_bits(self) -> List[Optional[int]]:
        return self.state.legal_moves()

    def legal_moves_as_moves(self) -> List[Move]:
        return [self.bit2move(bit) for bit in self.legal_moves_bits()]

    def current_agent(self) -> ReversiAgent:
        return self.agents[self.state.player_turn]

    def next_step(self) -> None:
        if self.state.is_terminal():
            return

        self.current_turn += 1
        player = self.state.player_turn
        agent = self.current_agent()

        move: Move = agent.choose_move(self.state)
        self.moves_history.append((player, move))
        self.scores_history.append(self.get_current_scores())

        # update game state
        self.state = self.state.update(move)

        # update GUI
        if self.graphical_display is not None:
            self.graphical_display.update(self.state, last_move=self.move2bit(move))

        if self.verbose:
            self.display()

    def play(self, max_turns: int = 10_000, stop_at: int = None) -> GameState:
        if self.verbose:
            print("start game\n")

            # just print the game board in state 0
            print(self.snapshot())

        while not self.state.is_terminal() and self.current_turn < max_turns:
            prev_snapshot = self.snapshot()
            self.next_step()

            if stop_at is None:
                continue

            if stop_at <= self.current_turn:
                print(f"\nprevious game snapshot - state {self.current_turn - 1}")
                print(f"\n{prev_snapshot}")
                self.print_previous_scores()
                print("\ncurrent game snapshot")
                self.display()

                print("\nforced to stop at the middle of this game (no winner)\n")
                return self.state

        if self.verbose:
            self.print_current_scores(is_final=True)

        utility_red = self.state.utility(ColorDiscPlayer.RED)
        utility_white = self.state.utility(ColorDiscPlayer.WHITE)

        if self.graphical_display is not None:
            self.graphical_display.update(
                self.state,
                terminal=True,
                utility_red=utility_red,
                utility_white=utility_white,
            )
            self.graphical_display.display()

        return self.state

    def display(self) -> None:
        player, move = self.moves_history[-1]
        if move.is_pass:
            print(f"\nstate {self.current_turn}, {player.name} PASS")
        else:
            print(f"\nstate {self.current_turn}, {player.name} moved, action={move}\n")

        print(self.snapshot())
        self.print_current_scores()

    def check_cell(self, cell: Tuple[int, int]) -> Optional[ColorDiscPlayer]:
        """

        check which player occupies cell (row, column).
        if cell is empty, return None
        """
        bit = self.cell2bit(cell)

        if self.state.red_bitboard.is_bit_on(bit):
            return ColorDiscPlayer.RED

        if self.state.white_bitboard.is_bit_on(bit):
            return ColorDiscPlayer.WHITE

        return None

    def snapshot(self):
        board_range = range(self.board_size)
        lines = ["  " + " ".join(str(i) for i in board_range)]
        for row in board_range:
            players_discs: list = []
            for column in board_range:
                player = self.check_cell((row, column))
                players_discs.append("." if player is None else str(player))
            lines.append(f"{row} " + " ".join(players_discs))

        return "\n".join(lines)


    def get_current_scores(self):
        red_score = self.state.score(ColorDiscPlayer.RED)
        white_score = self.state.score(ColorDiscPlayer.WHITE)
        return red_score, white_score

    def print_current_scores(self, is_final=False):
        red_score, white_score = self.get_current_scores()

        if is_final:
            print("\ngame over")
            print(f"final scores: RED={red_score}, WHITE={white_score}")
            if red_score > white_score:
                print("RED win")
            elif white_score > red_score:
                print("WHITE win")
            else:
                print("DRAW")

        if not is_final:
            print(f"\nresult - RED={red_score}, WHITE={white_score}, "
                  f"TOTAL={get_occupied_bitmask(self.state.red_bitboard, self.state.white_bitboard).bit_count()}")

    def print_previous_scores(self):
        red_score, white_score = self.scores_history[-1]
        print(f"\nresult - RED={red_score}, WHITE={white_score}, "
              f"TOTAL={get_occupied_bitmask(self.state.red_bitboard, self.state.white_bitboard).bit_count()}")
