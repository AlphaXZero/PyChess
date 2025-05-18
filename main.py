import colorama as c


PIECES = {
    "knight": {
        "moves": (
            (2, 1),
            (2, -1),
            (-2, 1),
            (-2, -1),
            (1, 2),
            (1, -2),
            (-1, 2),
            (-1, -2),
        ),
        "repeat": False,
    },
    "rook": {"moves": ((1, 0), (0, 1), (-1, 0), (0, -1)), "repeat": True},
    "king": {"moves": ((1, 0), (0, 1), (-1, 0), (0, -1)), "repeat": False},
    "pawnw": {"moves": (1, 0), "repeat": False},
    "pawnb": {"moves": (-1, 0), "repeat": False},
    "bihsop": {"moves": ((1, 1), (-1, -1), (1, -1), (-1, 1)), "repeat": True},
    "queen": {
        "moves": (
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
        ),
        "repeat": True,
    },
}


board = [
    [
        ("rook", "b"),
        ("knight", "b"),
        ("bihsop", "b"),
        ("queen", "b"),
        ("king", "b"),
        ("bihsop", "b"),
        ("knight", "b"),
        ("rook", "b"),
    ],
    [("pawnb", "b") for _ in range(8)],
    ["00" for _ in range(8)],
    ["00" for _ in range(8)],
    ["00" for _ in range(8)],
    ["00" for _ in range(8)],
    [("pawnw", "w") for _ in range(8)],
    [
        ("rook", "w"),
        ("knight", "w"),
        ("bihsop", "w"),
        ("king", "w"),
        ("queen", "w"),
        ("bihsop", "w"),
        ("knight", "w"),
        ("rook", "w"),
    ],
]

board_void = [["00" for _ in range(8)] for _ in range(8)]


def print_board(board):
    for i, line in enumerate(board):
        print(i, end=" ")
        for cell in line:
            print(cell[0][0], end=" ")
        print()


def print_board_highlight(board, cell2):
    highlight = list_valid_move(board, cell2)
    c.init()
    for i, line in enumerate(board):
        print(i, end=" ")
        for y, cell in enumerate(line):
            if (i, y) in highlight:
                print(c.Fore.RED + cell[0][0] + c.Style.RESET_ALL, end=" ")
            else:
                print(cell[0][0], end=" ")
        print()


def get_piece(board, cell):
    # TODO : case vide
    return board[cell[0]][cell[1]]


def list_valid_move(board, cell) -> list:
    piece_type = get_piece(board, cell)[0]
    piece_color = get_piece(board, cell)[1]
    move_list = []
    for move in PIECES[piece_type]["moves"]:
        actual_position = cell
        if PIECES[piece_type]["repeat"]:
            while True:
                actualy = actual_position[0] + move[0]
                actualx = actual_position[1] + move[1]
                if 0 <= actualy <= 7 and 0 <= actualx <= 7:
                    if get_piece(board, (actualy, actualx))[1] != piece_color:
                        move_list.append((actualy, actualx))
                        actual_position = (actualy, actualx)
                        # TODO : MOCHE CHANGER !
                    if board[actualy][actualx] != "00":
                        break
                else:
                    break
        else:
            actualy = actual_position[0] + move[0]
            actualx = actual_position[1] + move[1]
            if 0 <= actualy <= 7 and 0 <= actualx <= 7:
                if get_piece(board, (actualy, actualx))[1] != piece_color:
                    move_list.append((actualy, actualx))
    return move_list


def move_piece(board): ...


if __name__ == "__main__":
    board_void[4][4] = ("queen", "w")
    board_void[4][1] = ("queen", "w")
    board_void[1][1] = ("queen", "b")
    print(sorted(list_valid_move(board_void, (4, 4))))
    print_board_highlight(board_void, (4, 4))
