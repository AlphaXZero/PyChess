from pieces.piece import Piece


class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.moveset = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def draw_piece(self, canvas, size, piece_colors):
        canvas.create_text(
            self.x * size + int(size * 0.54),
            self.y * size + int(size * 0.35),
            text="♜",
            font=("Arial", 120),
            fill=piece_colors[self.color],
        )
