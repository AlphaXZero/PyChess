PIECES = {
    "knight": {
        "mooves": (
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
    "rook": {"mooves": ((1, 0), (0, 1), (-1, 0), (0, -1)), "repeat": True},
    "king": {"mooves": ((1, 0), (0, 1), (-1, 0), (0, -1)), "repeat": False},
    "pawnw": {"mooves": (1, 0), "repeat": False},
    "pawnb": {"mooves": (-1, 0), "repeat": False},
    "bihsop": {"mooves": ((1, 1), (-1, -1), (1, -1), (-1, 1)), "repeat": True},
    "queen": {
        "mooves": (
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
        ),
        "reapeat": True,
    },
}


board = [
    [
        ("rook", "b"),
        ("knight", "b"),
        ("bishop", "b"),
        ("queen", "b"),
        ("king", "b"),
        ("bishop", "b"),
        ("knight", "b"),
        ("rook", "b"),
    ],
    [("pawnb", "b") for i in range(8)],
    ["0" for i in range(8)],
    ["0" for i in range(8)],
    ["0" for i in range(8)],
    ["0" for i in range(8)],
    [("pawnw", "w") for i in range(8)],
    [
        ("rook", "w"),
        ("knight", "w"),
        ("bishop", "w"),
        ("king", "w"),
        ("queen", "w"),
        ("bishop", "w"),
        ("knight", "w"),
        ("rook", "w"),
    ],
]


def print_board(board):
    for line in board:
        for cell in line:
            print(cell[0][0], end=" ")
        print()


def get_piece(board, cell):
    return board[cell[0]][cell[1]]


print(get_piece(board, (0, 3)))


def list_valid_move(board, cell) -> list:
    piece_type = get_piece(cell)[0]
    piece_color = get_piece(cell)[1]
    move_list = []
    for move in PIECES[piece_type]["mooves"]:
        actual_position = cell
        if PIECES[piece_type]["repeat"]:
            while True:
                actualy = actual_position[0] + move[0]
                actualx = actual_position[1] + move[1]
                if 0 <= actualy <= 7 and 0 <= actualx <= 7:
                    if get_piece((actualy, actualx))[1] != piece_color:
                        move_list.append((actualy, actualx))
                        actual_position = (actualy, actualx)
                        if board[actualy, actualx] != 0:
                            break
                else:
                    break
        else:
            actualy = actual_position[0] + move[0]
            actualx = actual_position[1] + move[1]
            if 0 <= actualy <= 9 and 0 <= actualx <= 9:
                if get_piece((actualy, actualx))[1] != piece_color:
                    move_list.append(move)


def moove_piece(board): ...


def main():
    print_board(board)


if __name__ == "__main__":
    main()
