import ttkbootstrap as tk
import engine
from tkinter import messagebox

COLOR_CHOICE = "Classic"
# Themes made by @cindy.vanderveen
COLOR_THEME = {
    "Classic": {
        "white": {"fill": "#f2f2f2", "line": "black"},
        "black": {"fill": "#464646", "line": "black"},
        "black_board": "#777777",
        "white_board": "#ffffff",
    },
    "High On Drugs": {
        "white": {"fill": "#00ff38", "line": "#00f9ff"},
        "black": {"fill": "#3c00ff", "line": "#00f9ff"},
        "black_board": "#fd00ff",
        "white_board": "#fdff00",
    },
    "Halloween": {
        "white": {"fill": "#00ba91", "line": "#00ba91"},
        "black": {"fill": "#863174", "line": "#863174"},
        "black_board": "black",
        "white_board": "#e26b0f",
    },
    "Holy Blood": {
        "black": {"fill": "red4", "line": "red4"},
        "white": {"fill": "indian red", "line": "brown4"},
        "black_board": "red",
        "white_board": "tomato",
    },
    "Neon": {
        "white": {"fill": "cyan", "line": "white"},
        "black": {"fill": "deep pink", "line": "white"},
        "white_board": "CadetBlue1",
        "black_board": "magenta2",
    },
    "Wood": {
        "white": {"fill": "ivory2", "line": "black"},
        "black": {"fill": "black", "line": "black"},
        "white_board": "NavajoWhite2",
        "black_board": "saddle brown",
    },
    "Chess.com": {
        "white": {"fill": "#ffffff", "line": "#4b4847"},
        "black": {"fill": "#4b4847", "line": "#4b4847"},
        "white_board": "#eeeed2",
        "black_board": "#69923e",
    },
    "Star Wars": {
        "white": {"fill": "RoyalBlue1", "line": "RoyalBlue1"},
        "black": {"fill": "red3", "line": "red3"},
        "white_board": "navy",
        "black_board": "black",
    },
    "Royal": {
        "white": {"fill": "gold", "line": "dark green"},
        "black": {"fill": "purple4", "line": "red4"},
        "white_board": "red4",
        "black_board": "blue4",
    },
    "Noel": {
        "white": {"fill": "#f4f0bb", "line": "#f4f0bb"},
        "black": {"fill": "#43291f", "line": "#43291f"},
        "white_board": "#87c38f",
        "black_board": "#da2c38",
    },
    "Dusk": {
        "black": {"fill": "#7C4585", "line": "#7C4585"},
        "white": {"fill": "#F8B55F", "line": "#F8B55F"},
        "white_board": "#C95792",
        "black_board": "#3D365C",
    },
    "Army": {
        "white": {"fill": "#25591f", "line": "#25591f"},
        "black": {"fill": "#593a0e", "line": "#593a0e"},
        "white_board": "#72601b",
        "black_board": "#19270d",
    },
}

LINE_SETTINGS = {"width": 3}
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

    label = tk.Label(frame, text="Game Turn : ", font=("Arial", 14))
    label.pack(side="left", pady=4)
    turn_text = tk.Label(frame, textvariable=text_top, font=("Arial", 14))
    turn_text.pack(side="left", padx=4)

    theme_label = tk.Label(frame, text="Theme :", font=("Arial", 14))

    theme_combobox = tk.Combobox(
        frame,
        values=list(COLOR_THEME.keys()),
        width=15,
        state="readonly",
    )
    theme_combobox.pack(side="right", padx=4, pady=4)
    theme_label.pack(side="right", padx=10)
    theme_combobox.set(COLOR_CHOICE)

    def change_theme(event):
        global COLOR_CHOICE
        COLOR_CHOICE = theme_combobox.get()
        draw_grid()
        draw_board()

    theme_combobox.bind("<<ComboboxSelected>>", change_theme)

    update_turn_lab()


def update_turn_lab():
    global text_top
    text_top.set(f"{color[(GAME_TURN % 2)]}")


def build_checkerboard(parent):
    global canvas, history_content
    frame = tk.Frame(parent, borderwidth=2, relief="groove")
    frame2 = tk.Frame(parent, borderwidth=2, relief="groove")
    frame.pack(side="left", fill="both")
    frame2.pack(side="left", fill="both")

    history_content = tk.StringVar()
    label = tk.Label(frame2, text="oekzaeizauen", width=20)
    label["textvariable"] = history_content
    label.pack()
    canvas = tk.Canvas(frame, width=SIZE * 8, height=SIZE * 8)
    canvas.pack(fill="both", expand=True, anchor="center")
    tk.Text()
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
                    fill=COLOR_THEME[COLOR_CHOICE]["white_board"],
                )
            else:
                # noir
                canvas.create_rectangle(
                    SIZE * i,
                    SIZE * y,
                    SIZE + (SIZE * i),
                    SIZE + (SIZE * y),
                    fill=COLOR_THEME[COLOR_CHOICE]["black_board"],
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


def draw_knight(x, y, settings):
    global canvas
    x, y = x * SIZE, y * SIZE
    # rectangle nez
    canvas.create_rectangle(
        x + gp(20),
        y + gp(40),
        x + gp(90),
        y + gp(60),
        **settings,
    )
    # triangle nez
    canvas.create_polygon(
        x + gp(20),
        y + gp(40),
        x + gp(68),
        y + gp(40),
        x + gp(70),
        y + gp(20),
        **settings,
    )
    # rectangle corps
    canvas.create_rectangle(
        x + gp(60),
        y + gp(20),
        x + gp(90),
        y + gp(90),
        **settings,
    )
    # base
    canvas.create_rectangle(
        x + gp(40),
        y + gp(80),
        x + gp(90),
        y + gp(90),
        **settings,
    )
    # triangle pied
    canvas.create_polygon(
        x + gp(40),
        y + gp(80),
        x + gp(70),
        y + gp(60),
        x + gp(70),
        y + gp(80),
        **settings,
    )
    # rectanle oreille
    canvas.create_rectangle(
        x + gp(60),
        y + gp(10),
        x + gp(80),
        y + gp(20),
        **settings,
    )
    # rectangle oreille
    canvas.create_line(x + gp(60), y + gp(10), x + gp(60), y + gp(24), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(10), x + gp(80), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(60), y + gp(10), x + gp(80), y + gp(10), **LINE_SETTINGS)
    # ligne droite oreille
    canvas.create_line(x + gp(80), y + gp(20), x + gp(90), y + gp(20), **LINE_SETTINGS)
    # corps ligne vertical
    canvas.create_line(x + gp(90), y + gp(20), x + gp(90), y + gp(90), **LINE_SETTINGS)
    # pied
    canvas.create_line(x + gp(40), y + gp(90), x + gp(90), y + gp(90), **LINE_SETTINGS)
    # pied gauche
    canvas.create_line(x + gp(40), y + gp(80), x + gp(40), y + gp(90), **LINE_SETTINGS)
    # hyppotenuse pied
    canvas.create_line(x + gp(40), y + gp(80), x + gp(60), y + gp(65), **LINE_SETTINGS)
    # mileu gauche
    canvas.create_line(x + gp(60), y + gp(66), x + gp(60), y + gp(62), **LINE_SETTINGS)
    # mileu horizontal
    canvas.create_line(x + gp(20), y + gp(62), x + gp(60), y + gp(62), **LINE_SETTINGS)
    # nez vertical
    canvas.create_line(x + gp(20), y + gp(62), x + gp(20), y + gp(40), **LINE_SETTINGS)
    # nez hyppotenuse
    canvas.create_line(x + gp(20), y + gp(40), x + gp(60), y + gp(23), **LINE_SETTINGS)

    # cercle oeil
    settings["fill"] = "black"
    canvas.create_oval(x + gp(60), y + gp(30), x + gp(70), y + gp(40), **settings)


def draw_rook(x, y, settings):
    global canvas
    x, y = x * SIZE, y * SIZE

    # rectanngle corps
    canvas.create_rectangle(
        x + gp(30),
        y + gp(40),
        x + gp(70),
        y + gp(80),
        **settings,
    )
    # rectangle sommet
    canvas.create_rectangle(
        x + gp(24),
        y + gp(20),
        x + gp(76),
        y + gp(40),
        **settings,
    )
    # petit rectangles sommets
    canvas.create_rectangle(
        x + gp(24),
        y + gp(10),
        x + gp(34),
        y + gp(20),
        **settings,
    )
    canvas.create_rectangle(
        x + gp(44),
        y + gp(10),
        x + gp(56),
        y + gp(20),
        **settings,
    )
    canvas.create_rectangle(
        x + gp(66),
        y + gp(10),
        x + gp(76),
        y + gp(20),
        **settings,
    )
    # base
    settings.update({"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS["fill"]})
    canvas.create_rectangle(
        x + gp(20),
        y + gp(70),
        x + gp(80),
        y + gp(90),
        **settings,
    )
    # petites lignes base
    canvas.create_line(x + gp(20), y + gp(70), x + gp(30), y + gp(70), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(70), x + gp(70), y + gp(70), **LINE_SETTINGS)
    # corps
    canvas.create_line(x + gp(30), y + gp(70), x + gp(30), y + gp(40), **LINE_SETTINGS)
    canvas.create_line(x + gp(70), y + gp(70), x + gp(70), y + gp(40), **LINE_SETTINGS)
    # petutes lignes bas ehaut
    canvas.create_line(x + gp(24), y + gp(40), x + gp(76), y + gp(40), **LINE_SETTINGS)
    canvas.create_line(x + gp(76), y + gp(40), x + gp(70), y + gp(40), **LINE_SETTINGS)
    # haut cotés
    canvas.create_line(x + gp(24), y + gp(40), x + gp(24), y + gp(10), **LINE_SETTINGS)
    canvas.create_line(x + gp(76), y + gp(40), x + gp(76), y + gp(10), **LINE_SETTINGS)
    # petites lignes sommet
    canvas.create_line(x + gp(24), y + gp(10), x + gp(34), y + gp(10), **LINE_SETTINGS)
    canvas.create_line(x + gp(44), y + gp(10), x + gp(56), y + gp(10), **LINE_SETTINGS)
    canvas.create_line(x + gp(66), y + gp(10), x + gp(76), y + gp(10), **LINE_SETTINGS)
    # petites lignes sommet bas
    canvas.create_line(x + gp(34), y + gp(20), x + gp(44), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(66), y + gp(20), x + gp(56), y + gp(20), **LINE_SETTINGS)
    # peties lignes verticales
    canvas.create_line(x + gp(24), y + gp(10), x + gp(24), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(34), y + gp(10), x + gp(34), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(44), y + gp(10), x + gp(44), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(56), y + gp(10), x + gp(56), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(66), y + gp(10), x + gp(66), y + gp(20), **LINE_SETTINGS)


def draw_pawn(x, y, settings):
    global canvas
    x, y = x * SIZE, y * SIZE
    # base
    canvas.create_rectangle(
        x + gp(20),
        y + gp(70),
        x + gp(80),
        y + gp(90),
        **settings,
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
        **settings,
    )
    # rectangle sommet
    settings.update({"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS["fill"]})
    canvas.create_rectangle(x + gp(34), y + gp(30), x + gp(66), y + gp(50), **settings)
    # rond sommmet

    canvas.create_oval(x + gp(40), y + gp(10), x + gp(60), y + gp(30), **settings)
    # base
    canvas.create_line(x + gp(20), y + gp(90), x + gp(80), y + gp(90), **LINE_SETTINGS)
    canvas.create_line(x + gp(20), y + gp(90), x + gp(20), y + gp(70), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(90), x + gp(80), y + gp(70), **LINE_SETTINGS)
    # base haut
    canvas.create_line(x + gp(80), y + gp(70), x + gp(70), y + gp(70), **LINE_SETTINGS)
    canvas.create_line(x + gp(20), y + gp(70), x + gp(30), y + gp(70), **LINE_SETTINGS)
    # triangle coté
    canvas.create_line(x + gp(30), y + gp(70), x + gp(40), y + gp(50), **LINE_SETTINGS)
    canvas.create_line(x + gp(70), y + gp(70), x + gp(60), y + gp(50), **LINE_SETTINGS)


def draw_bishop(x, y, settings):
    global canvas
    x, y = x * SIZE, y * SIZE
    settings.update({"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS["fill"]})

    # ovale corps
    canvas.create_oval(
        x + gp(35),
        y + gp(20),
        x + gp(65),
        y + gp(80),
        **settings,
    )
    # rond sommmet
    canvas.create_oval(
        x + gp(46),
        y + gp(10),
        x + gp(54),
        y + gp(20),
        **settings,
    )
    # base
    canvas.create_rectangle(
        x + gp(25),
        y + gp(75),
        x + gp(75),
        y + gp(90),
        **settings,
    )


def draw_queen(x, y, settings):
    global canvas
    x, y = x * SIZE, y * SIZE
    # base
    canvas.create_rectangle(
        x + gp(10),
        y + gp(80),
        x + gp(90),
        y + gp(90),
        **settings,
    )
    # grand triangle
    canvas.create_polygon(
        x + gp(20),
        y + gp(80),
        x + gp(80),
        y + gp(80),
        x + gp(50),
        y + gp(40),
        **settings,
    )
    settings.update({"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS["fill"]})
    # petit triangle
    canvas.create_polygon(
        x + gp(50),
        y + gp(44),
        x + gp(30),
        y + gp(20),
        x + gp(70),
        y + gp(20),
        **settings,
    )
    # rond sommet

    canvas.create_oval(
        x + gp(46),
        y + gp(10),
        x + gp(54),
        y + gp(20),
        **settings,
    )
    # base
    canvas.create_line(x + gp(10), y + gp(90), x + gp(90), y + gp(90), **LINE_SETTINGS)
    canvas.create_line(x + gp(10), y + gp(90), x + gp(10), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(90), y + gp(90), x + gp(90), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(10), y + gp(80), x + gp(20), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(90), y + gp(80), x + gp(80), y + gp(80), **LINE_SETTINGS)
    # trianle bas
    canvas.create_line(x + gp(20), y + gp(80), x + gp(50), y + gp(44), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(80), x + gp(50), y + gp(44), **LINE_SETTINGS)


def draw_king(x, y, settings):
    global canvas
    x, y = x * SIZE, y * SIZE
    # base
    canvas.create_rectangle(
        x + gp(10),
        y + gp(80),
        x + gp(90),
        y + gp(90),
        **settings,
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
        **settings,
    )
    # sommet vertical
    settings.update({"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS["fill"]})
    canvas.create_rectangle(
        x + gp(46),
        y + gp(50),
        x + gp(54),
        y + gp(10),
        **settings,
    )
    # sommet horizontal

    canvas.create_rectangle(
        x + gp(28),
        y + gp(24),
        x + gp(72),
        y + gp(28),
        **settings,
    )
    # base
    canvas.create_line(x + gp(10), y + gp(90), x + gp(90), y + gp(90), **LINE_SETTINGS)
    canvas.create_line(x + gp(10), y + gp(90), x + gp(10), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(90), y + gp(90), x + gp(90), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(10), y + gp(80), x + gp(20), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(90), y + gp(80), x + gp(80), y + gp(80), **LINE_SETTINGS)
    # trapèze
    canvas.create_line(x + gp(20), y + gp(80), x + gp(30), y + gp(50), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(80), x + gp(70), y + gp(50), **LINE_SETTINGS)
    canvas.create_line(x + gp(30), y + gp(50), x + gp(70), y + gp(50), **LINE_SETTINGS)


def draw_board():
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
        draw_bishop(x, y, DRAW_SETTINGS)
    if piece[0] == "rook":
        draw_rook(x, y, DRAW_SETTINGS)
    if piece[0] == "pawnb":
        draw_pawn(x, y, DRAW_SETTINGS)
    if piece[0] == "pawnw":
        draw_pawn(x, y, DRAW_SETTINGS)
    if piece[0] == "knight":
        draw_knight(x, y, DRAW_SETTINGS)
    if piece[0] == "queen":
        draw_queen(x, y, DRAW_SETTINGS)
    if piece[0] == "king":
        draw_king(x, y, DRAW_SETTINGS)


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
        history_content.set(
            history_content.get() + "\n" + engine.format_history(engine.HISTORY)[-1]
        )
    draw_grid()
    draw_board()


if __name__ == "__main__":
    build_app().mainloop()
