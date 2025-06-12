from pieces.piece import Piece


class Bishop(Piece):
    def get_starting_cell():
        return [
            Bishop("white", 3, 1),
            Bishop("white", 6, 1),
            Bishop("black", 3, 8),
            Bishop("black", 6, 8),
        ]

    def get_move(self, position): ...
