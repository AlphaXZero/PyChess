from board.board import Board
from ui.main_ui import MainWindow

if __name__ == "__main__":
    board = Board()
    board.new_board()
    board.print_board()
    print(board.get_piece(0, 2).get_move())
    app = MainWindow()
    app.mainloop()
