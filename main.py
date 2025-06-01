import json
import engine
import GUI


def save_game_on_quit():
    GUI.build_app().mainloop()
    with open("board.json", "r") as f:
        boards = json.load(f)
    boards["current"] = GUI.current_board
    boards["history"] = engine.HISTORY
    with open("board.json", "w") as f:
        json.dump(boards, f, indent=4)


if __name__ == "__main__":
    save_game_on_quit()
