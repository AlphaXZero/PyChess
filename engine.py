import colorama as c
from typing import List, Tuple, Optional

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
    [("0", "0") for _ in range(8)],
    [("0", "0") for _ in range(8)],
    [("0", "0") for _ in range(8)],
    [("0", "0") for _ in range(8)],
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


def print_board(board: list[list[tuple[str, str]]]):
    """print the game board

    Args:
        board (list[list[tuple[str, str]]]): game board
    """
    for i, line in enumerate(board):
        print(i, end=" ")
        for cell in line:
            print(cell[0][0], end=" ")
        print()


# TODO : créer une varible avec list[list[tuplestr,str]] ?
# TODO bine comme ça ou mieux de faire board,y,x,test_cehck + etsce bien de préciser autant
# TODO séparer en plus de fonctions ?
def list_valid_move(
    board: list[list[tuple[str, str]]],
    cell: tuple[int, int],
    specific_piece: Optional[str] = None,
) -> list[tuple[int, int]]:
    """list all valid move for the piece at the given cell

    Args:
        board (list[list[tuple[str, str]]]): game board
        cell (tuple[int, int]): coordinates of the piece (y,x)
        specific_piece (Optional[str], optional): If provided, use this piece type instead of the actual one in the cell.
         Defaults to None.

    Returns:
        list[tuple[int, int]]: a list with every cell (y,x) where the piece can go
    """
    y, x = cell
    piece_type = board[y][x][0] if specific_piece is None else specific_piece
    piece_color = board[y][x][1]
    valid_moves = []
    if piece_type != "pawnb" and piece_type != "pawnw":
        for move in PIECES[piece_type]["moves"]:
            current_position = cell
            if PIECES[piece_type]["repeat"]:
                while True:
                    # TODO répétitions .
                    actual_y = current_position[0] + move[0]
                    actual_x = current_position[1] + move[1]
                    if 0 <= actual_y <= 7 and 0 <= actual_x <= 7:
                        if board[actual_y][actual_x][1] != piece_color:
                            valid_moves.append((actual_y, actual_x))
                            current_position = (actual_y, actual_x)
                        if board[actual_y][actual_x] != ("0", "0"):
                            break
                    else:
                        break
            else:
                actual_y = current_position[0] + move[0]
                actual_x = current_position[1] + move[1]
                if 0 <= actual_y <= 7 and 0 <= actual_x <= 7:
                    if board[actual_y][actual_x][1] != piece_color:
                        valid_moves.append((actual_y, actual_x))
    else:
        return list_valid_move_pawn(board, y, x, piece_type, piece_color)
    return valid_moves


# TODO :merge les 2 fonctions
def list_valid_move_pawn(
    board: list[list[tuple[str, str]]],
    y: int,
    x: int,
    piece_type: str,
    piece_color: str,
) -> list[tuple[int, int]]:
    """sub-fonction for list_valid_move

    Args:
        board (list[list[tuple[str, str]]]): _description_
        y (int): y-coordinate
        x (int): x-coordinate
        piece_type (str):
        piece_color (str): "white" | "black

    Returns:
        list[tuple[int, int]]: a list with every cell (y,x) where the pawn can go
    """
    move_list = []
    for i, move in enumerate(PIECES[piece_type]["moves"]):
        actual_y = y + move[0]
        actual_x = x + move[1]
        if i == 0:
            if 0 <= actual_y <= 7 and 0 <= actual_x <= 7:
                if board[actual_y][actual_x] == ("0", "0"):
                    move_list.append((actual_y, actual_x))
        else:
            if 0 <= actual_y <= 7 and 0 <= actual_x <= 7:
                if board[actual_y][actual_x][1] != piece_color and board[actual_y][
                    actual_x
                ] != ("0", "0"):
                    move_list.append((actual_y, actual_x))
    if piece_color == "white" and y == 6:
        if board[y - 1][x] == ("0", "0") and board[y - 2][x] == ("0", "0"):
            move_list.append((y - 2, x))
    elif piece_color == "black" and y == 1:
        if board[y + 1][x] == ("0", "0") and board[y + 2][x] == ("0", "0"):
            move_list.append((y + 2, x))

    return move_list


def promote_pawn(board2, cell):
    if board2[cell[0]][cell[1]][0] == "pawnb" or board2[cell[0]][cell[1]][0] == "pawnw":
        if cell[0] == PIECES[board2[cell[0]][cell[1]][0]]["promote"]:
            board2[cell[0]][cell[1]] = ("queen", board2[cell[0]][cell[1]][1])


def check_check(
    board: list[list[tuple[str, str]]], cell: tuple[int, int]
) -> list[tuple[int, int]]:
    """give the cells where a piece is checking the cell

    Args:
        board (list[list[tuple[str, str]]]): game board
        cell (tuple[int,int]): cell (y,x) where check is needed

    Returns:
        list[tuple[int, int]]: list of positions (y,x) of pieces checking the given cell
    """
    y, x = cell
    checking_cells = []
    target_color = board[y][x][1]
    if target_color not in {"white", "black"}:
        return []
    opponent_color = "black" if target_color == "white" else "white"
    for i in range(8):
        for j in range(8):
            piece, color = board[i][j]
            if color != opponent_color or piece == "0":
                continue
            # Liste des mouvements possibles pour cette pièce
            possible_moves = list_valid_move(board, (i, j))
            if cell in possible_moves:
                checking_cells.append((i, j))
    return checking_cells


def find_king(board: list[list[tuple[str, str]]], color: str) -> tuple[int, int]:
    """find where the king is

    Args:
        board (list[list[tuple[str, str]]]): game board
        color (str): the color of the king we want to find

    Returns:
        tuple[int, int]: tuple  of position (y,x)
    """
    for i, line in enumerate(board):
        for j, cell in enumerate(line):
            if cell[0] == "king" and cell[1] == color:
                return (i, j)


# TODO enlever color
def move_piece(
    board: list[list[tuple[str, str]]],
    y: int,
    x: int,
    new_y: int,
    new_x: int,
    color: str,
) -> list[list[tuple[str, str]]]:
    """move a piece a return the board with the piece mooved

    Args:
        board (list[list[tuple[str, str]]]): game board
        y (int): y value for the initial cell
        x (int): x vlaue for the initial cell
        new_y (int): y value for the wanted cell
        new_x (int): x value for the wanted cell
        color (str): the color of the piece we want to move (to avoid moving an opponent piece)

    Returns:
        list[list[tuple[str, str]]]: gmae board
    """
    if board[y][x][1] != color:
        return -1
    possible_mooves = list_valid_move(board, (y, x))
    if (new_y, new_x) in possible_mooves:
        board[new_y][new_x], board[y][x] = board[y][x], ("0", "0")
        promote_pawn(board, (new_y, new_x))
    else:
        return -1
    return board


if __name__ == "__main__":
    pass
