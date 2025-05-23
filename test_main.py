"""
test for engine
__author__ = Gvanderveen
__version__ = 0.1
"""

import engine
import pytest


# j'utilise une class faire des catégories pour mes tests mais on peut enlever si c'est vraiment interdit les objets (:
class TestListValidMoveKnight:
    def test_knight_moves_center(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
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
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[3][3] = ("knight", "w")
        board[5][4] = ("pawnw", "w")
        moves = engine.list_valid_move(board, (3, 3))
        expected_moves = [(5, 2), (1, 4), (1, 2), (4, 5), (4, 1), (2, 5), (2, 1)]
        assert sorted(moves) == sorted(expected_moves)

    def test_knight_can_capture_enemy(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
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
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[0][0] = ("knight", "w")
        moves = engine.list_valid_move(board, (0, 0))
        expected_moves = [(2, 1), (1, 2)]
        assert sorted(moves) == sorted(expected_moves)

    def test_knight_outbound2(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[6][7] = ("knight", "w")
        moves = engine.list_valid_move(board, (6, 7))
        expected_moves = [(4, 6), (7, 5), (5, 5)]
        assert sorted(moves) == sorted(expected_moves)


class TestListValidMoveRook:
    def test_rook_center(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
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
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
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
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
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


class TestListValidMoveQueen:
    def test_queen_center_clear(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
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
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
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
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
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


class TestListValidMovePawn:
    def test_pawnb_basic(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[2][3] = ("pawnb", "black")
        actual_moves = engine.list_valid_move(board, (2, 3))
        expected_moves = [(3, 3)]
        assert sorted(actual_moves) == sorted(expected_moves)

    def test_pawnw_basic(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[2][3] = ("pawnw", "white")
        actual_moves = engine.list_valid_move(board, (2, 3))
        expected_moves = [(1, 3)]
        assert sorted(actual_moves) == sorted(expected_moves)

    def test_pawnb_never_moved(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[1][4] = ("pawnb", "black")
        actual_moves = engine.list_valid_move(board, (1, 4))
        expected_moves = [(2, 4), (3, 4)]
        assert sorted(actual_moves) == sorted(expected_moves)

    def test_pawnw_never_moved(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[6][4] = ("pawnw", "white")
        actual_moves = engine.list_valid_move(board, (6, 4))
        expected_moves = [(5, 4), (4, 4)]
        assert sorted(actual_moves) == sorted(expected_moves)

    def test_pawnw_promote(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[1][4] = ("pawnw", "white")
        engine.move_piece(board, 1, 4, 0, 4, "white")
        assert board[0][4] == ("queen", "white")

    def test_pawnb_promote(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[6][4] = ("pawnb", "black")
        engine.move_piece(board, 6, 4, 7, 4, "black")
        assert board[7][4] == ("queen", "black")


class TestMovePiece:
    def test_valid_rook_move(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("rook", "white")
        result = engine.move_piece(board, 4, 4, 4, 7, "white")
        assert result[4][7] == ("rook", "white")
        assert result[4][4] == ("0", "0")

    def test_invalid_rook_move_diagonal(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("rook", "white")
        result = engine.move_piece(board, 4, 4, 6, 6, "white")
        assert result == -1

    def test_valid_knight_move(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("knight", "white")
        result = engine.move_piece(board, 4, 4, 6, 5, "white")
        assert result[6][5] == ("knight", "white")
        assert result[4][4] == ("0", "0")

    def test_invalid_knight_move(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("knight", "white")
        result = engine.move_piece(board, 4, 4, 5, 5, "white")
        assert result == -1

    def test_pawn_initial_double_move(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[6][4] = ("pawnw", "white")
        result = engine.move_piece(board, 6, 4, 4, 4, "white")
        assert result[4][4] == ("pawnw", "white")
        assert result[6][4] == ("0", "0")

    def test_pawn_promotion(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[1][0] = ("pawnw", "white")
        engine.move_piece(board, 1, 0, 0, 0, "white")
        assert board[0][0] == ("queen", "white")

    def test_cannot_move_on_own_piece(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("rook", "white")
        board[4][6] = ("knight", "white")
        result = engine.move_piece(board, 4, 4, 4, 6, "white")
        assert result == -1

    def test_capture_opponent(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("rook", "white")
        board[4][7] = ("knight", "black")
        result = engine.move_piece(board, 4, 4, 4, 7, "white")
        assert result[4][7] == ("rook", "white")
        assert result[4][4] == ("0", "0")


class TestFindKing:
    def test_find_white_king(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[7][4] = ("king", "white")
        assert engine.find_king(board, "white") == (7, 4)

    def test_find_black_king(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[0][4] = ("king", "black")
        assert engine.find_king(board, "black") == (0, 4)

    def test_find_king_not_found(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        assert engine.find_king(board, "white") is None


class TestCheckCheck:
    def test_check_by_rook(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[0][0] = ("king", "black")
        board[0][7] = ("rook", "white")

        result = engine.check_check(board, (0, 0))
        assert (0, 7) in result
        assert len(result) == 1

    def test_check_by_bishop(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[2][2] = ("king", "black")
        board[0][0] = ("bihsop", "white")  # orthographe gardée comme dans ton code

        result = engine.check_check(board, (2, 2))
        assert (0, 0) in result
        assert len(result) == 1

    def test_check_by_queen(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "black")
        board[4][7] = ("queen", "white")

        result = engine.check_check(board, (4, 4))
        assert (4, 7) in result
        assert len(result) == 1

    def test_check_by_knight(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "white")
        board[2][5] = ("knight", "black")

        result = engine.check_check(board, (4, 4))
        assert (2, 5) in result
        assert len(result) == 1

    def test_no_check(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "white")
        board[0][0] = ("rook", "black")  # Pas en ligne directe

        result = engine.check_check(board, (4, 4))
        assert result == []

    def test_double_check(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "white")
        board[4][0] = ("rook", "black")
        board[7][7] = ("bihsop", "black")

        result = engine.check_check(board, (4, 4))
        assert (4, 0) in result
        assert (7, 7) in result
        assert len(result) == 2

    def test_white_pawn_checking_black_king_diagonal(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "black")
        board[5][3] = ("pawnw", "white")  # Peut capturer en diagonale

        result = engine.check_check(board, (4, 4))
        assert (5, 3) in result
        assert len(result) == 1

    def test_white_pawn_not_checking_black_king_forward(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "black")
        board[5][4] = ("pawnw", "white")  # Ne peut pas capturer droit devant

        result = engine.check_check(board, (4, 4))
        assert result == []

    def test_black_pawn_checking_white_king_diagonal(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "white")
        board[3][3] = ("pawnb", "black")  # Peut capturer en diagonale

        result = engine.check_check(board, (4, 4))
        assert (3, 3) in result
        assert len(result) == 1

    def test_black_pawn_not_checking_white_king_forward(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "white")
        board[3][4] = ("pawnb", "black")  # Ne peut pas capturer droit devant

        result = engine.check_check(board, (4, 4))
        assert result == []

    def test_white_pawn_diagonal_check(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "black")
        board[5][3] = ("pawnw", "white")  # attaque diagonale
        result = engine.check_check(board, (4, 4))
        assert (5, 3) in result

    def test_black_pawn_diagonal_check(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "white")
        board[3][3] = ("pawnb", "black")  # attaque diagonale
        result = engine.check_check(board, (4, 4))
        assert (3, 3) in result

    # ❌ Cas incorrects — pas de mise en échec
    def test_white_pawn_behind_king(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "black")
        board[3][4] = ("pawnw", "white")  # derrière le roi
        result = engine.check_check(board, (4, 4))
        assert result == []

    def test_black_pawn_behind_king(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "white")
        board[5][4] = ("pawnb", "black")  # derrière le roi
        result = engine.check_check(board, (4, 4))
        assert result == []

    def test_white_pawn_sideways_king(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "black")
        board[4][5] = ("pawnw", "white")  # à côté, mais pas en diagonale
        result = engine.check_check(board, (4, 4))
        assert result == []

    def test_black_pawn_sideways_king(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "white")
        board[4][3] = ("pawnb", "black")  # à côté, mais pas en diagonale
        result = engine.check_check(board, (4, 4))
        assert result == []

    def test_white_pawn_forward_but_blocked(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "black")
        board[5][4] = (
            "pawnw",
            "white",
        )  # juste devant — mais ne peut pas capturer droit
        result = engine.check_check(board, (4, 4))
        assert result == []

    def test_black_pawn_forward_but_blocked(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[4][4] = ("king", "white")
        board[3][4] = ("pawnb", "black")  # juste devant — ne capture pas droit
        result = engine.check_check(board, (4, 4))
        assert result == []

    # 🔁 Cas symétriques et bords de plateau
    def test_white_pawn_on_edge_can_check(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[0][0] = ("king", "black")
        board[1][1] = ("pawnw", "white")  # diagonale vers coin
        result = engine.check_check(board, (0, 0))
        assert (1, 1) in result

    def test_black_pawn_on_edge_can_check(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[7][7] = ("king", "white")
        board[6][6] = ("pawnb", "black")  # diagonale vers coin
        result = engine.check_check(board, (7, 7))
        assert (6, 6) in result

    def test_en_passant_capture_by_white(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[3][4] = ("pawnw", "white")  # pion blanc prêt à capturer
        board[3][5] = ("pawnb", "black")  # pion noir qui vient de bouger de 2 cases

        # Simuler l'historique de mouvement si nécessaire pour autoriser en passant
        # Ex: engine.last_move = ((1,5), (3,5))

        result = engine.move_piece(board, 3, 4, 2, 5, "white", en_passant_target=(3, 5))
        assert result[2][5] == ("pawnw", "white")
        assert result[3][5] == ("0", "0")  # pion noir capturé
        assert result[3][4] == ("0", "0")

    def test_en_passant_invalid_after_delay(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[3][4] = ("pawnw", "white")
        board[3][5] = ("pawnb", "black")

        # Pas d’en passant autorisé ici (trop tard)
        result = engine.move_piece(board, 3, 4, 2, 5, "white", en_passant_target=None)
        assert result == -1

    def test_white_pawn_promotion_to_queen(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[1][0] = ("pawnw", "white")

        result = engine.move_piece(board, 1, 0, 0, 0, "white")
        assert result[0][0] == ("queen", "white")
        assert result[1][0] == ("0", "0")

    def test_pawn_blocked_forward(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[6][3] = ("pawnw", "white")
        board[5][3] = ("rook", "black")  # une pièce bloque le pion

        result = engine.move_piece(board, 6, 3, 5, 3, "white")
        assert result == -1

    def test_pawn_cannot_capture_forward(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[6][3] = ("pawnw", "white")
        board[5][3] = ("rook", "black")  # pièce ennemie en avant

        result = engine.move_piece(board, 6, 3, 5, 3, "white")
        assert result == -1  # capture non autorisée vers l’avant

    def test_pawn_capture_diagonal(self):
        board = [[("0", "0") for _ in range(8)] for _ in range(8)]
        board[6][3] = ("pawnw", "white")
        board[5][4] = ("rook", "black")

        result = engine.move_piece(board, 6, 3, 5, 4, "white")
        assert result[5][4] == ("pawnw", "white")
        assert result[6][3] == ("0", "0")
