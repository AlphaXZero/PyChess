from board.board import Board
import tkinter as tk
import ttkbootstrap as ttk
from ui.board_ui import BoardUI


class MainWindow(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Chess Game")
        self.size = 1150
        self.geometry(f"{self.size}x{int(self.size * 0.77)}")

        main_frame = ttk.Frame(self, borderwidth=4)
        main_frame.pack(expand=True, fill="both")

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(side="top", fill="x")

        label_text_turn_label = ttk.Label(
            top_frame,
            text="Player turn:",
            font=("Roboto", 18),
        )
        label_text_turn_label.pack(side="left", padx=(6, 0), pady=5)

        self.text_turn = tk.StringVar(value="White")
        turn_label = ttk.Label(
            top_frame,
            textvariable=self.text_turn,
            font=("Roboto", 18),
        )
        turn_label.pack(side="left", padx=(1, 0), pady=5)

        self.boardui = BoardUI(main_frame, int(self.size * 0.7))
        self.boardui.pack(side="right", expand=True, fill="both", padx=5, pady=5)
