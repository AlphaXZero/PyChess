from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, color, y, x):
        self.color = color
        self.y = y
        self.x = x
        self.repeat = range(1, 8)

    def get_move(self):
        moves = []
        for dy, dx in self.moveset:
            for step in self.repeat:
                new_x = self.x + dx * step
                new_y = self.y + dy * step
                if 0 <= new_x <= 7 and 0 <= new_y <= 7:
                    moves.append((new_y, new_x))
                else:
                    break
        return moves

    def convert_chess_coordinate(self):
        chess_row = ["a", "b", "c", "d", "e", "f", "g", "h"]
        return (chess_row[self.x], self.y)
