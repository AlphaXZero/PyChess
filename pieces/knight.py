from pieces.piece import Piece


class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.moveset = [
            (-2, -1),
            (-2, 1),
            (2, -1),
            (2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
        ]
        self.repeat = False
        self.repr = "♞"
