import ttkbootstrap as tk
import engine
from tkinter import messagebox

COLOR_THEME = {
    "white": "white",
    "black": "gray14",
    "black_board": "DarkOliveGreen3",
    "white_board": "Antique white",
}

current_board = engine.board

color = ["white", "black"]
GAME_TURN = 0
text_top = None
SIZE = 110


def gp(percent: int):
    return SIZE * (percent / 100)


def build_app() -> tk.Window:
    global text_top, root
    root = tk.Window(
        title="PyChess", themename="superhero", minsize=(SIZE * 8, SIZE * 8)
    )
    text_top = tk.StringVar()
    build_top_frame(root)
    build_checkerboard(root)
    root.position_center()
    draw_board()
    move_piece_GUI()
    return root


def restart():
    global current_board
    current_board = engine.board
    draw_grid()
    draw_board()


def build_top_frame(parent):
    global text_top
    frame = tk.Frame(parent, borderwidth=2, relief="groove")
    frame.pack(side="top", fill="x", expand=False)
    button = tk.Button(frame, text="Nouvelle Partie", style="sucess", command=restart)

    label = tk.Label(frame, text="Game Turn : ", font=("Arial", 14))
    label.pack(side="left", pady=4)
    turn_text = tk.Label(frame, textvariable=text_top, font=("Arial", 14))
    turn_text.pack(side="left", padx=4)
    button.pack()
    update_turn_lab()


def update_turn_lab():
    global text_top
    text_top.set(f"{color[(GAME_TURN % 2)]}")


def build_checkerboard(parent):
    global canvas
    frame = tk.Frame(parent, borderwidth=2, relief="groove")
    frame.pack(side="top", fill="both")
    canvas = tk.Canvas(frame, width=SIZE * 8, height=SIZE * 8)
    canvas.pack(fill="both", expand=True, anchor="center", pady=10)
    draw_grid()


def draw_grid():
    global canvas
    canvas.configure(width=SIZE * 8, height=SIZE * 8)
    for i in range(8):
        for y in range(8):
            if i % 2 == y % 2:
                # blanc
                canvas.create_rectangle(
                    SIZE * i,
                    SIZE * y,
                    SIZE + (SIZE * i),
                    SIZE + (SIZE * y),
                    fill=COLOR_THEME["white_board"],
                )
            else:
                # noir
                canvas.create_rectangle(
                    SIZE * i,
                    SIZE * y,
                    SIZE + (SIZE * i),
                    SIZE + (SIZE * y),
                    fill=COLOR_THEME["black_board"],
                )


current_moove = []


# TODO : ne pas ajouter cou si clique sur une puece à lui
def move_piece_GUI():
    global canvas

    canvas.bind("<Button-1>", get_clicked_cell1)


def get_clicked_cell1(event):
    """
        get clicked cell
    comment break
        :param word: word to decode
        :type word: str

        :return decoded: word
        :rtype: str
    """
    global current_moove
    x = event.x // SIZE
    y = event.y // SIZE

    coords = engine.list_valid_move(current_board, (y, x))
    # remonter la vrif ici
    if current_board[y][x][1] == color[(GAME_TURN % 2)]:
        draw_help_circles(coords)
    current_moove.append((y, x))
    if len(current_moove) == 2:
        show_move(
            current_moove[0][0],
            current_moove[0][1],
            current_moove[1][0],
            current_moove[1][1],
            color[GAME_TURN % 2],
        )
        current_moove = []
    check_white = engine.is_check(
        current_board, engine.find_king(current_board, "white")
    )
    # TODO:séparer
    for i in check_white:
        draw_warn_circles(i)

    check_black = engine.is_check(
        current_board, engine.find_king(current_board, "black")
    )
    # TODO:séparer + pion bug pour roi blanc
    for i in check_black:
        draw_warn_circles(i)


def draw_warn_circles(cell):
    global canvas

    canvas.create_oval(
        (cell[1] * SIZE) + gp(6),
        (cell[0] * SIZE) + gp(6),
        (cell[1] * SIZE) + gp(94),
        (cell[0] * SIZE) + gp(94),
        outline="orange",
        width=4,
    )


def draw_help_circles(coords):
    global canvas
    for cell in coords:
        canvas.create_oval(
            (cell[1] * SIZE) + gp(40),
            (cell[0] * SIZE) + gp(40),
            (cell[1] * SIZE) + gp(60),
            (cell[0] * SIZE) + gp(60),
            outline="blue",
            width=4,
        )


def draw_knight(x, y, color):
    global canvas
    x, y = x * SIZE, y * SIZE
    # rectangle nez
    canvas.create_rectangle(
        x + gp(20),
        y + gp(40),
        x + gp(90),
        y + gp(60),
        outline=color,
        fill=color,
    )
    # triangle nez
    canvas.create_polygon(
        x + gp(20),
        y + gp(40),
        x + gp(68),
        y + gp(40),
        x + gp(70),
        y + gp(20),
        outline=color,
        fill=color,
    )
    # rectangle corps
    canvas.create_rectangle(
        x + gp(60),
        y + gp(20),
        x + gp(90),
        y + gp(90),
        outline=color,
        fill=color,
    )
    # base
    canvas.create_rectangle(
        x + gp(40),
        y + gp(80),
        x + gp(90),
        y + gp(90),
        outline=color,
        fill=color,
    )
    # triangle pied
    canvas.create_polygon(
        x + gp(40),
        y + gp(80),
        x + gp(70),
        y + gp(60),
        x + gp(70),
        y + gp(80),
        outline=color,
        fill=color,
    )
    # rectanle oreille
    canvas.create_rectangle(
        x + gp(60),
        y + gp(10),
        x + gp(80),
        y + gp(20),
        outline=color,
        fill=color,
    )
    # cercle oeil
    # TODO CHANEGER couleur
    canvas.create_oval(
        x + gp(60),
        y + gp(30),
        x + gp(70),
        y + gp(40),
        outline=color,
        fill="white" if color == "black" else "black",
    )


def draw_rook(x, y, color):
    global canvas
    x, y = x * SIZE, y * SIZE
    # base
    canvas.create_rectangle(
        x + gp(20),
        y + gp(70),
        x + gp(80),
        y + gp(90),
        outline=color,
        fill=color,
    )
    # rectanngle corps
    canvas.create_rectangle(
        x + gp(30),
        y + gp(40),
        x + gp(70),
        y + gp(80),
        outline=color,
        fill=color,
    )
    # rectangle sommet
    canvas.create_rectangle(
        x + gp(24),
        y + gp(20),
        x + gp(76),
        y + gp(40),
        outline=color,
        fill=color,
    )
    # petit rectangles sommets
    canvas.create_rectangle(
        x + gp(24),
        y + gp(10),
        x + gp(34),
        y + gp(20),
        outline=color,
        fill=color,
    )
    canvas.create_rectangle(
        x + gp(44),
        y + gp(10),
        x + gp(56),
        y + gp(20),
        outline=color,
        fill=color,
    )
    canvas.create_rectangle(
        x + gp(66),
        y + gp(10),
        x + gp(76),
        y + gp(20),
        outline=color,
        fill=color,
    )
    # base
    canvas.create_line(x + gp(20), y + gp(70), x + gp(20), y + gp(90), width=2)
    canvas.create_line(x + gp(20), y + gp(90), x + gp(80), y + gp(90), width=2)
    canvas.create_line(x + gp(80), y + gp(70), x + gp(80), y + gp(90), width=2)
    # petites lignes base
    canvas.create_line(x + gp(20), y + gp(70), x + gp(30), y + gp(70), width=2)
    canvas.create_line(x + gp(80), y + gp(70), x + gp(70), y + gp(70), width=2)
    # corps
    canvas.create_line(x + gp(30), y + gp(70), x + gp(30), y + gp(40), width=2)
    canvas.create_line(x + gp(70), y + gp(70), x + gp(70), y + gp(40), width=2)
    # petutes lignes bas ehaut
    canvas.create_line(x + gp(24), y + gp(40), x + gp(30), y + gp(40), width=2)
    canvas.create_line(x + gp(76), y + gp(40), x + gp(70), y + gp(40), width=2)
    # haut cotés
    canvas.create_line(x + gp(24), y + gp(40), x + gp(24), y + gp(10), width=2)
    canvas.create_line(x + gp(76), y + gp(40), x + gp(76), y + gp(10), width=2)
    # petites lignes sommet
    canvas.create_line(x + gp(24), y + gp(10), x + gp(34), y + gp(10), width=2)
    canvas.create_line(x + gp(44), y + gp(10), x + gp(56), y + gp(10), width=2)
    canvas.create_line(x + gp(66), y + gp(10), x + gp(76), y + gp(10), width=2)
    # petites lignes sommet bas
    canvas.create_line(x + gp(34), y + gp(20), x + gp(44), y + gp(20), width=2)
    canvas.create_line(x + gp(66), y + gp(20), x + gp(56), y + gp(20), width=2)
    # peties lignes verticales
    canvas.create_line(x + gp(24), y + gp(10), x + gp(24), y + gp(20), width=2)
    canvas.create_line(x + gp(34), y + gp(10), x + gp(34), y + gp(20), width=2)
    canvas.create_line(x + gp(44), y + gp(10), x + gp(44), y + gp(20), width=2)
    canvas.create_line(x + gp(56), y + gp(10), x + gp(56), y + gp(20), width=2)
    canvas.create_line(x + gp(66), y + gp(10), x + gp(66), y + gp(20), width=2)


def draw_pawn(x, y, color):
    global canvas
    x, y = x * SIZE, y * SIZE
    # base
    canvas.create_rectangle(
        x + gp(20),
        y + gp(70),
        x + gp(80),
        y + gp(90),
        outline=color,
        fill=color,
    )
    # trapeze corps
    canvas.create_polygon(
        x + gp(30),
        y + gp(70),
        x + gp(40),
        y + gp(50),
        x + gp(60),
        y + gp(50),
        x + gp(70),
        y + gp(70),
        outline=color,
        fill=color,
    )
    # rectangle sommet
    canvas.create_rectangle(
        x + gp(34),
        y + gp(30),
        x + gp(66),
        y + gp(50),
        outline=color,
        fill=color,
    )
    # rond sommmet
    canvas.create_oval(
        x + gp(40),
        y + gp(10),
        x + gp(60),
        y + gp(30),
        outline=color,
        fill=color,
    )


def draw_bishop(x, y, color):
    global canvas
    x, y = x * SIZE, y * SIZE
    # base
    canvas.create_rectangle(
        x + gp(20),
        y + gp(70),
        x + gp(80),
        y + gp(90),
        outline=color,
        fill=color,
    )
    # ovale corps
    canvas.create_oval(
        x + gp(40),
        y + gp(20),
        x + gp(60),
        y + gp(80),
        outline=color,
        fill=color,
    )
    # rond sommmet
    canvas.create_oval(
        x + gp(46),
        y + gp(10),
        x + gp(54),
        y + gp(20),
        outline=color,
        fill=color,
    )


def draw_queen(x, y, color):
    global canvas
    x, y = x * SIZE, y * SIZE
    # base
    canvas.create_rectangle(
        x + gp(10),
        y + gp(80),
        x + gp(90),
        y + gp(90),
        outline=color,
        fill=color,
    )
    # grand triangle
    canvas.create_polygon(
        x + gp(20),
        y + gp(80),
        x + gp(80),
        y + gp(80),
        x + gp(50),
        y + gp(40),
        outline=color,
        fill=color,
    )
    # petit triangle
    canvas.create_polygon(
        x + gp(50),
        y + gp(44),
        x + gp(30),
        y + gp(20),
        x + gp(70),
        y + gp(20),
        outline=color,
        fill=color,
    )
    # rond sommet
    canvas.create_oval(
        x + gp(46),
        y + gp(10),
        x + gp(54),
        y + gp(20),
        outline=color,
        fill=color,
    )


def draw_king(x, y, color):
    global canvas
    x, y = x * SIZE, y * SIZE
    # base
    canvas.create_rectangle(
        x + gp(10),
        y + gp(80),
        x + gp(90),
        y + gp(90),
        outline=color,
        fill=color,
    )
    # traèze
    canvas.create_polygon(
        x + gp(20),
        y + gp(80),
        x + gp(80),
        y + gp(80),
        x + gp(70),
        y + gp(50),
        x + gp(30),
        y + gp(50),
        outline=color,
        fill=color,
    )
    # sommet vertical
    canvas.create_rectangle(
        x + gp(46),
        y + gp(50),
        x + gp(54),
        y + gp(10),
        outline=color,
        fill=color,
    )
    # sommet horizontal
    canvas.create_rectangle(
        x + gp(28),
        y + gp(24),
        x + gp(72),
        y + gp(28),
        outline=color,
        fill=color,
    )


def draw_board():
    for i, line in enumerate(current_board):
        for j, piece in enumerate(line):
            draw_piece(piece, j, i)


def draw_piece(piece, x, y):
    if piece[0] == "bishop":
        draw_bishop(x, y, COLOR_THEME[piece[1]])
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


def show_move(y, x, newy, newx, col):
    global GAME_TURN

    if engine.move_piece(current_board, (y, x), (newy, newx), col) is not None:
        engine.move_piece(current_board, (y, x), (newy, newx), col)
        if engine.is_check_mat(
            current_board, engine.find_king(current_board, color[((GAME_TURN + 1) % 2)])
        ):
            messagebox.showinfo("Félicitations !", f"{col} a gagné")
        GAME_TURN += 1
        update_turn_lab()
        print(engine.format_history(engine.HISTORY))
    draw_grid()
    draw_board()


if __name__ == "__main__":
    build_app().mainloop()
