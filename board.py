from pieces.queen import Queen
from pieces.rook import Rook


class Board:
    def __init__(self):
        self.board = []

    def new_board(self):
        self.board = [*Queen.get_starting_cell(), *Rook.get_starting_cell()]

    def __repr__(self):
        board_repr = [piece.__dict__ for piece in self.board]
        return str(board_repr)


if __name__ == "__main__":
    board=Board()
    board.new_board()
    print(board)
