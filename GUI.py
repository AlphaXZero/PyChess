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
                    50 * i, 50 * y, 50 + (50 * i), 50 + (50 * y), fill="white"
                )
            else:
                canvas.create_rectangle(
                    50 * i, 50 * y, 50 + (50 * i), 50 + (50 * y), fill="grey"
                )


if __name__ == "__main__":
    build_app().mainloop()
