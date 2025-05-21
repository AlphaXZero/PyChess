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
    "king": {
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
        "repeat": False,
    },
    "pawnw": {"moves": ((-1, 0), (-1, -1), (-1, 1)), "repeat": False, "promote": 0},
    "pawnb": {"moves": ((1, 0), (1, 1), (1, -1)), "repeat": False, "promote": 7},
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


def list_valid_move(board, cell, test_check=None) -> list:
    """
    y puis x
    """
    piece_type = get_piece(board, cell)[0] if test_check is None else test_check
    piece_color = get_piece(board, cell)[1]
    move_list = []
    if piece_type != "pawnb" and piece_type != "pawnw":
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
    else:
        return list_valid_move_pawn(board, cell)
    return move_list


# TODO :merge les 2 fonctions
def list_valid_move_pawn(board, cell):
    piece_type = get_piece(board, cell)[0]
    piece_color = get_piece(board, cell)[1]
    move_list = []
    if piece_color == "white" and cell[0] == 6:
        if board[cell[0] - 1][cell[1]] == "00":
            move_list.extend([(cell[0] - 1, cell[1]), (cell[0] - 2, cell[1])])
    elif piece_color == "black" and cell[0] == 1:
        if board[cell[0] + 1][cell[1]] == "00":
            move_list.extend([(cell[0] + 1, cell[1]), (cell[0] + 2, cell[1])])
    else:
        for i, move in enumerate(PIECES[piece_type]["moves"]):
            actualy = cell[0] + move[0]
            actualx = cell[1] + move[1]
            if i == 0:
                if 0 <= actualy <= 7 and 0 <= actualx <= 7:
                    if get_piece(board, (actualy, actualx)) == "00":
                        move_list.append((actualy, actualx))
            else:
                if 0 <= actualy <= 7 and 0 <= actualx <= 7:
                    if (
                        get_piece(board, (actualy, actualx))[1] != piece_color
                        and get_piece(board, (actualy, actualx)) != "00"
                    ):
                        move_list.append((actualy, actualx))

    return move_list


def promote_pawn(board2, cell):
    if board2[cell[0]][cell[1]][0] == "pawnb" or board2[cell[0]][cell[1]][0] == "pawnw":
        if cell[0] == PIECES[board2[cell[0]][cell[1]][0]]["promote"]:
            board2[cell[0]][cell[1]] = ("queen", board2[cell[0]][cell[1]][1])


# TODO : pions bug
def check_check(board, cell):
    cells_where_check = []
    for piece in PIECES.keys():
        place_to_check = list_valid_move(board, cell, piece)
        for i in place_to_check:
            if board[i[0]][i[1]][0] == piece:
                cells_where_check.append((i[0], i[1]))
    return cells_where_check


def find_king(board, color):
    for i, line in enumerate(board):
        for j, cell in enumerate(line):
            if cell[0] == "king" and cell[1] == color:
                return (i, j)


# TODO bug pion bouge
def move_piece(board, y, x, new_y, new_x):
    get_piece(board, (y, x))
    possi = list_valid_move(board, (y, x))
    if (new_y, new_x) in possi:
        board[new_y][new_x], board[y][x] = board[y][x], "00"
        promote_pawn(board, (new_y, new_x))
    else:
        return None
    return board


if __name__ == "__main__":
    # board_void[4][1] = ("queen", "w")
    # print(sorted(list_valid_move(board_void, (4, 4))))
    # print(list_valid_move(board, (0, 1)))
    # board_void = [["00" for _ in range(8)] for _ in range(8)]
    # board_void[4][4] = ("queen", "black")
    # board_void[2][3] = ("knight","white")
    # print_board_highlight(board, (1, 4))
    # print(list_valid_move(board, (6, 4)))
    # print(check_check(board_void,(4,4)))
    # print("fin")
    # print(find_king(board,"black"))

    board = [["00" for _ in range(8)] for _ in range(8)]
    board[4][4] = ("king", "white")
    board[3][4] = ("pawnb", "black")  # Ne peut pas capturer droit devant
    result = check_check(board, (4, 4))
    print_board(board)
