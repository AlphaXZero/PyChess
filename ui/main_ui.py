from board.board import Board
import tkinter as tk
import ttkbootstrap as ttk
import json
from ui.board_ui import BoardUI


class MainWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly", minsize=(900, 870))
        self.title("Chess Game")
        self.size = 1150
        self.board_size = int(self.size * 0.7)
        self.font = ("Roboto", 18)
        self.geometry(f"{self.size}x{int(self.size * 0.76)}")

        self.main_frame = ttk.Frame(self, borderwidth=4)
        self.main_frame.pack(expand=True, fill="both")

        self.build_top_frame()
        self.build_checkerboard()

    def build_top_frame(self):
        top_frame = ttk.Frame(self.main_frame, borderwidth=4)
        top_frame.pack(side="top", fill="x")

        label_text_turn_label = ttk.Label(
            top_frame,
            text="Player turn:",
            font=self.font,
        )
        label_text_turn_label.pack(side="left", padx=(6, 0), pady=5)

        self.text_turn = tk.StringVar(value="White")
        turn_label = ttk.Label(
            top_frame,
            textvariable=self.text_turn,
            font=self.font,
        )
        turn_label.pack(side="left", padx=(1, 0), pady=5)

        theme_label = tk.Label(top_frame, text="Theme :", font=self.font)
        self.themes = BoardUI.load_theme(self)
        self.themes_combobox = ttk.Combobox(
            top_frame,
            values=list(self.themes["color_theme"].keys()),
            width=15,
            state="readonly",
        )
        self.themes_combobox.pack(side="right", padx=7, pady=4)
        theme_label.pack(side="right", padx=10, pady=4)
        self.themes_combobox.set(BoardUI.load_theme(self)["user_choice"])
        self.themes_combobox.bind("<<ComboboxSelected>>", self.change_theme)

    def change_theme(self, event=None):
        self.themes["user_choice"] = self.themes_combobox.get()
        with open("themes.json", "w") as f:
            json.dump(self.themes, f)
        self.boardui.load_theme()
        self.boardui.update_board()

    def build_checkerboard(self):
        checkerboard_frame = ttk.Frame(self.main_frame, borderwidth=4)
        checkerboard_frame.pack(side="left")

        self.boardui = BoardUI(checkerboard_frame, self.board_size)
        self.boardui.pack()
