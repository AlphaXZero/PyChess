from pieces.piece import Piece

class Queen(Piece):
    def get_available_move(self): ...

    @staticmethod
    def get_starting_cell():
        return [Queen("white", 4, 1), Queen("black", 4, 8)]

    def get_move(self, position):...