import ttkbootstrap as tk
import engine

COLOR_THEME = {"white": "seashell3", "black": "black"}

board = engine.board


def build_app(start_game=None) -> tk.Window:
    root = tk.Window(title="PyChess", themename="pulse", minsize=(600, 600))
    build_top_frame(root, start_game)
    build_checkerboard(root)
    root.position_center()
    draw_board()
    move_piece_GUI()
    return root


def build_top_frame(parent, start_game):
    frame = tk.Frame(parent, borderwidth=2, relief="groove")
    frame.pack(side="top", fill="x", expand=False)
    label = tk.Button(frame, text="Jouer", style="sucess", command=start_game)
    label.pack(pady=2)


def build_checkerboard(parent):
    global canvas
    frame = tk.Frame(parent, borderwidth=2, relief="groove")
    frame.pack(side="top", fill="both")
    canvas = tk.Canvas(frame, width=500, height=500)
    canvas.pack(fill="none", expand=True, anchor="center", pady=10)
    draw_grid()


def draw_grid():
    global canvas
    canvas.configure(width=402, height=402)
    for i in range(8):
        for y in range(8):
            if i % 2 == y % 2:
                canvas.create_rectangle(
                    50 * i, 50 * y, 50 + (50 * i), 50 + (50 * y), fill="lightgoldenrod1"
                )
            else:
                canvas.create_rectangle(
                    50 * i, 50 * y, 50 + (50 * i), 50 + (50 * y), fill="darkorange4"
                )


current_moove = []


def move_piece_GUI():
    global canvas

    canvas.bind("<Button-1>", get_clicked_cell1)


def get_clicked_cell1(event):
    """
    get clicked cell

    :param word: word to decode
    :type word: str

    :return decoded: word
    :rtype: str
    """
    global current_moove
    x = event.x // 50
    y = event.y // 50

    coords = engine.list_valid_move(board, (y, x))
    draw_help_circles(coords)
    current_moove.append((y, x))
    if len(current_moove) == 2:
        show_move(
            current_moove[0][0],
            current_moove[0][1],
            current_moove[1][0],
            current_moove[1][1],
        )
        current_moove = []
    check_white = engine.check_check(board, engine.find_king(board, "white"))
    print(check_white)
    # TODO:séparer
    for i in check_white:
        draw_warn_circles(i)

    check_black = engine.check_check(board, engine.find_king(board, "black"))
    print(check_black)
    # TODO:séparer + pion bug pour roi blanc
    for i in check_black:
        draw_warn_circles(i)


def draw_warn_circles(cell):
    global canvas

    canvas.create_oval(
        (cell[1] * 50) + 3,
        (cell[0] * 50) + 3,
        (cell[1] * 50) + 47,
        (cell[0] * 50) + 47,
        outline="orange",
        width=4,
    )


def draw_help_circles(coords):
    global canvas
    for cell in coords:
        canvas.create_oval(
            (cell[1] * 50) + 20,
            (cell[0] * 50) + 20,
            (cell[1] * 50) + 30,
            (cell[0] * 50) + 30,
            outline="blue",
            width=4,
        )


def draw_knight(x, y, color):
    global canvas
    x, y = x * 50, y * 50
    # rectangle nez
    canvas.create_rectangle(x + 10, y + 20, x + 45, y + 30, outline=color, fill=color)
    # triangle nez
    canvas.create_polygon(
        x + 10, y + 20, x + 34, y + 20, x + 35, y + 10, outline=color, fill=color
    )
    # rectangle corps
    canvas.create_rectangle(x + 30, y + 10, x + 45, y + 45, outline=color, fill=color)
    # base
    canvas.create_rectangle(x + 20, y + 40, x + 45, y + 45, outline=color, fill=color)
    # triangle pied
    canvas.create_polygon(
        x + 20, y + 40, x + 35, y + 30, x + 35, y + 40, outline=color, fill=color
    )
    # rectanle oreille
    canvas.create_rectangle(x + 30, y + 5, x + 40, y + 10, outline=color, fill=color)
    # cercle oeil
    # TODO CHANEGER couleur
    canvas.create_oval(
        x + 30,
        y + 15,
        x + 35,
        y + 20,
        outline=color,
        fill="white" if color == "black" else "black",
    )


def draw_rook(x, y, color):
    global canvas
    x, y = x * 50, y * 50
    # base
    canvas.create_rectangle(x + 10, y + 35, x + 40, y + 45, outline=color, fill=color)
    # rectanngle corps
    canvas.create_rectangle(x + 15, y + 20, x + 35, y + 40, outline=color, fill=color)
    # rectangle sommet
    canvas.create_rectangle(x + 12, y + 10, x + 38, y + 20, outline=color, fill=color)
    # petit rectangles sommets
    canvas.create_rectangle(x + 12, y + 5, x + 17, y + 10, outline=color, fill=color)
    canvas.create_rectangle(x + 22, y + 5, x + 27, y + 10, outline=color, fill=color)
    canvas.create_rectangle(x + 33, y + 5, x + 38, y + 10, outline=color, fill=color)


def draw_pawn(x, y, color):
    global canvas
    x, y = x * 50, y * 50
    # base
    canvas.create_rectangle(x + 10, y + 35, x + 40, y + 45, outline=color, fill=color)
    # trapeze corps
    canvas.create_polygon(
        x + 15,
        y + 35,
        x + 20,
        y + 25,
        x + 30,
        y + 25,
        x + 35,
        y + 35,
        outline=color,
        fill=color,
    )
    # rectangle sommet
    canvas.create_rectangle(x + 17, y + 15, x + 33, y + 25, outline=color, fill=color)
    # rond sommmet
    canvas.create_oval(x + 20, y + 5, x + 30, y + 15, outline=color, fill=color)


def draw_bihsop(x, y, color):
    global canvas
    x, y = x * 50, y * 50
    # base
    canvas.create_rectangle(x + 10, y + 35, x + 40, y + 45, outline=color, fill=color)
    # ovale corps
    canvas.create_oval(x + 20, y + 10, x + 30, y + 40, outline=color, fill=color)
    # rond sommmet
    canvas.create_oval(x + 23, y + 5, x + 27, y + 10, outline=color, fill=color)


def draw_queen(x, y, color):
    global canvas
    x, y = x * 50, y * 50
    # base
    canvas.create_rectangle(x + 5, y + 40, x + 45, y + 45, outline=color, fill=color)
    # grand triangle
    canvas.create_polygon(
        x + 10, y + 40, x + 40, y + 40, x + 25, y + 20, outline=color, fill=color
    )
    # petit triangle
    canvas.create_polygon(
        x + 25, y + 22, x + 15, y + 10, x + 35, y + 10, outline=color, fill=color
    )
    # rond sommet
    canvas.create_oval(x + 23, y + 5, x + 27, y + 10, outline=color, fill=color)


def draw_king(x, y, color):
    global canvas
    x, y = x * 50, y * 50
    # base
    canvas.create_rectangle(x + 5, y + 40, x + 45, y + 45, outline=color, fill=color)
    # traèze
    canvas.create_polygon(
        x + 10,
        y + 40,
        x + 40,
        y + 40,
        x + 35,
        y + 25,
        x + 15,
        y + 25,
        outline=color,
        fill=color,
    )
    # sommet vertical
    canvas.create_rectangle(x + 23, y + 25, x + 27, y + 5, outline=color, fill=color)
    # sommet horizontal
    canvas.create_rectangle(x + 14, y + 12, x + 36, y + 14, outline=color, fill=color)


def draw_board():
    for i, line in enumerate(board):
        for j, piece in enumerate(line):
            draw_piece(piece, j, i)


def draw_piece(piece, x, y):
    if piece[0] == "bihsop":
        draw_bihsop(x, y, COLOR_THEME[piece[1]])
    if piece[0] == "rook":
        draw_rook(x, y, COLOR_THEME[piece[1]])
    if piece[0] == "pawnb":
        draw_pawn(x, y, COLOR_THEME[piece[1]])
    if piece[0] == "pawnw":
        draw_pawn(x, y, COLOR_THEME[piece[1]])
    if piece[0] == "knight":
        draw_knight(x, y, COLOR_THEME[piece[1]])
    if piece[0] == "queen":
        draw_queen(x, y, COLOR_THEME[piece[1]])
    if piece[0] == "king":
        draw_king(x, y, COLOR_THEME[piece[1]])


def show_move(y, x, newy, newx):
    engine.move_piece(board, y, x, newy, newx)
    draw_grid()
    draw_board()


if __name__ == "__main__":
    build_app().mainloop()
