from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    @abstractmethod
    def get_starting_cell():
        pass

    @abstractmethod
    def get_move(self, position):
        pass

    def convert_chess_coordinate(self):
        chess_row = ["a", "b", "c", "d", "e", "f", "g", "h"]
        return (chess_row[self.x], self.y)
