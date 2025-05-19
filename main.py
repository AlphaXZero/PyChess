import colorama as c
import engine
import GUI


def move_knight():
    GUI.show_move(0, 1, 2, 2)


if __name__ == "__main__":
    GUI.build_app(move_knight).mainloop()
