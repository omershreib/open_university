from __future__ import annotations
from models import ColorDiscPlayer, Move
from game_board import ReversiGameBoard
from game_state import GameState
from agents import ReversiAgent
from graphic_display import ReversiGraphicDisplay


class ReversiGameRunner:
    def __init__(self, board_size: int, max_agent: ReversiAgent, min_agent: ReversiAgent, verbose: bool = True):
        self.agents = {
            ColorDiscPlayer.RED: max_agent,
            ColorDiscPlayer.WHITE: min_agent
        }
        self.verbose = verbose

        board = ReversiGameBoard(board_size=board_size).initial_game_setup()
        self.state = GameState(board=board, player_turn=ColorDiscPlayer.RED)

        self.current_turn: int = 0
        self.moves_history: list[tuple[ColorDiscPlayer, Move]] = []

        self.graphical_display = ReversiGraphicDisplay(board_size=board_size, interactive=True, delay=0.01)
        self.graphical_display.initial_graphic_display()
        self.graphical_display.update(self.state)

    def current_agent(self) -> ReversiAgent:
        return self.agents[self.state.player_turn]

    def utility(self, player: ColorDiscPlayer) -> int:
        return self.state.board.calc_score(player) - self.state.board.calc_score(player.opposition())

    def next_step(self) -> None:
        if self.state.is_terminal():
            return

        player = self.state.player_turn
        agent = self.current_agent()
        move = agent.choose_move(self.state)
        legal_moves = self.state.actions()

        # for this_move in legal_moves:
        #     print(this_move.get_move())

        if move not in legal_moves:
            pass
            raise ValueError(f"agent {agent} played illegal move {move}\n"
                             f"legal moves: {[legal_move.get_move() for legal_move in legal_moves]}")

        self.moves_history.append((player, move))
        self.state = self.state.movement_result(move)
        self.graphical_display.update(state=self.state, player_move=move)

        if self.verbose:
            self._print_turn(player, move)

    def play(self, max_turns: int = 1000) -> GameState:
        if self.verbose:
            print("start game")
            print(self.state.board)
            print()

        while not self.state.is_terminal() and self.current_turn < max_turns:
            self.next_step()
            self.current_turn += 1

        red_score = self.state.board.calc_score(ColorDiscPlayer.RED)
        white_score = self.state.board.calc_score(ColorDiscPlayer.WHITE)

        if self.verbose:
            print("\ngame over")
            print(self.state.board)
            print(f"final scores: RED={red_score}, WHITE={white_score}")
            if red_score > white_score:
                print("RED win")
            elif white_score > red_score:
                print("WHITE win")
            else:
                print("DRAW")

        red_utility = self.utility(ColorDiscPlayer.RED)
        white_utility = self.utility(ColorDiscPlayer.WHITE)

        self.graphical_display.update(self.state, terminal=True, red_utility=red_utility, white_utility=white_utility)
        self.graphical_display.display()

        return self.state

    def _print_turn(self, player: ColorDiscPlayer, move: Move) -> None:
        if move.is_pass:
            print(f"{player.name} must PASS")
        else:
            print(f"{player.name} plays {move}")
        red = self.state.board.calc_score(ColorDiscPlayer.RED)
        white = self.state.board.calc_score(ColorDiscPlayer.WHITE)
        print(f"turn: {self.current_turn}, scores: RED={red}, WHITE={white}\n")
        print(self.state.board)
        print()
