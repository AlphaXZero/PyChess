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
    for i, line in enumerate(board):
        print(i, end=" ")
        for cell in line:
            print(cell[0][0], end=" ")
        print()


def list_valid_move(
    board: Board,
    cell: Position,
    specific_piece: Optional[str] = None,
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
    return valid_moves


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


def check_check(board: Board, cell: Position) -> list[Position]:
    """
    Return the positions of pieces that are checking the given cell.

    Args:
        board (Board): The chess board.
        cell (Position): The cell (row, column) to check.

    Returns:
        list[Position]: Positions of pieces checking the given cell.
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
) -> Board:
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
        Board: The updated chess board if the move is valid, otherwise -1.
    """
    if board[y][x][1] != color:
        return -1
    possible_moves = list_valid_move(board, (y, x))
    if (new_y, new_x) in possible_moves:
        board[new_y][new_x], board[y][x] = board[y][x], VOID_CELL
        promote_pawn(board, (new_y, new_x))
    else:
        return -1
    return board


if __name__ == "__main__":
    board = [[VOID_CELL for _ in range(8)] for _ in range(8)]
    board[4][4] = ("king", "black")
    board[5][3] = ("pawnw", "white")  # Can capture diagonally

    result = check_check(board, (4, 4))
    print(result)
