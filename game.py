from board.board import Board
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.pawn import Pawn
from pieces.king import King
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.piece import Piece

if __name__ == "__main__":
    board = Board()
    board.new_board()
    board.print_board()
