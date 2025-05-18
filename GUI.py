import ttkbootstrap as tk


def build_app() -> tk.Window:
    root = tk.Window(title="PyChess", themename="pulse", minsize=(600, 600))
    build_top_frame(root)
    build_checkerboard(root)
    # build_bottom_frame(root)
    root.position_center()
    return root


def build_top_frame(parent):
    frame = tk.Frame(parent, borderwidth=2, relief="groove")
    frame.pack(side="top", fill="x", expand=False)

    label = tk.Button(frame, text="Jouer", style="sucess")
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
    draw_rook(1, 1, "black")
    draw_pawn(1, 2, "black")
    draw_bihsop(1, 3, "black")
    draw_knight(1, 4, "black")
    draw_rook(2, 1, "snow")
    draw_pawn(2, 2, "snow")
    draw_bihsop(2, 3, "snow")
    draw_knight(2, 4, "snow")


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


if __name__ == "__main__":
    build_app().mainloop()
