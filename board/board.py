from pieces.queen import Queen
from pieces.rook import Rook
from pieces.pawn import Pawn
from pieces.king import King
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.piece import Piece
from copy import deepcopy
import colorama as c


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.previous_board = deepcopy(self.board)
        self.game_turn = 1
        self.capture = {"white": [], "black": []}
        self.history = []

    @property
    def color_turn(self) -> str:
        return ("white", "black")[(self.game_turn - 1) % 2]

    @property
    def opponent_color(self) -> str:
        return ("white", "black")[(self.game_turn) % 2]

    def get_piece(self, y: int, x: int) -> Piece | None:
        if 0 <= x < 8 and 0 <= y < 8:
            return self.board[y][x]
        return None

    def new_board(self) -> None:
        for i in range(8):
            for j in range(8):
                if i == 0 or i == 7:
                    if j in (0, 7):
                        self.board[i][j] = Rook("white" if i == 7 else "black", i, j)
                    elif j in (1, 6):
                        self.board[i][j] = Knight("white" if i == 7 else "black", i, j)
                    elif j in (2, 5):
                        self.board[i][j] = Bishop("white" if i == 7 else "black", i, j)
                    elif j == 3:
                        self.board[i][j] = Queen("white" if i == 7 else "black", i, j)
                    elif j == 4:
                        self.board[i][j] = King("white" if i == 7 else "black", i, j)
                elif i in (1, 6):
                    self.board[i][j] = Pawn("white" if i == 6 else "black", i, j)

    def print_board(self) -> None:
        X_NAME = ["a", "b", "c", "d", "e", "f", "g", "h"]
        X_NAME = ["a", "b", "c", "d", "e", "f", "g", "h"]
        c.init()
        for i, line in enumerate(self.board):
            print(8 - i, end=" ")
            for cell in line:
                if isinstance(cell, Piece):
                    color = c.Back.WHITE if cell.color == "white" else c.Back.BLACK
                    print(
                        color + cell.__class__.__name__[0:2] + c.Style.RESET_ALL,
                        end=" ",
                    )
                else:
                    print("0", end="  ")
            print()
        print(" ", "  ".join(X_NAME))

    def check_move(self, y: int, x: int, only_control=False) -> list[tuple[int, int]]:
        piece = self.get_piece(y, x)
        moves = []
        move_distance_range = 8 if piece.repeat else 2
        if piece.color != self.color_turn or piece is None:
            return moves
        if isinstance(piece, Pawn):
            return self.check_pawn_move(y, x)
        for dy, dx in piece.moveset:
            for step in range(1, move_distance_range):
                new_x = piece.x + dx * step
                new_y = piece.y + dy * step
                if not (0 <= new_x <= 7 and 0 <= new_y <= 7):
                    break
                cell_item = self.get_piece(new_y, new_x)
                if cell_item is None:
                    moves.append((new_y, new_x))
                elif piece.color != cell_item.color:
                    moves.append((new_y, new_x))
                    break
                else:
                    break
        return moves

    def check_pawn_move(self, y: int, x: int) -> list[tuple[int, int]]:
        valid_moves = []
        piece = self.get_piece(y, x)
        new_y, new_x = piece.y + piece.moveset[0][0], piece.x + piece.moveset[0][1]
        if 0 <= new_y <= 7 and 0 <= new_x <= 7 and self.board[new_y][new_x] is None:
            valid_moves.append((new_y, new_x))
            if len(piece.moveset) == 2:
                new_y, new_x = (
                    piece.y + piece.moveset[1][0],
                    piece.x + piece.moveset[1][1],
                )
                if (
                    0 <= new_y <= 7
                    and 0 <= new_x <= 7
                    and self.board[new_y][new_x] is None
                ):
                    valid_moves.append((new_y, new_x))
        for dy, dx in piece.controled_cell:
            new_y, new_x = piece.y + dy, piece.x + dx
            capturable_piece = self.get_piece(new_y, new_x)
            if (
                0 <= new_y <= 7
                and 0 <= new_x <= 7
                and capturable_piece is not None
                and capturable_piece.color != piece.color
            ):
                valid_moves.append((new_y, new_x))
        return valid_moves

    def do_move(self, inital_pos: tuple[int, int], final_pos: tuple[int, int]) -> None:
        y, x = inital_pos
        newy, newx = final_pos
        moving_piece = self.get_piece(y, x)
        piece_destination = self.get_piece(newy, newx)
        if moving_piece:
            if piece_destination and piece_destination.color == moving_piece.color:
                return
            if piece_destination:
                self.capture[moving_piece.color].append(moving_piece.__class__.__name__)
            self.board[newy][newx], self.board[y][x] = self.board[y][x], None
            self.update_history(newy, newx)
            moving_piece.x, moving_piece.y = newx, newy
            self.game_turn += 1

    def update_history(self, ny: int, nx: int) -> None:
        piece: Piece = self.get_piece(ny, nx)
        self.history.append(
            {
                "turn": self.game_turn,
                "inital": piece.convert_chess_coordinate(),
                "final": piece.convert_chess_coordinate(ny, nx),
                "capture": deepcopy(self.capture),
            }
        )
        print(self.history)

    def list_checking_pieces(self, y: int, x: int) -> list[int, int]:
        """
        Returns a list of coordinates (y, x) of all pieces that are currently checking
        a specific target cell
        """
        checking_pieces = []
        temp_piece = (
            Queen(self.opponent_color, y, x)
            if self.get_piece(y, x) is None
            else self.get_piece(y, x)
        )
        self.board[y][x] = temp_piece
        for row in self.board:
            for piece in row:
                if isinstance(piece, Piece):
                    if (y, x) in self.check_move(piece.y, piece.x):
                        checking_pieces.append(self.get_piece(piece.y, piece.x))
        self.board[y][x] = None
        return checking_pieces

    def find_king(self):
        for row in self.board:
            for piece in row:
                if (
                    isinstance(piece, Piece)
                    and piece.__class__.__name__ == "King"
                    and piece.color == self.color_turn
                ):
                    return piece


if __name__ == "__main__":
    board2 = Board()
    board2.new_board()
    board2.print_board()
    print(board2.find_king())
