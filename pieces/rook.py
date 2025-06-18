from pieces.piece import Piece


class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.moveset = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        self.repr="♜"
        self.repeat = True