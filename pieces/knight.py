from pieces.piece import Piece


class Knight(Piece):
    def get_starting_cell():
        return [
            Knight("white", 2, 1),
            Knight("white", 7, 1),
            Knight("black", 2, 8),
            Knight("black", 7, 8),
        ]

    def get_move(self, position): ...
