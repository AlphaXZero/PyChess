from pieces.piece import Piece


class Pawn(Piece):
    def get_starting_cell():
        return [Pawn("white", i, 2) for i in range(1, 9)] + [
            Pawn("black", i, 7) for i in range(1, 9)
        ]

    def get_move(self, position): ...
