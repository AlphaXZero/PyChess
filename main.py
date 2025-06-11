import json
import engine
import gui


def save_game_on_quit():
    gui.build_app().mainloop()
    try:
        with open("board.json", "r") as f:
            boards = json.load(f)
    except FileNotFoundError:
        print("File not found, be sure to have a board.json file in your directory")
    boards["current"] = gui.current_board
    boards["history"] = engine.history
    with open("board.json", "w") as f:
        json.dump(boards, f, indent=4)


if __name__ == "__main__":
    save_game_on_quit()
 