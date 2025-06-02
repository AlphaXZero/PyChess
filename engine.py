"""
Chess board game engine
Type aliases:
    Position: tuple[int, int] -- (row, column) on the board
    Board: list[list[tuple[str, str]]] -- 8x8 chess board, each cell is (piece, color)
"""

__author__ = "georgevdv"
__version__ = "0.8.0"
from typing import Optional, Tuple, Literal
from copy import deepcopy
import colorama as c
import json


Board = list[list[list[str, str]]]
Position = Tuple[int, int]

VOID_CELL = ["0", "0"]
COLOR = ("white", "black")

X_NAME = ("a", "b", "c", "d", "e", "f", "g", "h")
with open("board.json", "r") as f:
    game_state = json.load(f)
board: Board = (
    game_state["default"] if game_state["current"] == [] else game_state["current"]
)
history: list[dict] = [] if game_state["history"] == [] else game_state["history"]
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


def print_board(board: Board) -> None:
    """
    Print the game board to the console. (used for testing)

    Args:
        board (Board): The chess board to display.
    """
    c.init()
    for i, line in enumerate(board):
        print(8 - i, end=" ")
        for cell in line:
            if cell[1] == "white":
                print(
                    c.Back.WHITE + (cell[0][0]) + c.Style.RESET_ALL,
                    end=" ",
                )
            elif cell[1] == "black":
                print(
                    c.Back.BLUE + (cell[0][0]) + c.Style.RESET_ALL,
                    end=" ",
                )
            else:
                print(cell[0][0], end=" ")
        print()
    print(" ", " ".join(X_NAME))


def find_king(board: Board, color: str) -> Position:
    """
    Find the position of the specified color king in the board

    Args:
        board (Board): game board
        color (str): color of the king we want to search

    Returns:
        Position: return a tuple with (y,x) values where the king is
    """
    for i, line in enumerate(board):
        for j, cell in enumerate(line):
            if cell[0] == "king" and cell[1] == color:
                return (i, j)


def list_valid_move(
    board: Board,
    cell: Position,
    specific_piece: Optional[str] = None,
    ignore_king_safety: bool = False,
    only_control: bool = False,
) -> list[Position]:
    """
    List all the position where the piece at the given position can go

    Args:
        board (Board): game board
        cell (Position): position (y,x) of the piece
        specific_piece (Optional[str], optional): used for is_check, simulate another piece type than the one at the given positon. Defaults to None.
        ignore_king_safety (bool, optional): if True, dont look if the king is check after move. Defaults prevent the player to check himself. Defaults to False.
        only_control (bool, optional): used for is_check, only look after the control zone of the pawn. Defaults to False.

    Returns:
        list[Position]: list of tuple (y,x) with every positons where the piece can go
    """
    y, x = cell
    piece_type = specific_piece or board[y][x][0]
    piece_color = board[y][x][1]
    valid_moves = []
    if piece_type in ("pawnb", "pawnw"):
        if only_control:
            return get_control_pawn(cell, piece_type)

        valid_moves = list_valid_move_pawn(board, cell, piece_type, piece_color)
    else:
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

    if ignore_king_safety:
        return valid_moves

    safe_moves = []
    for new_y, new_x in valid_moves:
        sim_board = deepcopy(board)
        sim_board[new_y][new_x], sim_board[y][x] = sim_board[y][x], VOID_CELL
        king_cell = find_king(sim_board, piece_color)
        if king_cell and not get_checking_pieces(sim_board, king_cell):
            safe_moves.append((new_y, new_x))
    if piece_type == "king":
        safe_moves.extend(list_valid_castling(board, piece_color))
    return safe_moves


def get_control_pawn(
    cell: Position, piece_type: Literal["pawnb", "pawnw"]
) -> list[Position]:
    """
    used by list_valid_move, list all the cell controlled by a pawn

    Args:
        cell (Position): (y,x) values in the board
        piece_type (Literal["pawnb", "pawnw")

    Returns:
        list[Position]: tuple with tuple of cell (y,x) that piece controls
    """
    controlled_cell_list = []
    y, x = cell
    piece_type = "pawnb" if piece_type == "pawnw" else "pawnw"
    for i, move in enumerate(PIECES[piece_type]["moves"]):
        if 0 <= y + move[0] <= 7 and 0 <= x + move[1] <= 7 and i != 0:
            controlled_cell_list.append((y + move[0], x + move[1]))
    return controlled_cell_list


def list_valid_move_pawn(
    board: Board, cell: Position, piece_type: str, piece_color: str
) -> list[Position]:
    """
    used by list_valid_move, same as list_valid_move but for pawn

    Args:
        board (Board): game board
        cell (Position): (y,x) values
        piece_type (str):
        piece_color (str): "black" | "white"

    Returns:
        list[Position]: list with tuple of postions (y,x) where the pawn can go
    """
    y, x = cell
    valid_moves = []
    initial_pawn_row = 6 if piece_color == "white" else 1
    en_passant_bound = 3 if piece_color == "white" else 4
    direction = (-1) if piece_color == "white" else 1

    for i, move in enumerate(PIECES[piece_type]["moves"]):
        new_y, new_x = y + move[0], x + move[1]
        if 0 <= new_y <= 7 and 0 <= new_x <= 7:
            if i == 0 and board[new_y][new_x] == VOID_CELL:
                valid_moves.append((new_y, new_x))
                if initial_pawn_row == y and board[new_y + move[0]][x] == VOID_CELL:
                    valid_moves.append((new_y + move[0], x))
            elif i != 0:
                if (
                    board[new_y][new_x][1] != piece_color
                    and board[new_y][new_x] != VOID_CELL
                ):
                    valid_moves.append((new_y, new_x))
                if (
                    y == en_passant_bound
                    and board[new_y - direction][new_x][0][:4] == "pawn"
                    and board[new_y - direction][new_x][1] != piece_color
                    and abs(history[-1]["cell"][0] - history[-1]["new_cell"][0]) == 2
                ):
                    valid_moves.append((new_y, history[-1]["new_cell"][1]))
    return valid_moves


def get_checking_pieces(
    board: Board, cell: Position, color: str = None
) -> list[Position]:
    """
    Returns the positions of pieces checking the given position

    Args:
        board (Board): game board
        cell (Position): position (y,x) values
        color (str, optional): mainly used for castling, color of the current player. Defaults to None.

    Returns:
        list[Position]: list of Positions that are checking the cell given
    """
    y, x = cell
    checking_cells = []
    piece_color = color or board[y][x][1]
    for i in PIECES.keys():
        for new_y, new_x in list_valid_move(
            board,
            cell,
            i,
            ignore_king_safety=True,
            only_control=True,
        ):
            if board[new_y][new_x][0] == i and piece_color != board[new_y][new_x][1]:
                checking_cells.append((new_y, new_x))
    return checking_cells


def is_checkmat(board: Board, cell: Position) -> bool:
    """
    Returns True if the game is checkmate.

    Args:
        board (Board): game board
        cell (Position): Position (y,x) values

    Returns:
        bool: True if check_mat, False otherwise
    """
    color = board[cell[0]][cell[1]][1]
    if not get_checking_pieces(board, cell):
        return False

    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece[1] != color:
                continue
            valid_moves = list_valid_move(board, (y, x))
            for move in valid_moves:
                sim_board = deepcopy(board)
                sim_board = move_piece(sim_board, (y, x), move, color, no_mem=True)
                king_pos = find_king(sim_board, color)
                if sim_board and not get_checking_pieces(sim_board, king_pos):
                    return False
    return True


def is_stalemate(board: Board, cell: Position) -> bool:
    """
    return True if the game is stalemate

    Args:
        board (Board): game board
        cell (Position): Position (y,x) values

    Returns:
        bool: True if stalemate, False otherwise
    """
    y, x = cell
    if get_checking_pieces(board, cell):
        return False
    for move in list_valid_move(board, cell, ignore_king_safety=True):
        sim_board = deepcopy(board)
        sim_board = move_piece(
            sim_board,
            (y, x),
            (move[0], move[1]),
            board[y][x][1],
            no_mem=True,
        )
        if not get_checking_pieces(board, (move[0], move[1])):
            return False
    for i, line in enumerate(board):
        for j, piece in enumerate(line):
            if piece[1] == board[y][x][1]:
                print(piece)
                if list_valid_move(board, (i, j)) != []:
                    return False

    return True


def is_draw_repetitions(board: Board, past_board: list[Board]) -> bool:
    """
    check if the same positions appears 3 times

    Args:
        board (_type_): game board
        past_board (_type_): list of past games board

    Returns:
        _type_: True if is a draw, False otherwise
    """
    count = sum(1 for past in past_board if past == board)
    return count >= 3


def promote_pawn(board: Board, cell: Position) -> None:
    """
    Transforms a pawn in a queen

    Args:
        board (Board): game board
        cell (Position): Position (y,x) values of the cell to check
    """
    y, x = cell
    if board[y][x][0][0:4] == "pawn":
        if y == PIECES[board[y][x][0]]["promote"]:
            board[y][x] = ["queen", board[y][x][1]]


def list_valid_castling(board: Board, color: str) -> list[Position]:
    """
    returns the position where the king can castle

    Args:
        board (Board): game board
        color (str): the color of the player who wants to castle

    Returns:
        list[Position]: list of tuple (y,x) values where the king can castle
    """
    valid_castling_moves = []
    player_turn = COLOR.index(color)
    y, x = find_king(board, color)
    for i, hist in enumerate(history):
        if hist["piece_type"] == "king" and (i % 2) == player_turn:
            return valid_castling_moves

    # left
    if board[y][0][0] == "rook" and board[y][1:x] == [VOID_CELL] * (x - 1):
        flag = True
        for i, hist in enumerate(history):
            if (
                hist["piece_type"] == "rook"
                and hist["cell"] == (y, 0)
                and i % 2 == player_turn
            ):
                flag = False
                break
        for i in range(5):
            if get_checking_pieces(board, (y, 0 + i), color) != []:
                flag = False
                break
        if flag:
            valid_castling_moves.append((y, len(board[y][1:x]) - 1))
    # right
    if board[y][-1][0] == "rook" and board[y][x + 1 : -1] == [VOID_CELL] * (abs(x - 6)):
        flag = True
        for i, hist in enumerate(history):
            if (
                hist["piece_type"] == "rook"
                and hist["cell"] == (y, 7)
                and i % 2 == player_turn
            ):
                flag = False
                break
        for i in range(4):
            if get_checking_pieces(board, (y, 4 + i), color) != []:
                flag = False
                break
        if flag:
            valid_castling_moves.append((y, 4 + len(board[y][1:x]) - 1))

    return valid_castling_moves


def move_piece(
    board: Board, cell: Position, new_cell: Position, color: str, no_mem: bool = False
) -> Board | None:
    """
    take a game board, a cell and a new_cell to move and returns the board with the piece moved

    Args:
        board (Board): game_board
        cell (Position): initial position (y,x)
        new_cell (Position): position where to move
        color (str): color of the player's turn
        no_mem (bool, optional): used to avoid is_check_mate adding things in the HISTORY. Defaults to False.

    Returns:
        Board | None: return the board with the movement done or None if the position is unreachable
    """
    y, x = cell
    new_y, new_x = new_cell
    piece_type = board[y][x][0]
    if board[y][x][1] != color:
        return None
    possible_moves = list_valid_move(board, (y, x))
    if (new_y, new_x) in possible_moves:
        if not no_mem:
            update_history(history, piece_type, (y, x), (new_y, new_x))
        # en_passant
        if (
            len(history) > 2
            and history[-1]["piece_type"][0] == "p"
            and history[-2]["piece_type"][0] == "p"
            and history[-2]["cell"][1] != history[-1]["cell"][1]
            and history[-2]["new_cell"][1] == history[-1]["new_cell"][1]
        ):
            direction = 1 if color == "white" else -1
            board[new_y + direction][new_x] = VOID_CELL
        # castle
        if piece_type == "king" and abs(new_x - x) == 2:
            if new_x == 2:
                board[y][0], board[y][3] = board[y][3], board[y][0]
            else:
                board[y][7], board[y][5] = board[y][5], board[y][7]

        board[new_y][new_x], board[y][x] = board[y][x], VOID_CELL
        promote_pawn(board, (new_y, new_x))

    else:
        return None
    return board


def update_history(
    history: list[dict], piece: str, cell: Position, new_cell: Position
) -> list[dict]:
    """
    add move in the history

    Args:
        history (list[dict]): old moves
        piece (str): king, rook, ...
        cell (Position): position (y,x) pre move
        new_cell (Position): positon (y,x) post move

    Returns:
        list[dict]: list with moves
    """
    y, x = cell
    new_y, new_x = new_cell
    history.append({"piece_type": piece, "cell": (y, x), "new_cell": (new_y, new_x)})
    return history


def format_history(history: list[dict[str]]) -> list[str]:
    """
    format the history to be redeable

    Args:
        history (list[dict[str]]): list of moves to format

    Returns:
        list[str]: list of moves formatted
    """
    text_history = []
    for item in history:
        text_history.append(
            f"{item['piece_type']} {X_NAME[item['cell'][1]]}{8 - item['cell'][0]} -> {X_NAME[item['new_cell'][1]]}{8 - item['new_cell'][0]}"
        )
    return text_history


if __name__ == "__main__":
    pass
