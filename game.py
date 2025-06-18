from board.board import Board
from ui.main_ui import MainWindow

if __name__ == "__main__":
    board = Board()
    board.new_board()
    board.print_board()
    app = MainWindow()
    app.mainloop()
