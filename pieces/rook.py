from pieces.piece import Piece


class Rook(Piece):
    @staticmethod
    def get_starting_cell():
        return [
            Rook("white", 1, 1),
            Rook("white", 8, 1),
            Rook("black", 1, 8),
            Rook("black", 8, 8),
        ]

    def get_move(self, position): ...
