from pieces.piece import Piece


class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.moveset = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        self.repr = "♝"
        self.repeat = True
