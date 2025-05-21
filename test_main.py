"""
test for engine
__author__ = Gvanderveen
__version__ = 0.1
"""

import engine
import pytest


# j'utilise une class faire des catégories pour mes tests mais on peut enlever si c'est vraiment interdit les objets (:
class TestKnight:
    def test_knight_moves_center(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[3][3] = ("knight", "b")
        moves = engine.list_valid_move(board, (3, 3))
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
        assert sorted(moves) == sorted(expected_moves)

    def test_knight_blocked_by_ally(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[3][3] = ("knight", "w")
        board[5][4] = ("pawnw", "w")
        moves = engine.list_valid_move(board, (3, 3))
        expected_moves = [(5, 2), (1, 4), (1, 2), (4, 5), (4, 1), (2, 5), (2, 1)]
        assert sorted(moves) == sorted(expected_moves)

    def test_knight_can_capture_enemy(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[3][3] = ("knight", "w")
        board[5][4] = ("pawnb", "b")
        moves = engine.list_valid_move(board, (3, 3))
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
        assert sorted(moves) == sorted(expected_moves)

    def test_knight_outbound(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[0][0] = ("knight", "w")
        moves = engine.list_valid_move(board, (0, 0))
        expected_moves = [(2, 1), (1, 2)]
        assert sorted(moves) == sorted(expected_moves)

    def test_knight_outbound2(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[6][7] = ("knight", "w")
        moves = engine.list_valid_move(board, (6, 7))
        expected_moves = [(4, 6), (7, 5), (5, 5)]
        assert sorted(moves) == sorted(expected_moves)


class TestRook:
    def test_rook_center(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][4] = ("rook", "w")
        moves = engine.list_valid_move(board, (4, 4))
        expected_moves = [
            (0, 4),
            (1, 4),
            (2, 4),
            (3, 4),
            (5, 4),
            (6, 4),
            (7, 4),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 5),
            (4, 6),
            (4, 7),
        ]
        assert sorted(moves) == sorted(expected_moves)

    def test_rook_blocked_by_allies(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][4] = ("rook", "w")
        board[4][6] = ("pawnw", "w")
        board[2][4] = ("pawnw", "w")
        expected_moves = [
            (3, 4),
            (5, 4),
            (6, 4),
            (7, 4),
            (4, 3),
            (4, 2),
            (4, 1),
            (4, 0),
            (4, 5),
        ]

        actual_moves = engine.list_valid_move(board, (4, 4))
        assert sorted(actual_moves) == sorted(expected_moves)

    def test_rook_can_capture_enemies(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][4] = ("rook", "w")
        board[4][6] = ("pawnb", "b")
        board[1][4] = ("queen", "b")

        expected_moves = [
            (3, 4),
            (2, 4),
            (1, 4),
            (5, 4),
            (6, 4),
            (7, 4),
            (4, 3),
            (4, 2),
            (4, 1),
            (4, 0),
            (4, 5),
            (4, 6),
        ]

        actual_moves = engine.list_valid_move(board, (4, 4))
        assert sorted(actual_moves) == sorted(expected_moves)


class TestQueen:
    def test_queen_center_clear(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][4] = ("queen", "w")
        expected_moves = [
            (0, 0),
            (0, 4),
            (1, 1),
            (1, 4),
            (1, 7),
            (2, 2),
            (2, 4),
            (2, 6),
            (3, 3),
            (3, 4),
            (3, 5),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 5),
            (4, 6),
            (4, 7),
            (5, 3),
            (5, 4),
            (5, 5),
            (6, 2),
            (6, 4),
            (6, 6),
            (7, 1),
            (7, 4),
            (7, 7),
        ]

        actual_moves = engine.list_valid_move(board, (4, 4))
        assert sorted(actual_moves) == sorted(expected_moves)

    def test_queen_blocked_by_allies(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][4] = ("queen", "w")
        board[4][1] = ("pawnw", "w")
        board[1][1] = ("queen", "w")
        expected_moves = [
            (0, 4),
            (1, 4),
            (1, 7),
            (2, 2),
            (2, 4),
            (2, 6),
            (3, 3),
            (3, 4),
            (3, 5),
            (4, 2),
            (4, 3),
            (4, 5),
            (4, 6),
            (4, 7),
            (5, 3),
            (5, 4),
            (5, 5),
            (6, 2),
            (6, 4),
            (6, 6),
            (7, 1),
            (7, 4),
            (7, 7),
        ]

        actual_moves = engine.list_valid_move(board, (4, 4))
        assert sorted(actual_moves) == sorted(expected_moves)

    def test_queen_can_capture_enemies(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][4] = ("queen", "w")
        board[4][1] = ("queen", "w")
        board[1][1] = ("queen", "b")

        expected_moves = [
            (0, 4),
            (1, 1),
            (1, 4),
            (1, 7),
            (2, 2),
            (2, 4),
            (2, 6),
            (3, 3),
            (3, 4),
            (3, 5),
            (4, 2),
            (4, 3),
            (4, 5),
            (4, 6),
            (4, 7),
            (5, 3),
            (5, 4),
            (5, 5),
            (6, 2),
            (6, 4),
            (6, 6),
            (7, 1),
            (7, 4),
            (7, 7),
        ]

        actual_moves = engine.list_valid_move(board, (4, 4))
        assert sorted(actual_moves) == sorted(expected_moves)


class TestPawn:
    def test_pawnb_basic(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[2][3] = ("pawnb", "black")
        actual_moves = engine.list_valid_move(board, (2, 3))
        expected_moves = [(3, 3)]
        assert sorted(actual_moves) == sorted(expected_moves)

    def test_pawnw_basic(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[2][3] = ("pawnw", "white")
        actual_moves = engine.list_valid_move(board, (2, 3))
        expected_moves = [(1, 3)]
        assert sorted(actual_moves) == sorted(expected_moves)

    def test_pawnb_never_moved(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[1][4] = ("pawnb", "black")
        actual_moves = engine.list_valid_move(board, (1, 4))
        expected_moves = [(2, 4), (3, 4)]
        assert sorted(actual_moves) == sorted(expected_moves)

    def test_pawnw_never_moved(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[6][4] = ("pawnw", "white")
        actual_moves = engine.list_valid_move(board, (6, 4))
        expected_moves = [(5, 4), (4, 4)]
        assert sorted(actual_moves) == sorted(expected_moves)

    def test_pawnw_promote(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[1][4] = ("pawnw", "white")
        engine.move_piece(board, 1, 4, 0, 4)
        assert board[0][4] == ("queen", "white")

    def test_pawnb_promote(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[6][4] = ("pawnb", "black")
        engine.move_piece(board, 6, 4, 7, 4)
        assert board[7][4] == ("queen", "black")


class TestMovePiece:
    def test_valid_rook_move(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][4] = ("rook", "white")
        result = engine.move_piece(board, 4, 4, 4, 7)
        assert result[4][7] == ("rook", "white")
        assert result[4][4] == "00"

    def test_invalid_rook_move_diagonal(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][4] = ("rook", "white")
        result = engine.move_piece(board, 4, 4, 6, 6)
        assert result == None

    def test_valid_knight_move(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][4] = ("knight", "white")
        result = engine.move_piece(board, 4, 4, 6, 5)
        assert result[6][5] == ("knight", "white")
        assert result[4][4] == "00"

    def test_invalid_knight_move(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][4] = ("knight", "white")
        result = engine.move_piece(board, 4, 4, 5, 5)
        assert result == None

    def test_pawn_initial_double_move(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[6][4] = ("pawnw", "white")
        result = engine.move_piece(board, 6, 4, 4, 4)
        assert result[4][4] == ("pawnw", "white")
        assert result[6][4] == "00"

    def test_pawn_promotion(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[1][0] = ("pawnw", "white")
        engine.move_piece(board, 1, 0, 0, 0)
        assert engine.get_piece(board, (0, 0)) == ("queen", "white")

    def test_cannot_move_on_own_piece(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][4] = ("rook", "white")
        board[4][6] = ("knight", "white")
        result = engine.move_piece(board, 4, 4, 4, 6)
        assert result == None

    def test_capture_opponent(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][4] = ("rook", "white")
        board[4][7] = ("knight", "black")
        result = engine.move_piece(board, 4, 4, 4, 7)
        assert result[4][7] == ("rook", "white")
        assert result[4][4] == "00"

class TestFindKing:
    def test_find_white_king(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[7][4] = ("king", "white")
        assert engine.find_king(board, "white") == (7, 4)

    def test_find_black_king(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[0][4] = ("king", "black")
        assert engine.find_king(board, "black") == (0, 4)

    def test_find_king_not_found(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        assert engine.find_king(board, "white") is None


class TestBasicFunc:
    def test_get_piece(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][1] = ("queen", "w")
        assert engine.get_piece(board, (4, 1)) == ("queen", "w")
