from abc import ABC


class Piece(ABC):
    def __init__(self, color, y, x):
        self.color = color
        self.y = y
        self.x = x

    def draw_piece(self, canvas, size, piece_colors, piece_lines):
        canvas.create_text(
            self.x * size + int(size * 0.52),
            self.y * size + int(size * 0.52),
            text=self.repr,
            font=("Helvetica", int(size * 0.7)),
            fill=piece_lines[self.color],
        )
        canvas.create_text(
            self.x * size + int(size * 0.5),
            self.y * size + int(size * 0.5),
            text=self.repr,
            font=("Helvetica", int(size * 0.7)),
            fill=piece_colors[self.color],
        )

    def __repr__(self):
        return f"{self.__class__.__name__};{self.color};{self.y};{self.x}"

    def convert_chess_coordinate(self, y=None, x=None):
        chess_row = ["a", "b", "c", "d", "e", "f", "g", "h"]
        if y and x:
            return (chess_row[x], y)
        return (chess_row[self.x], self.y)
