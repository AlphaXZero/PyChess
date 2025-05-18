import colorama as c
import engine
import GUI

COLOR_THEME = {"white": "seashell3", "black": "black"}


# TODO où mettre ça ????
def init_game():
    for i, line in enumerate(engine.board):
        for j, piece in enumerate(line):
            if piece[0] == "bihsop":
                GUI.draw_bihsop(j, i, COLOR_THEME[piece[1]])
            if piece[0] == "rook":
                GUI.draw_rook(j, i, COLOR_THEME[piece[1]])
            if piece[0] == "pawnb":
                GUI.draw_pawn(j, i, COLOR_THEME[piece[1]])
            if piece[0] == "pawnw":
                GUI.draw_pawn(j, i, COLOR_THEME[piece[1]])
            if piece[0] == "knight":
                GUI.draw_knight(j, i, COLOR_THEME[piece[1]])
            if piece[0] == "queen":
                GUI.draw_queen(j, i, COLOR_THEME[piece[1]])


if __name__ == "__main__":
    GUI.build_app(init_game).mainloop()
