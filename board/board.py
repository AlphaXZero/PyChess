from pieces.queen import Queen
from pieces.rook import Rook
from pieces.pawn import Pawn
from pieces.king import King
from pieces.bishop import Bishop
from pieces.knight import Knight
import colorama as c


class Board:
    def __init__(self):
        self.board = []

    def new_board(self):
        self.board = [
            *Queen.get_starting_cell(),
            *Rook.get_starting_cell(),
            *Pawn.get_starting_cell(),
            *King.get_starting_cell(),
            *Bishop.get_starting_cell(),
            *Knight.get_starting_cell(),
        ]

    def print_board(self):
        board_repr = [[("0", "0") for i in range(8)] for j in range(8)]
        c.init()
        for obj in self.board:
            board_repr[8 - obj.y][obj.x - 1] = (obj.__class__.__name__, obj.color)
        print(board_repr)
        for i, line in enumerate(board_repr):
            print(8 - i, end=" ")
            for cell in line:
                if cell[0] == "white":
                    print(
                        c.Back.RED + (cell[0][0]) + c.Style.RESET_ALL,
                        end=" ",
                    )
                elif cell[1] == "black":
                    print(
                        c.Back.BLUE + (cell[0][0]) + c.Style.RESET_ALL,
                        end=" ",
                    )
                else:
                    print(cell[0][0], end=" ")
            print()
        # print(" ", " ".join(X_NAME))
