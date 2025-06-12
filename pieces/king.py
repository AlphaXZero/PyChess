from pieces.piece import Piece


class King(Piece):
    def get_starting_cell():
        return [King("white", 5, 1), King("black", 5, 8)]

    def get_move(self, position): ...
