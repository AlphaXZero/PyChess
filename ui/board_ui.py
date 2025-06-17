from tkinter import ttk, Canvas, messagebox
from board.board import Board
import json


class BoardUI(ttk.Frame):
    def __init__(self, parent, size):
        super().__init__(parent)
        self.size = size // 8
        self.load_theme()

        self.canvas = Canvas(self, width=self.size, height=self.size)
        self.canvas.pack(side="right", expand=True, fill="both")

        self.current_board = Board()
        self.current_board.new_board()
        self.current_board.print_board()
        self.update_board()

    def load_theme(self):
        try:
            with open("themes.json", "r") as f:
                themes = json.load(f)
        except FileNotFoundError:
            messagebox.showerror(
                "Error", "themes.json file not found. Using default theme."
            )
            themes = {
                "color theme": {
                    "Classic": {
                        "white": {"fill": "#f2f2f2", "line": "black"},
                        "black": {"fill": "#464646", "line": "black"},
                        "black_board": "#777777",
                        "white_board": "#ffffff",
                    }
                },
                "user choice": "Classic",
            }
        self.piece_colors = {
            "white": themes["color theme"][themes["user choice"]]["white"]["fill"],
            "black": themes["color theme"][themes["user choice"]]["black"]["fill"],
        }
        self.piece_lines = {
            "white": themes["color theme"][themes["user choice"]]["white"]["line"],
            "black": themes["color theme"][themes["user choice"]]["black"]["line"],
        }
        self.board_colors = (
            themes["color theme"][themes["user choice"]]["black_board"],
            themes["color theme"][themes["user choice"]]["white_board"],
        )

    def update_board(self):
        for row in range(8):
            for col in range(8):
                x1 = col * self.size
                y1 = row * self.size
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=self.board_colors[(row + col) % 2], outline=""
                )
        self.draw_pieces()

    def draw_pieces(self):
        for row in self.current_board.board:
            for piece in row:
                if piece is not None:
                    piece.draw_piece(self.canvas, self.size, self.piece_colors)
