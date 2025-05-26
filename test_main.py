import pytest
from engine import list_valid_move, VOID_CELL, Board, HISTORY


@pytest.fixture(autouse=True)
def reset_history():
    HISTORY.clear()


def empty_board() -> Board:
    return [[VOID_CELL for _ in range(8)] for _ in range(8)]


class TestKnightListValidMove:
    def test_knight_center_of_board(self):
        board = empty_board()
        board[3][3] = ("knight", "white")
        expected_moves = [
            (5, 4),
            (5, 2),
            (1, 4),
            (1, 2),
            (4, 5),
            (4, 1),
            (2, 5),
            (2, 1),
        ]
        result = list_valid_move(board, (3, 3), ignore_king_safety=True)
        assert sorted(result) == sorted(expected_moves)

    def test_knight_blocked_by_own_pieces(self):
        board = empty_board()
        board[3][3] = ("knight", "white")
        board[5][4] = ("pawnw", "white")
        board[1][4] = ("pawnw", "white")
        expected_moves = [(5, 2), (1, 2), (4, 5), (4, 1), (2, 5), (2, 1)]
        result = list_valid_move(board, (3, 3), ignore_king_safety=True)
        assert sorted(result) == sorted(expected_moves)

    def test_knight_can_take_enemy_piece(self):
        board = empty_board()
        board[3][3] = ("knight", "white")
        board[5][2] = ("pawnw", "black")
        board[2][5] = ("queen", "black")
        expected_moves = [
            (5, 4),
            (5, 2),
            (1, 4),
            (1, 2),
            (4, 5),
            (4, 1),
            (2, 5),
            (2, 1),
        ]
        result = list_valid_move(board, (3, 3), ignore_king_safety=True)
        assert sorted(result) == sorted(expected_moves)

    def test_knight_on_edge(self):
        board = empty_board()
        board[0][0] = ("knight", "white")
        expected_moves = [(1, 2), (2, 1)]
        result = list_valid_move(board, (0, 0), ignore_king_safety=True)
        assert sorted(result) == sorted(expected_moves)

    def test_knight_surrounded_by_own_and_enemy(self):
        board = empty_board()
        board[3][3] = ("knight", "white")
        board[5][4] = ("pawnw", "white")
        board[5][2] = ("pawnw", "black")
        board[1][4] = ("pawnw", "white")
        board[1][2] = ("pawnw", "black")
        expected_moves = [(5, 2), (1, 2), (4, 5), (4, 1), (2, 5), (2, 1)]
        result = list_valid_move(board, (3, 3), ignore_king_safety=True)
        assert sorted(result) == sorted(expected_moves)


class TestRookListValidMove:
    def test_rook_open_lines(self):
        board = empty_board()
        board[4][4] = ("rook", "white")
        expected_moves = [
            (3, 4),
            (2, 4),
            (1, 4),
            (0, 4),
            (5, 4),
            (6, 4),
            (7, 4),
            (4, 3),
            (4, 2),
            (4, 1),
            (4, 0),
            (4, 5),
            (4, 6),
            (4, 7),
        ]
        result = list_valid_move(board, (4, 4), ignore_king_safety=True)
        assert sorted(result) == sorted(expected_moves)

    def test_rook_blocked_by_own_piece(self):
        board = empty_board()
        board[4][4] = ("rook", "white")
        board[6][4] = ("pawnw", "white")
        board[4][2] = ("pawnw", "white")
        expected_moves = [
            (3, 4),
            (2, 4),
            (1, 4),
            (0, 4),
            (5, 4),
            (4, 3),
            (4, 5),
            (4, 6),
            (4, 7),
        ]
        result = list_valid_move(board, (4, 4), ignore_king_safety=True)
        assert sorted(result) == sorted(expected_moves)

    def test_rook_can_take_enemy(self):
        board = empty_board()
        board[4][4] = ("rook", "white")
        board[7][4] = ("pawnw", "black")
        board[4][0] = ("pawnw", "black")
        expected_moves = [
            (3, 4),
            (2, 4),
            (1, 4),
            (0, 4),
            (5, 4),
            (6, 4),
            (7, 4),
            (4, 3),
            (4, 2),
            (4, 1),
            (4, 0),
            (4, 5),
            (4, 6),
            (4, 7),
        ]
        result = list_valid_move(board, (4, 4), ignore_king_safety=True)
        assert (7, 4) in result
        assert (4, 0) in result
        assert sorted(result) == sorted(expected_moves)

    def test_rook_on_corner(self):
        board = empty_board()
        board[0][0] = ("rook", "white")
        expected_moves = [(i, 0) for i in range(1, 8)] + [(0, i) for i in range(1, 8)]
        result = list_valid_move(board, (0, 0), ignore_king_safety=True)
        assert sorted(result) == sorted(expected_moves)


class TestPawnListValidMove:
    def test_white_pawn_initial_two_steps(self):
        board = empty_board()
        board[6][4] = ("pawnw", "white")
        expected = [(5, 4), (4, 4)]
        result = list_valid_move(board, (6, 4), ignore_king_safety=True)
        assert sorted(result) == sorted(expected)

    def test_white_pawn_blocked(self):
        board = empty_board()
        board[6][4] = ("pawnw", "white")
        board[5][4] = ("pawnw", "black")
        expected = []
        result = list_valid_move(board, (6, 4), ignore_king_safety=True)
        assert result == expected

    def test_white_pawn_capture(self):
        board = empty_board()
        board[4][4] = ("pawnw", "white")
        board[3][3] = ("pawnb", "black")
        board[3][5] = ("queen", "black")
        expected = [(3, 4), (3, 3), (3, 5)]
        result = list_valid_move(board, (4, 4), ignore_king_safety=True)
        assert sorted(result) == sorted(expected)

    def test_white_pawn_cannot_capture_own(self):
        board = empty_board()
        board[4][4] = ("pawnw", "white")
        board[3][3] = ("pawnw", "white")
        expected = [(3, 4)]
        result = list_valid_move(board, (4, 4), ignore_king_safety=True)
        assert sorted(result) == sorted(expected)

    def test_black_pawn_initial_two_steps(self):
        board = empty_board()
        board[1][4] = ("pawnb", "black")
        expected = [(2, 4), (3, 4)]
        result = list_valid_move(board, (1, 4), ignore_king_safety=True)
        assert sorted(result) == sorted(expected)

    def test_black_pawn_blocked(self):
        board = empty_board()
        board[1][4] = ("pawnb", "black")
        board[2][4] = ("pawnw", "white")
        expected = []
        result = list_valid_move(board, (1, 4), ignore_king_safety=True)
        assert result == expected

    def test_black_pawn_capture(self):
        board = empty_board()
        board[3][4] = ("pawnb", "black")
        board[4][3] = ("pawnw", "white")
        board[4][5] = ("queen", "white")
        expected = [(4, 4), (4, 3), (4, 5)]
        result = list_valid_move(board, (3, 4), ignore_king_safety=True)
        assert sorted(result) == sorted(expected)

    def test_black_pawn_cannot_capture_own(self):
        board = empty_board()
        board[3][4] = ("pawnb", "black")
        board[4][3] = ("pawnb", "black")
        expected = [(4, 4)]
        result = list_valid_move(board, (3, 4), ignore_king_safety=True)
        assert sorted(result) == sorted(expected)

    def test_pawn_on_last_rank(self):
        board = empty_board()
        board[0][5] = ("pawnw", "white")
        result = list_valid_move(board, (0, 5), ignore_king_safety=True)
        assert result == []

        board = empty_board()
        board[7][2] = ("pawnb", "black")
        result = list_valid_move(board, (7, 2), ignore_king_safety=True)
        assert result == []

    def test_white_pawn_cannot_double_step_if_blocked(self):
        board = empty_board()
        board[6][4] = ("pawnw", "white")
        board[5][4] = ("pawnw", "black")
        result = list_valid_move(board, (6, 4), ignore_king_safety=True)
        assert result == []

    def test_black_pawn_cannot_double_step_if_blocked_but_can_one_step(self):
        board = empty_board()
        board[1][3] = ("pawnb", "black")
        board[3][3] = ("pawnw", "white")
        result = list_valid_move(board, (1, 3), ignore_king_safety=True)
        assert result == [(2, 3)]


class TestQueenListValidMove:
    def test_queen_free_space(self):
        board = empty_board()
        board[4][4] = ("queen", "white")
        result = list_valid_move(board, (4, 4), ignore_king_safety=True)
        assert result == [
            (5, 4),
            (6, 4),
            (7, 4),
            (4, 5),
            (4, 6),
            (4, 7),
            (3, 4),
            (2, 4),
            (1, 4),
            (0, 4),
            (4, 3),
            (4, 2),
            (4, 1),
            (4, 0),
            (5, 5),
            (6, 6),
            (7, 7),
            (3, 3),
            (2, 2),
            (1, 1),
            (0, 0),
            (5, 3),
            (6, 2),
            (7, 1),
            (3, 5),
            (2, 6),
            (1, 7),
        ]

    def test_queen_blocked_by_own_pieces(self):
        board = empty_board()
        board[4][4] = ("queen", "white")
        board[6][4] = ("pawnw", "white")
        board[4][6] = ("pawnw", "white")
        board[6][6] = ("pawnw", "white")
        board[2][2] = ("pawnw", "white")
        result = list_valid_move(board, (4, 4), ignore_king_safety=True)
        assert (6, 4) not in result
        assert (4, 6) not in result
        assert (6, 6) not in result
        assert (2, 2) not in result
        assert (5, 4) in result
        assert (4, 5) in result
        assert (5, 5) in result
        assert (3, 3) in result

    def test_queen_can_capture_enemy(self):
        board = empty_board()
        board[4][4] = ("queen", "white")
        board[7][4] = ("pawnw", "white")
        board[0][4] = ("pawnb", "black")
        board[4][0] = ("pawnb", "black")
        board[1][1] = ("pawnb", "black")
        result = list_valid_move(board, (4, 4), ignore_king_safety=True)
        assert (0, 4) in result
        assert (4, 0) in result
        assert (1, 1) in result
        assert (7, 4) not in result
