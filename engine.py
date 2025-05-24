"""
Type aliases:
    Position: tuple[int, int] -- (row, column) on the board
    Board: list[list[tuple[str, str]]] -- 8x8 chess board, each cell is (piece, color)
"""

from typing import Optional, Tuple

Board = list[list[Tuple[str, str]]]
Position = Tuple[int, int]

VOID_CELL = ("0", "0")
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
    "bishop": {"moves": ((1, 1), (-1, -1), (1, -1), (-1, 1)), "repeat": True},
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
        ("bishop", "black"),
        ("queen", "black"),
        ("king", "black"),
        ("bishop", "black"),
        ("knight", "black"),
        ("rook", "black"),
    ],
    [("pawnb", "black") for _ in range(8)],
    [VOID_CELL for _ in range(8)],
    [VOID_CELL for _ in range(8)],
    [VOID_CELL for _ in range(8)],
    [VOID_CELL for _ in range(8)],
    [("pawnw", "white") for _ in range(8)],
    [
        ("rook", "white"),
        ("knight", "white"),
        ("bishop", "white"),
        ("king", "white"),
        ("queen", "white"),
        ("bishop", "white"),
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


def list_valid_move(
    board: Board,
    cell: Position,
    specific_piece: Optional[str] = None,
) -> list[tuple[int, int]]:
    """list all valid moves for the piece at the given cell on the board

    Args:
        board (list[list[tuple[str, str]]]): game board
        cell (tuple[int, int]): coordinates of the piece (y,x)
        specific_piece (Optional[str], optional): If provided, use this piece type instead of the actual one in the cell.
         Defaults to None.

    Returns:
        list[tuple[int, int]]: a list with every cells (y,x) where the piece can move to
    """
    y, x = cell
    piece_type = specific_piece or board[y][x][0]
    piece_color = board[y][x][1]
    valid_moves = []

    if piece_type in ("pawnb", "pawnw"):
        return list_valid_move_pawn(board, y, x, piece_type, piece_color)

    repeat = PIECES[piece_type]["repeat"]
    for dy, dx in PIECES[piece_type]["moves"]:
        new_y, new_x = y + dy, x + dx
        while 0 <= new_y <= 7 and 0 <= new_x <= 7:
            target_piece, target_color = board[new_y][new_x]
            if target_color == piece_color:
                break
            valid_moves.append((new_y, new_x))
            if target_piece != VOID_CELL[0] or not repeat:
                break
            new_y += dy
            new_x += dx
    return valid_moves


def list_valid_move_pawn(
    board: Board,
    y: int,
    x: int,
    piece_type: str,
    piece_color: str,
) -> list[Position]:
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
    bound = 6 if piece_color == "white" else 1
    direction = -1 if piece_color == "white" else 1

    for i, move in enumerate(PIECES[piece_type]["moves"]):
        new_y, new_x = y + move[0], x + move[1]
        if 0 <= new_y <= 7 and 0 <= new_x <= 7:
            if i == 0 and board[new_y][new_x] == VOID_CELL:
                move_list.append((new_y, new_x))
                if (
                    new_y < 7
                    and board[y + (2 * direction)][x] == VOID_CELL
                    and bound == y
                ):
                    move_list.append((y + (2 * direction), x))
            elif i != 0:
                if (
                    board[new_y][new_x][1] != piece_color
                    and board[new_y][new_x] != VOID_CELL
                ):
                    move_list.append((new_y, new_x))
    return move_list


def promote_pawn(board: list[list[tuple[str, str]]], cell: tuple[int, int]) -> None:
    """check if a pawn is promotabe then transform the cell in the board with queen

    Args:
        board (list[list[tuple[str, str]]]): game board
        cell (tuple[int, int]): coordinates of the piece (y,x)
    """
    y, x = cell
    if board[y][x][0][0:4] == "pawn":
        if y == PIECES[board[y][x][0]]["promote"]:
            board[y][x] = ("queen", board[y][x][1])


# demander quelle version faire un set supprimer les pièces à chaque fois ? ou parcourir tout le tableau pour voir les pièces dispo ?
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
    checking_cell = []
    if board[y][x][1] not in {"white", "black"}:
        return []
    for piece in PIECES.keys():
        possible_moves = []
        possible_moves.extend(list_valid_move(board, (y, x), piece))
        piece = "pawnw" if piece == "pawnb" else "pawnb" if piece == "pawnw" else piece
        for coord in possible_moves:
            new_y, new_x = coord
            if piece == board[new_y][new_x][0] and coord not in checking_cell:
                checking_cell.append(coord)
    return checking_cell


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
        board[new_y][new_x], board[y][x] = board[y][x], VOID_CELL
        promote_pawn(board, (new_y, new_x))
    else:
        return -1
    return board


if __name__ == "__main__":
    board = [[VOID_CELL for _ in range(8)] for _ in range(8)]
    board[4][4] = ("king", "black")
    board[5][3] = ("pawnw", "white")  # Peut capturer en diagonale

    result = check_check(board, (4, 4))
    print(result)
