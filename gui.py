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


def build_app() -> tk.Window:
    global text_top, root
    root = tk.Window(title="PyChess", themename="darkly", minsize=(SIZE * 8, SIZE * 8))
    text_top = tk.StringVar()
    build_top_frame(root)
    build_checkerboard(root)
    root.position_center()
    draw_board()
    move_piece_GUI()
    return root


def reset_var():
    global GAME_TURN, past_board
    engine.history = []
    GAME_TURN = 0
    label_spec.config(state="normal")
    label_spec.delete("1.0", tk.END)
    engine.occu_board = 0
    past_board = []


def restart_game():
    global current_board
    is_yes = messagebox.askyesno(
        title="Recommencer ?",
        message="Etes vous sûr de vouloir recommencer la partie ?",
    )
    if is_yes:
        with open("board.json", "r") as f:
            boards = json.load(f)
        boards["current"] = []
        with open("board.json", "w") as f:
            json.dump(boards, f)
        current_board = boards["default"]
        reset_var()
        draw_board()


def build_top_frame(parent):
    global text_top

    frame = tk.Frame(
        parent,
        borderwidth=2,
        relief="groove",
    )
    frame.pack(side="top", fill="x", expand=True)

    label = tk.Label(frame, text="Game Turn : ", font=("Times New Roman", 14))
    label.pack(side="left", pady=4, padx=2)
    turn_text = tk.Label(
        frame, textvariable=text_top, font=("Times New Roman", 14, "bold")
    )
    turn_text.pack(side="left", pady=4)
    button = tk.Button(
        frame,
        command=restart_game,
        text="Restart",
        bootstyle="danger",
    )
    # TODO demander cderic
    # button.config(font=("Times New Roman", 14, "bold"))
    button.pack(side="left", padx=(SIZE * 4.6) / 2, pady=4)

    theme_label = tk.Label(frame, text="Theme :", font=("Times New Roman", 14))

    theme_combobox = tk.Combobox(
        frame,
        values=list(COLOR_THEME.keys()),
        width=15,
        state="readonly",
    )
    theme_combobox.pack(side="right", padx=7, pady=4)
    theme_label.pack(side="right", padx=10)
    theme_combobox.set(COLOR_CHOICE)

    def change_theme(event):
        global COLOR_CHOICE

        COLOR_CHOICE = theme_combobox.get()
        themes["user choice"] = COLOR_CHOICE
        f = open("themes.json", "w")
        f.write(json.dumps(themes))
        f.close()
        draw_board()

    theme_combobox.bind("<<ComboboxSelected>>", change_theme)

    update_turn_lab()


def update_turn_lab():
    global text_top
    text_top.set(f"{COLOR[(GAME_TURN % 2)]}")


def build_checkerboard(parent):
    global canvas, label_spec
    frame = tk.Frame(parent, borderwidth=2, relief="groove")
    frame2 = tk.Frame(parent, borderwidth=2, relief="groove")
    frame.pack(side="left", fill="both")
    frame2.pack(side="left", fill="both")
    scrollbar = tk.Scrollbar(frame2)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    label_spec = tk.Text(
        frame2,
        width=20,
        yscrollcommand=scrollbar.set,
        font=("Times New Roman", 14, "bold"),
    )
    label_spec.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.config(command=label_spec.yview)
    add_history(True)
    label_spec.config(state="disabled")
    canvas = tk.Canvas(frame, width=SIZE * 8, height=SIZE * 8)
    canvas.pack(fill="both", expand=True, anchor="center")
    tk.Text()
    draw_grid()


def add_history(first=False):
    label_spec.config(state="normal")
    if first:
        label_spec.insert(
            tk.END, "\n".join(engine.format_history(engine.history)) + "\n"
        )
    else:
        label_spec.insert(tk.END, engine.format_history(engine.history)[-1] + "\n")
    label_spec.see(tk.END)
    label_spec.config(state="disabled")


def draw_grid():
    global canvas
    bottom_label = engine.X_NAME
    canvas.configure(width=SIZE * 8, height=SIZE * 8)
    for i in range(8):
        for y in range(8):
            if i % 2 == y % 2:
                canvas.create_rectangle(
                    SIZE * i,
                    SIZE * y,
                    SIZE + (SIZE * i),
                    SIZE + (SIZE * y),
                    fill=COLOR_THEME[COLOR_CHOICE]["white_board"],
                )
            else:
                canvas.create_rectangle(
                    SIZE * i,
                    SIZE * y,
                    SIZE + (SIZE * i),
                    SIZE + (SIZE * y),
                    fill=COLOR_THEME[COLOR_CHOICE]["black_board"],
                )
            if i == 0:
                canvas.create_text(
                    (SIZE * i) + SIZE * 0.1,
                    (SIZE * y) + SIZE * 0.1,
                    text=8 - (y),
                    font=("Times New Roman", 18, "bold"),
                )
            if y == 7:
                canvas.create_text(
                    (SIZE * i) + SIZE * 0.92,
                    (SIZE * y) + SIZE * 0.92,
                    text=bottom_label[i],
                    font=("Times New Roman", 18, "bold"),
                )


current_moove = []


def move_piece_GUI():
    global canvas
    canvas.bind("<Button-1>", get_clicked_cell1)


def get_clicked_cell1(event):
    global current_moove
    x = event.x // SIZE
    y = event.y // SIZE
    coords = engine.list_valid_move(current_board, (y, x))
    if current_board[y][x][1] == COLOR[(GAME_TURN % 2)] and len(current_moove) == 0:
        draw_help_circles(coords, canvas)
        current_moove.append((y, x))
    elif len(current_moove) == 1 and current_board[y][x][1] == COLOR[(GAME_TURN % 2)]:
        draw_board()
        draw_help_circles(coords, canvas)
        current_moove = [(y, x)]
    else:
        current_moove.append((y, x))
    if len(current_moove) == 2:
        show_move(
            current_moove[0][0],
            current_moove[0][1],
            current_moove[1][0],
            current_moove[1][1],
            COLOR[GAME_TURN % 2],
        )
        current_moove = []
    check_white = engine.get_checking_pieces(
        current_board, engine.find_king(current_board, "white")
    )
    # TODO:séparer
    for cell in check_white:
        draw_warn_circles(cell, canvas)

    check_black = engine.get_checking_pieces(
        current_board, engine.find_king(current_board, "black")
    )
    for cell in check_black:
        draw_warn_circles(cell, canvas)


def draw_board():
    draw_grid()
    for i, line in enumerate(current_board):
        for j, piece in enumerate(line):
            draw_piece(piece, j, i)


def draw_piece(piece, x, y):
    global DRAW_SETTINGS
    if piece[0] != "0":
        DRAW_SETTINGS = {
            "outline": COLOR_THEME[COLOR_CHOICE][piece[1]]["fill"],
            "fill": COLOR_THEME[COLOR_CHOICE][piece[1]]["fill"],
        }
        LINE_SETTINGS.update({"fill": COLOR_THEME[COLOR_CHOICE][piece[1]]["line"]})
    if piece[0] == "bishop":
        draw_bishop(x, y, DRAW_SETTINGS, canvas)
    if piece[0] == "rook":
        draw_rook(x, y, DRAW_SETTINGS, canvas)
    if piece[0] == "pawnb":
        draw_pawn(x, y, DRAW_SETTINGS, canvas)
    if piece[0] == "pawnw":
        draw_pawn(x, y, DRAW_SETTINGS, canvas)
    if piece[0] == "knight":
        draw_knight(x, y, DRAW_SETTINGS, canvas)
    if piece[0] == "queen":
        draw_queen(x, y, DRAW_SETTINGS, canvas)
    if piece[0] == "king":
        draw_king(x, y, DRAW_SETTINGS, canvas)


def show_move(y, x, newy, newx, col):
    global GAME_TURN, past_board
    if engine.move_piece(current_board, (y, x), (newy, newx), col) is not None:
        engine.move_piece(current_board, (y, x), (newy, newx), col)
        if engine.is_draw_repetitions(current_board, past_board):
            messagebox.showinfo(title="oui", message="égalité par répétitions")
        else:
            past_board.append(deepcopy(current_board))
        if engine.is_checkmat(
            current_board, engine.find_king(current_board, COLOR[((GAME_TURN + 1) % 2)])
        ):
            messagebox.showinfo(f"Félicitations ! {col} a gagné")
            with open("board.json", "r") as f:
                boards = json.load(f)
            boards["current"] = []
            with open("board.json", "w") as f:
                json.dump(boards, f, indent=4)

        GAME_TURN += 1
        update_turn_lab()
        add_history()
    draw_board()


if __name__ == "__main__":
    pass
