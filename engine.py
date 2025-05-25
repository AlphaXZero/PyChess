"""
Chess board game engine
Type aliases:
    Position: tuple[int, int] -- (row, column) on the board
    Board: list[list[tuple[str, str]]] -- 8x8 chess board, each cell is (piece, color)
"""

__author__ = "georgevdv"
__version__ = "0.8.0"
from typing import Optional, Tuple, TypedDict
from copy import deepcopy
import colorama as c

Board = list[list[Tuple[str, str]]]
Position = Tuple[int, int]

VOID_CELL = ("0", "0")
HISTORY: list[dict] = []
X_NAME = ("a", "b", "c", "d", "e", "f", "g", "h")
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


board: Board = [
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


def print_board(board: Board) -> None:
    """
    Print the game board to the console.

    Args:
        board (Board): The chess board to display.
    """
    c.init()
    for i, line in enumerate(board):
        print(8 - i, end=" ")
        for cell in line:
            if cell[1] == "white":
                print(c.Back.WHITE + cell[0][0] + c.Style.RESET_ALL, end=" ")
            elif cell[1] == "black":
                print(c.Back.BLUE + cell[0][0] + c.Style.RESET_ALL, end=" ")
            else:
                print(cell[0][0], end=" ")
        print()
    print("O a b c d e f g h")


def list_valid_move(
    board: Board,
    cell: Position,
    specific_piece: Optional[str] = None,
    ignore_king_safety: bool = False,
) -> list[Position]:
    """
    List all valid moves for the piece at a given cell on the board.

    Args:
        board (Board): The chess board.
        cell (Position): Coordinates (row, column) of the piece.
        specific_piece (Optional[str], optional): If provided, use this piece type
            instead of the one actually in the cell.

    Returns:
        list[Position]: A list of cells (row, column) where the piece can move.
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
    if piece_type == "king" and not ignore_king_safety:
        safe_moves = []
        for new_y, new_x in valid_moves:
            sim_board = deepcopy(board)
            sim_board[new_y][new_x], sim_board[y][x] = (
                sim_board[y][x],
                sim_board[new_y][new_x],
            )
            if not is_check(sim_board, (new_y, new_x)):
                safe_moves.append((new_y, new_x))
        return safe_moves

    return valid_moves


# TODO : en passant bug 2 pions déplacé de 2
def list_valid_move_pawn(
    board: Board,
    y: int,
    x: int,
    piece_type: str,
    piece_color: str,
) -> list[Position]:
    """
    List all valid moves for a pawn at the given position.

    Args:
        board (Board): The chess board.
        y (int): Row coordinate of the pawn.
        x (int): Column coordinate of the pawn.
        piece_type (str): Piece type (e.g., "pawnw" or "pawnb").
        piece_color (str): Piece color ("white" or "black").

    Returns:
        list[Position]: A list of cells (row, column) where the pawn can move.
    """
    move_list = []
    bound = 6 if piece_color == "white" else 1
    direction = (-1) if piece_color == "white" else 1

    for i, move in enumerate(PIECES[piece_type]["moves"]):
        new_y, new_x = y + move[0], x + move[1]
        if 0 <= new_y <= 7 and 0 <= new_x <= 7:
            if i == 0 and board[new_y][new_x] == VOID_CELL:
                move_list.append((new_y, new_x))
                if (
                    new_y < 7
                    and bound == y
                    and board[y + (2 * direction)][x] == VOID_CELL
                ):
                    move_list.append((y + (2 * direction), x))
            elif i != 0:
                en_passant_bound = 3 if "white" == piece_color else 4

                if (
                    board[new_y][new_x][1] != piece_color
                    and board[new_y][new_x] != VOID_CELL
                ) or (
                    y == en_passant_bound
                    and board[new_y - direction][new_x][0][:-1] == "pawn"
                    and board[new_y - direction][new_x][1] != piece_color
                    and len(HISTORY) != 0
                    and abs(HISTORY[-1]["cell"][0] - HISTORY[-1]["new_cell"][0]) == 2
                ):
                    move_list.append((new_y, new_x))
    return move_list


def promote_pawn(board: Board, cell: Position) -> None:
    """
    Promote a pawn to a queen if it has reached the promotion rank.

    Args:
        board (Board): The chess board.
        cell (Position): Coordinates (row, column) of the pawn.
    """
    y, x = cell
    if board[y][x][0][0:4] == "pawn":
        if y == PIECES[board[y][x][0]]["promote"]:
            board[y][x] = ("queen", board[y][x][1])


# TODO changer pour autre bersion je pense
def is_check(board: Board, cell: Position) -> list[Position]:
    """
    Return the positions of pieces that are checking the given cell.

    Args:
        board (Board): The chess board.
        cell (Position): The cell (row, column) to check.

    Returns:
        list[Position]: Positions of pieces checking the given cell.
    """
    y, x = cell
    checking_cells = []
    piece_color = board[y][x][1]
    for n_y in range(8):
        for n_x in range(8):
            if board[n_y][n_x][1] != piece_color:
                if (y, x) in list_valid_move(
                    board, (n_y, n_x), ignore_king_safety=True
                ):
                    checking_cells.append((n_y, n_x))
    return checking_cells


def is_check_mat(board: Board, cell: Position) -> bool:
    """
    Determines whether the king is in checkmate from a given position on the board.

    Args:
        board (Board): The current state of the chessboard, including all pieces and their positions.
        cell (Position): The position of the king to check for checkmate.

    Returns:
        bool: True if checkmate else False
    """
    y, x = cell
    piece_color = board[y][x][1]
    for move in PIECES[board[y][x][0]]["moves"]:
        new_y, new_x = y + move[0], x + move[1]
        board_test = deepcopy(board)
        board_test = move_piece(board_test, y, x, new_y, new_x, piece_color)
        if board_test is None:
            continue
        if is_check(board_test, (new_y, new_x)) == []:
            return False
    return True


def is_stalemate(board: Board, cell: Position) -> bool:
    if is_check(board, cell):
        return False

    for move in list_valid_move(board, cell, ignore_king_safety=True):
        sim_board = deepcopy(board)
        sim_board = move_piece(
            sim_board, cell[0], cell[1], move[0], move[1], board[cell[0]][cell[1]][1]
        )
        if not is_check(board, (move[0], move[1])):
            return False
    return True


def is_rock(board: Board, cell: Position) -> bool:
    pass


def find_king(board: Board, color: str) -> Optional[Position]:
    """
    Find the position of the king of the specified color.

    Args:
        board (Board): The chess board.
        color (str): The color of the king to find ("white" or "black").

    Returns:
        Optional[Position]: Position (row, column) of the king, or None if not found.
    """
    for i, line in enumerate(board):
        for j, cell in enumerate(line):
            if cell[0] == "king" and cell[1] == color:
                return (i, j)
    return None


def move_piece(
    board: Board,
    y: int,
    x: int,
    new_y: int,
    new_x: int,
    color: str,
) -> Board | None:
    """
    Move a piece from (y, x) to (new_y, new_x) if the move is valid.

    Args:
        board (Board): The chess board.
        y (int): Row of the piece to move.
        x (int): Column of the piece to move.
        new_y (int): Destination row.
        new_x (int): Destination column.
        color (str): The color of the piece to move.

    Returns:
        Board | None: The updated chess board if the move is valid, otherwise None.
    """
    if board[y][x][1] != color:
        return None
    possible_moves = list_valid_move(board, (y, x))
    if (new_y, new_x) in possible_moves:
        update_history(HISTORY, board, (y, x), (new_y, new_x))
        if (
            len(HISTORY) >= 2
            and HISTORY[-1]["piece_symbol"][0] == "p"
            and HISTORY[-2]["piece_symbol"][0] == "p"
            and HISTORY[-2]["new_cell"][1] == HISTORY[-1]["new_cell"][1]
        ):
            direction = 1 if color == "white" else -1
            board[new_y + direction][new_x] = VOID_CELL
        board[new_y][new_x], board[y][x] = board[y][x], VOID_CELL
        promote_pawn(board, (new_y, new_x))

    else:
        return None
    return board


# TODO regarder si autre piece peut aller là-bas pour enlever le y,x
def update_history(
    history: list[dict], board: Board, cell: Position, new_cell: Position
) -> list[dict]:
    """
    update an list history with a move

    Args:
        history (list[str]): base history
        board (Board): game board
        cell (Position): the initial cell
        new_cell (Position): the cell afetr move

    Returns:
        list[str]: updated history with the move added
    """
    y, x = 8 - cell[0], X_NAME[cell[1]]
    n_y, n_x = 8 - new_cell[0], X_NAME[new_cell[1]]
    piece = board[cell[0]][cell[1]][0]
    piece_symbol = piece[0] if piece[0] != "p" else piece[0] + piece[-1]
    history.append(
        {"piece_symbol": piece_symbol, "cell": (y, x), "new_cell": (n_y, n_x)}
    )
    return history


def format_history(history: list[dict[str]]) -> list[str]:
    """return a list woth formated history

    Args:
        history (list[dict[str]]): _description_
    """
    text_history = []
    for item in history:
        text_history.append(
            f"{item['piece_symbol']}{item['cell'][1]}{item['cell'][0]}->{item['new_cell'][1]}{item['new_cell'][0]}"
        )
    return text_history


if __name__ == "__main__":
    board = [[VOID_CELL for _ in range(8)] for _ in range(8)]
    # Pat : roi noir en h8, roi blanc en f7, dame blanche en g6

    # board[7][7] = ("king", "white")
    # board[6][6] = ("pawnw", "black")
    # board[5][5] = ("king", "black")
    # print(is_check(board, (7, 7)))
    # print_board(board)
    # print(is_check_mat(board, (7, 7)))

    print("--------------------")
    board[7][7] = ("king", "black")
    board[5][6] = ("queen", "white")
    board[5][5] = ("king", "white")
    print_board(board)
    print("ici", is_stalemate(board, (7, 7)))
