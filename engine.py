import colorama as c

# TODO: peut pas faire de tuple de 1 ?
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
    "pawnw": {"moves": ((1, 0)), "repeat": False},
    "pawnb": {"moves": ((-1, 0), (0, 0)), "repeat": False},
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
    "0": {"moves": (), "repeat": False},
}


board = [
    [
        ("rook", "black"),
        ("knight", "black"),
        ("bihsop", "black"),
        ("queen", "black"),
        ("king", "black"),
        ("bihsop", "black"),
        ("knight", "black"),
        ("rook", "black"),
    ],
    [("pawnb", "black") for _ in range(8)],
    ["00" for _ in range(8)],
    ["00" for _ in range(8)],
    ["00" for _ in range(8)],
    ["00" for _ in range(8)],
    [("pawnw", "white") for _ in range(8)],
    [
        ("rook", "white"),
        ("knight", "white"),
        ("bihsop", "white"),
        ("king", "white"),
        ("queen", "white"),
        ("bihsop", "white"),
        ("knight", "white"),
        ("rook", "white"),
    ],
]

board_void = [["00" for _ in range(8)] for _ in range(8)]


def print_board(board):
    for i, line in enumerate(board):
        print(i, end=" ")
        for cell in line:
            print(cell[0][0], end=" ")
        print()


def print_board_highlight(board, cell):
    highlight = list_valid_move(board, cell)
    c.init()
    for i, line in enumerate(board):
        print(i, end=" ")
        for y, cell in enumerate(line):
            if (i, y) in highlight:
                print(c.Fore.RED + cell[0][0] + c.Style.RESET_ALL, end=" ")
            else:
                print(cell[0][0], end=" ")
        print()


def get_piece(board, cell: tuple):
    """
    y puis x
    """
    # TODO : case vide
    return board[cell[0]][cell[1]]


def list_valid_move(board, cell) -> list:
    """
    y puis x
    """
    piece_type = get_piece(board, cell)[0]
    piece_color = get_piece(board, cell)[1]
    print(piece_type)
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
            print(move)
            actualy = actual_position[0] + move[0]
            actualx = actual_position[1] + move[1]
            if 0 <= actualy <= 7 and 0 <= actualx <= 7:
                if get_piece(board, (actualy, actualx))[1] != piece_color:
                    move_list.append((actualy, actualx))
    return move_list


def move_piece(board, y, x, new_y, new_x):
    get_piece(board, (y, x))
    possi = list_valid_move(board, (y, x))
    print(possi)
    if (new_y, new_x) in possi:
        board[new_x][new_y], board[y][x] = board[y][x], "00"
    else:
        print("illegal move")
    return board


if __name__ == "__main__":
    # board_void[4][4] = ("queen", "w")
    # board_void[4][1] = ("queen", "w")
    # print(sorted(list_valid_move(board_void, (4, 4))))
    # print(list_valid_move(board, (0, 1)))
    # print_board_highlight(board_void, (4, 4))
    print_board(board)
    print_board(move_piece(board, 0, 1, 2, 2))
