from graphic_display import ReversiGraphicDisplay
from models import Color, Move

LEGAL_DISCS_FLIPS_DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 1),
    (1, -1), (1, 0), (1, 1),
]


def assert_board_size(n):
    if n % 2 != 0 or n < 6:
        raise ValueError(f"board size must be number (greater then or equal to 6)")


class ReversiGameBoard(ReversiGraphicDisplay):
    def __init__(self, board_size):
        assert_board_size(board_size)

        ReversiGraphicDisplay.__init__(self, board_size)
        self.board_size = board_size

        self.grid = None
        self.is_empty_board = False

    def is_point_in_board_boundaries(self, point) -> bool:
        x, y = point
        return 0 <= x < self.board_size and 0 <= y < self.board_size

    def is_point_location_empty(self, point) -> bool:
        x, y = point
        if self.grid[x][y] is not None:
            raise Exception(f"this is illegal move to put a disc on a non-empty position: {point}")

        return True

    def is_legal_point(self, point) -> bool:
        if not self.is_point_in_board_boundaries(point):
            return False

        if not self.is_point_location_empty(point):
            return False

        return True

    def is_legal_flipping_discs_point(self, oppo_player: Color, point) -> bool:
        if not self.is_point_in_board_boundaries(point):
            return False

        x, y = point

        if not self.grid[x][y] == oppo_player:
            return False

        return True

    def build_empty_board(self):
        qubic_range = range(self.board_size)
        self.grid = [[None for _ in qubic_range] for __ in qubic_range]
        self.is_empty_board = True

    def initial_game_setup(self):
        if not self.is_empty_board:
            self.build_empty_board()
            self.initial_graphic_display()

        top_left_center = int(self.board_size / 2) - 1
        red_player_init_top_point = (top_left_center, top_left_center)
        red_player_init_bottom_point = (top_left_center + 1, top_left_center + 1)
        white_player_init_top_point = (top_left_center + 1, top_left_center)
        white_player_init_bottom_point = (top_left_center, top_left_center + 1)

        self.add_point(Color.RED, red_player_init_top_point)
        self.add_point(Color.RED, red_player_init_bottom_point)
        self.add_point(Color.WHITE, white_player_init_top_point)
        self.add_point(Color.WHITE, white_player_init_bottom_point)

    def _add_point(self, player_disc, point):
        if self.is_legal_point(point):
            x, y = point
            self.grid[x][y] = player_disc

    def add_point(self, player_disc, point):
        self._add_point(player_disc, point)
        self.add_disc(player_disc, point)

    def calc_score(self, player: Color) -> int:
        qubic_range = range(self.board_size)
        return sum(1 for row in qubic_range for column in qubic_range if self.grid[row][column] == player)

    def is_full(self):
        qubic_range = range(self.board_size)
        return sum(1 for row in qubic_range for column in qubic_range if self.grid[row][column] is not None)

    def opposition_discs_flips_based_move(self, player: Color, point: tuple[int, int]) -> list[tuple[int, int]]:
        is_legal = self.is_legal_point(point)

        if not is_legal:
            return []

        if is_legal:
            x, y = point
            oppo_player = player.opposition()
            total_flips: list = []

            for hor_direction, ver_direction in LEGAL_DISCS_FLIPS_DIRECTIONS:
                flips: list = []

                # set potential flipping point around the player's point movement
                flip_x = x + hor_direction
                flip_y = y + ver_direction
                flipping_point = (flip_x, flip_y)

                while self.is_legal_flipping_discs_point(oppo_player, flipping_point):
                    flips.append(flipping_point)
                    flip_x += hor_direction
                    flip_y += ver_direction
                    flipping_point = (flip_x, flip_y)

                if flips:
                    total_flips.extend(flips)

            return total_flips

    def legal_moves(self, player) -> list[Move]:
        pass

    def apply_player_move(self, move) -> "ReversiGameBoard":
        pass

    def count_player_discs(self, player) -> int:
        pass
