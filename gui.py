"""
graphical user interface for chess game

"""

import json
from copy import deepcopy
from tkinter import messagebox
import ttkbootstrap as tk
import engine
from pieces_draw import (
    SIZE,
    draw_bishop,
    draw_help_circles,
    draw_king,
    draw_knight,
    draw_pawn,
    draw_queen,
    draw_rook,
    draw_warn_circles,
    LINE_SETTINGS,
)

with open("themes.json", "r") as f:
    themes = json.load(f)
COLOR_CHOICE = themes["user choice"]
COLOR_THEME = themes["color theme"]

current_board = engine.board
past_board = [deepcopy(current_board)]
COLOR = ("white", "black")
GAME_TURN = len(engine.history)
FONT_SETTINGS = {"font": ("Times New Roman", 14)}


def build_app() -> tk.Window:
    """
    create the mainframe and launch the GUI

    Returns:
        tk.Window: main window
    """
    global top_text, root
    root = tk.Window(title="PyChess", themename="darkly", minsize=(SIZE * 8, SIZE * 8))
    build_top_frame(root)
    build_mainframe(root)
    root.position_center()
    draw_board()
    bind_board_click_handler()
    return root


def reset_game_vars() -> None:
    """
    Reset the game state, clear move history, and update UI to initial values.
    """
    global GAME_TURN, past_board
    engine.history = []
    GAME_TURN = 0
    history_label.config(state="normal")
    history_label.delete("1.0", tk.END)
    engine.occu_board = 0
    past_board = []


def restart_game() -> None:
    """
    Prompt the user to restart the game and reset board and state upon confirmation
    """
    global current_board
    is_yes = messagebox.askyesno(
        title="Restart ?",
        message="Do you want to restart the game ?",
    )
    if is_yes:
        with open("board.json", "r") as f:
            boards = json.load(f)
        boards["current"] = []
        with open("board.json", "w") as f:
            json.dump(boards, f)
        current_board = boards["default"]
        reset_game_vars()
        draw_board()


def build_top_frame(parent: tk.Window) -> None:
    """
    Create the top frame with turn indicator, restart button, and theme selection

    Args:
        parent (tk.Window): main window
    """
    global top_text

    top_frame = tk.Frame(parent, borderwidth=4)
    top_frame.pack(side="top", fill="x", expand=True)

    top_text = tk.StringVar()
    turn_label = tk.Label(top_frame, text="Game Turn : ", **FONT_SETTINGS)
    turn_label.pack(side="left", pady=4, padx=2)
    turn_text = tk.Label(top_frame, textvariable=top_text, **FONT_SETTINGS)
    turn_text.pack(side="left", pady=4)
    update_turn_label()

    button = tk.Button(
        top_frame, command=restart_game, text="Restart", bootstyle="danger"
    )
    button.pack(side="left", padx=(SIZE * 4.6) / 2, pady=4)

    theme_label = tk.Label(top_frame, text="Theme :", **FONT_SETTINGS)
    theme_combobox = tk.Combobox(
        top_frame, values=list(COLOR_THEME.keys()), width=15, state="readonly"
    )
    theme_combobox.pack(side="right", padx=7, pady=4)
    theme_label.pack(side="right", padx=10, pady=4)
    theme_combobox.set(COLOR_CHOICE)

    def change_theme(event):
        """
        change the theme of the checkerboard
        """
        global COLOR_CHOICE

        COLOR_CHOICE = theme_combobox.get()
        themes["user choice"] = COLOR_CHOICE
        with open("themes.json", "w") as f:
            json.dump(themes, f)
        draw_board()

    theme_combobox.bind("<<ComboboxSelected>>", change_theme)


def update_turn_label() -> None:
    """
    Update the UI label to reflect the current player's turn.
    """
    global top_text
    top_text.set(f"{COLOR[(GAME_TURN % 2)]}")


def build_mainframe(parent: tk.Window) -> None:
    """
    build the mainframe with checkerboard on the left and history on the right
    """
    global checker_board_canvas, history_label
    check_frame = tk.Frame(parent, borderwidth=4)
    check_frame.pack(side="left", fill="both")
    history_frame = tk.Frame(parent, borderwidth=4)
    history_frame.pack(side="left", fill="both")
    scrollbar = tk.Scrollbar(history_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    history_label = tk.Text(
        history_frame, width=20, yscrollcommand=scrollbar.set, **FONT_SETTINGS
    )
    history_label.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.config(command=history_label.yview)
    update_history(True)

    checker_board_canvas = tk.Canvas(check_frame, width=SIZE * 8, height=SIZE * 8)
    checker_board_canvas.pack(fill="both", expand=True, anchor="center")
    checker_board_canvas.configure(width=SIZE * 8, height=SIZE * 8)
    draw_grid()


def update_history(init: bool = False) -> None:
    """
    add move in the history

    Args:
        init (bool, optional): If true add the previous history. Defaults to False.
    """
    history_label.config(state="normal")
    if init:
        history_label.insert(
            tk.END, "\n".join(engine.format_history(engine.history)) + "\n"
        )
    else:
        history_label.insert(tk.END, engine.format_history(engine.history)[-1] + "\n")
    history_label.see(tk.END)
    history_label.config(state="disabled")


def draw_grid() -> None:
    """
    Draw the chessboard grid and row/column labels on the canvas.
    """
    global checker_board_canvas
    bottom_label = engine.X_NAME

    for i in range(8):
        for y in range(8):
            if i % 2 == y % 2:
                checker_board_canvas.create_rectangle(
                    SIZE * i,
                    SIZE * y,
                    SIZE + (SIZE * i),
                    SIZE + (SIZE * y),
                    fill=COLOR_THEME[COLOR_CHOICE]["white_board"],
                )
            else:
                checker_board_canvas.create_rectangle(
                    SIZE * i,
                    SIZE * y,
                    SIZE + (SIZE * i),
                    SIZE + (SIZE * y),
                    fill=COLOR_THEME[COLOR_CHOICE]["black_board"],
                )
            if i == 0:
                checker_board_canvas.create_text(
                    (SIZE * i) + SIZE * 0.1,
                    (SIZE * y) + SIZE * 0.1,
                    text=8 - (y),
                    font=("Times New Roman", 18, "bold"),
                )
            if y == 7:
                checker_board_canvas.create_text(
                    (SIZE * i) + SIZE * 0.92,
                    (SIZE * y) + SIZE * 0.92,
                    text=bottom_label[i],
                    font=("Times New Roman", 18, "bold"),
                )


def draw_board():
    """
    draw the current board with every piece
    """
    draw_grid()
    for i, line in enumerate(current_board):
        for j, piece in enumerate(line):
            draw_piece(piece, j, i)


def draw_piece(piece: str, x: int, y: int):
    """
    Draw a single chess piece at the specified board coordinates

    Args:
        piece (str): piece we want to draw
        x (int): col
        y (int): row
    """
    global DRAW_SETTINGS
    if piece[0] != "0":
        DRAW_SETTINGS = {
            "outline": COLOR_THEME[COLOR_CHOICE][piece[1]]["fill"],
            "fill": COLOR_THEME[COLOR_CHOICE][piece[1]]["fill"],
        }
        LINE_SETTINGS.update({"fill": COLOR_THEME[COLOR_CHOICE][piece[1]]["line"]})
    if piece[0] == "bishop":
        draw_bishop(x, y, DRAW_SETTINGS, checker_board_canvas)
    if piece[0] == "rook":
        draw_rook(x, y, DRAW_SETTINGS, checker_board_canvas)
    if piece[0] == "pawnb":
        draw_pawn(x, y, DRAW_SETTINGS, checker_board_canvas)
    if piece[0] == "pawnw":
        draw_pawn(x, y, DRAW_SETTINGS, checker_board_canvas)
    if piece[0] == "knight":
        draw_knight(x, y, DRAW_SETTINGS, checker_board_canvas)
    if piece[0] == "queen":
        draw_queen(x, y, DRAW_SETTINGS, checker_board_canvas)
    if piece[0] == "king":
        draw_king(x, y, DRAW_SETTINGS, checker_board_canvas)


def bind_board_click_handler() -> None:
    """
    Bind mouse click event on the board to display possible moves
    """
    global checker_board_canvas
    checker_board_canvas.bind("<Button-1>", show_possible_moves)


current_move = []


def show_possible_moves(event) -> None:
    """
    shows possibles moves on the piece user clicked on
    """
    global current_move
    x = event.x // SIZE
    y = event.y // SIZE

    possible_moves = engine.list_valid_move(current_board, (y, x))
    if len(current_move) == 0 and current_board[y][x][1] == COLOR[(GAME_TURN % 2)]:
        draw_help_circles(possible_moves, checker_board_canvas)
        current_move.append((y, x))
    elif len(current_move) == 1 and current_board[y][x][1] == COLOR[(GAME_TURN % 2)]:
        draw_board()
        draw_help_circles(possible_moves, checker_board_canvas)
        current_move = [(y, x)]
    else:
        current_move.append((y, x))
    if len(current_move) == 2:
        do_move(
            current_move[0][0],
            current_move[0][1],
            current_move[1][0],
            current_move[1][1],
            COLOR[GAME_TURN % 2],
        )
        current_move = []

    warn_check("white")
    warn_check("black")


def warn_check(color: str) -> None:
    """
    highlight cells were pieces are checking the king

    Args:
        color (str): color of the player
    """
    for cell in engine.get_checking_pieces(
        current_board, engine.find_king(current_board, color)
    ):
        draw_warn_circles(cell, checker_board_canvas)


def do_move(y: int, x: int, newy: int, newx: int, color: str) -> None:
    """
    move the piece if possible and informs of the game state afterward

    Args:
        y (int): row before move
        x (int): col before move
        newy (int): row after move
        newx (int): col after move
        color (str): color of the player
    """
    global GAME_TURN, past_board
    if engine.move_piece(current_board, (y, x), (newy, newx), color) is not None:
        if engine.is_draw_repetitions(current_board, past_board) or engine.is_stalemate(
            current_board, engine.find_king(current_board, COLOR[((GAME_TURN + 1) % 2)])
        ):
            messagebox.showinfo(title="draw", message="draw")
        else:
            past_board.append(deepcopy(current_board))
        if engine.is_checkmate(
            current_board, engine.find_king(current_board, COLOR[((GAME_TURN + 1) % 2)])
        ):
            messagebox.showinfo(f"Congratulations ! {color} won")
            with open("board.json", "r") as f:
                boards = json.load(f)
            boards["current"] = []
            with open("board.json", "w") as f:
                json.dump(boards, f, indent=4)

        GAME_TURN += 1
        update_turn_label()
        update_history()
    draw_board()


if __name__ == "__main__":
    pass
