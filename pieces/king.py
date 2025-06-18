from pieces.piece import Piece


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.moveset = [
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
            (0, -1),
            (0, 1),
            (-1, 0),
            (1, 0),
        ]
        self.repeat = False
        self.repr = "♚"
