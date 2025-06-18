from tkinter import ttk, Canvas, messagebox
from board.board import Board
import json


class BoardUI(ttk.Frame):
    def __init__(self, parent, size):
        super().__init__(parent)
        self.size = size
        self.case_size = size // 8
        self.load_theme()
        self.move_choice = []
        self.possible_moves = None

        self.canvas = Canvas(self, width=self.size, height=self.size)
        self.canvas.pack(side="right", expand=True, fill="both")
        self.canvas.bind("<Button-1>", self.show_possible_moves)

        self.current_board = Board()
        self.current_board.new_board()
        self.update_board()

    def load_theme(self, choice=None):
        try:
            with open("themes.json", "r") as f:
                themes = json.load(f)
        except FileNotFoundError:
            messagebox.showerror(
                "Error", "themes.json file not found. Using default theme."
            )
            themes = {
                "color_theme": {
                    "Classic": {
                        "white": {"fill": "#f2f2f2", "line": "black"},
                        "black": {"fill": "#464646", "line": "black"},
                        "black_board": "#777777",
                        "white_board": "#ffffff",
                    }
                },
                "user_choice": "Classic",
            }
        self.user_theme_choice = choice or themes["user_choice"]

        self.piece_colors = {
            "white": themes["color_theme"][self.user_theme_choice]["white"]["fill"],
            "black": themes["color_theme"][self.user_theme_choice]["black"]["fill"],
        }
        self.piece_lines = {
            "white": themes["color_theme"][self.user_theme_choice]["white"]["line"],
            "black": themes["color_theme"][self.user_theme_choice]["black"]["line"],
        }
        self.board_colors = (
            themes["color_theme"][self.user_theme_choice]["black_board"],
            themes["color_theme"][self.user_theme_choice]["white_board"],
        )
        return themes

    def update_board(self):
        for row in range(8):
            for col in range(8):
                x1 = col * self.case_size
                y1 = row * self.case_size
                x2 = x1 + self.case_size
                y2 = y1 + self.case_size
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=self.board_colors[(row + col) % 2], outline=""
                )
        self.draw_pieces()

    def draw_pieces(self):
        for row in self.current_board.board:
            for piece in row:
                if piece is not None:
                    piece.draw_piece(
                        self.canvas, self.case_size, self.piece_colors, self.piece_lines
                    )

    def draw_help_circles(self, possible_moves):
        for y, x in possible_moves:
            self.canvas.create_oval(
                (x * self.case_size) + self.case_size * 0.4,
                (y * self.case_size) + self.case_size * 0.4,
                (x * self.case_size) + self.case_size * 0.6,
                (y * self.case_size) + self.case_size * 0.6,
                outline="blue",
                width=4,
            )

    def show_possible_moves(self, event):
        x = event.x // self.case_size
        y = event.y // self.case_size
        self.possible_moves = self.possible_moves or self.current_board.check_move(y, x)

        if self.move_choice == [] and self.possible_moves != []:
            self.draw_help_circles(self.possible_moves)
            self.move_choice.append((y, x))
        elif len(self.move_choice) == 1 and (y, x) in self.possible_moves:
            self.draw_help_circles(self.possible_moves)
            self.move_choice.append((y, x))

        # elif len(self.move_choice) == 1 and :
        else:
            self.move_choice = []
            self.possible_moves = None
            self.update_board()
        print(self.move_choice)

    def show_move(self): ...
