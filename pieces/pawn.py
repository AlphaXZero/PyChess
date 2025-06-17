from pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.moveset = [(0, 1)] if color == "white" else [(0, -1)]
        self.starting_row = 2 if color == "white" else 7
        self.repeat = range(1, 3)

    def draw_piece(self, canvas, size, piece_colors):
        canvas.create_text(
            self.x * size + int(size * 0.56),
            self.y * size + int(size * 0.30),
            text="♟",
            font=("Arial", 120),
            fill=piece_colors[self.color],
        )
