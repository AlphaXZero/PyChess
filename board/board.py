from pieces.queen import Queen
from pieces.rook import Rook
from pieces.pawn import Pawn
from pieces.king import King
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.piece import Piece
import colorama as c


class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.game_turn = 1
        self.color_turn = self.get_color_turn()

    def get_color_turn(self):
        return ("white", "black")[(self.game_turn - 1) % 2]

    def get_piece(self, y, x):
        if 0 <= x < 8 and 0 <= y < 8:
            return self.board[y][x]
        return None

    def new_board(self):
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

    def print_board(self):
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
