from pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

        self.starting_row = 2 if color == "white" else 7
        self.repeat = False
        self.repr = "♟"
        self.controled_cell = (
            [(-1, -1), (-1, 1)] if self.color == "white" else [(1, 1), (1, -1)]
        )

    @property
    def moveset(self):
        if self.color == "white":
            return [(-1, 0), (-2, 0)] if self.y == 6 else [(-1, 0)]
        else:
            return [(1, 0), (2, 0)] if self.y == 1 else [(1, 0)]
