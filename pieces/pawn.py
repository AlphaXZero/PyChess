from pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.moveset = [(-1, 0)] if color == "white" else [(1, 0)]
        if (self.y == 1 and self.color == "black") or (
            self.y == 6 and self.color == "white"
        ):
            self.moveset.append((-2 if self.color == "white" else 2, 0))
        self.starting_row = 2 if color == "white" else 7
        self.repeat = False
        self.repr = "♟"
