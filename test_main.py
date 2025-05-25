import pytest
import engine

VOID_CELL = engine.VOID_CELL


@pytest.fixture
def empty_board():
    return [[VOID_CELL for _ in range(8)] for _ in range(8)]


class TestKnightMoves:
    def test_knight_moves_center(self, empty_board):
        board = empty_board
        board[3][3] = ("knight", "white")
        expected = [(5, 4), (5, 2), (1, 4), (1, 2), (4, 5), (4, 1), (2, 5), (2, 1)]
        moves = engine.list_valid_move(board, (3, 3))
        assert sorted(moves) == sorted(expected)

    def test_knight_moves_corner(self, empty_board):
        board = empty_board
        board[0][0] = ("knight", "white")
        expected = [(2, 1), (1, 2)]
        moves = engine.list_valid_move(board, (0, 0))
        assert sorted(moves) == sorted(expected)

    def test_knight_moves_edge(self, empty_board):
        board = empty_board
        board[6][7] = ("knight", "white")
        expected = [(4, 6), (7, 5), (5, 5)]
        moves = engine.list_valid_move(board, (6, 7))
        assert sorted(moves) == sorted(expected)

    def test_knight_blocked_by_ally(self, empty_board):
        board = empty_board
        board[3][3] = ("knight", "white")
        board[5][4] = ("pawnw", "white")
        moves = engine.list_valid_move(board, (3, 3))
        assert (5, 4) not in moves

    def test_knight_can_capture_enemy(self, empty_board):
        board = empty_board
        board[3][3] = ("knight", "white")
        board[5][4] = ("pawnb", "black")
        moves = engine.list_valid_move(board, (3, 3))
        assert (5, 4) in moves


class TestRookMoves:
    def test_rook_center(self, empty_board):
        board = empty_board
        board[4][4] = ("rook", "white")
        expected = [(i, 4) for i in range(8) if i != 4] + [
            (4, i) for i in range(8) if i != 4
        ]
        moves = engine.list_valid_move(board, (4, 4))
        assert sorted(moves) == sorted(expected)

    def test_rook_blocked_by_ally(self, empty_board):
        board = empty_board
        board[4][4] = ("rook", "white")
        board[4][6] = ("pawnw", "white")
        expected = [
            (0, 4),
            (1, 4),
            (2, 4),
            (3, 4),
            (4, 0),
            (4, 1),
            (4, 2),
            (4, 3),
            (4, 5),
            (5, 4),
            (6, 4),
            (7, 4),
        ]
        moves = engine.list_valid_move(board, (4, 4))
        assert sorted(moves) == sorted(expected)

    def test_rook_can_capture_enemy(self, empty_board):
        board = empty_board
        board[4][4] = ("rook", "white")
        board[4][6] = ("pawnb", "black")
        moves = engine.list_valid_move(board, (4, 4))
        assert (4, 6) in moves

    def test_invalid_rook_move(self, empty_board):
        board = empty_board
        board[4][4] = ("rook", "white")
        assert engine.move_piece(board, 4, 4, 6, 6, "white") is None


class TestQueenMoves:
    def test_queen_can_capture(self, empty_board):
        board = empty_board
        board[4][4] = ("queen", "white")
        board[1][1] = ("queen", "black")
        moves = engine.list_valid_move(board, (4, 4))
        assert (1, 1) in moves


class TestPawnMoves:
    def test_black_pawn_promotion(self, empty_board):
        board = empty_board
        board[6][0] = ("pawnb", "black")
        engine.move_piece(board, 6, 0, 7, 0, "black")
        assert board[7][0] == ("queen", "black")

    def test_pawn_double_advance_blocked(self, empty_board):
        board = empty_board
        board[1][3] = ("pawnb", "black")
        board[2][3] = ("pawnw", "white")  # Bloque juste devant
        moves = engine.list_valid_move(board, (1, 3))
        assert (3, 3) not in moves and (2, 3) not in moves

    def test_pawn_blocked_cannot_advance(self, empty_board):
        board = empty_board
        board[6][4] = ("pawnw", "white")
        board[5][4] = ("knight", "black")
        moves = engine.list_valid_move(board, (6, 4))
        assert (5, 4) not in moves

    def test_pawnb_single_advance(self, empty_board):
        board = empty_board
        board[2][3] = ("pawnb", "black")
        expected = [(3, 3)]
        moves = engine.list_valid_move(board, (2, 3))
        assert sorted(moves) == sorted(expected)

    def test_pawnw_single_advance(self, empty_board):
        board = empty_board
        board[2][3] = ("pawnw", "white")
        expected = [(1, 3)]
        moves = engine.list_valid_move(board, (2, 3))
        assert sorted(moves) == sorted(expected)

    def test_pawnb_double_advance(self, empty_board):
        board = empty_board
        board[1][4] = ("pawnb", "black")
        expected = [(2, 4), (3, 4)]
        moves = engine.list_valid_move(board, (1, 4))
        assert sorted(moves) == sorted(expected)

    def test_pawnw_double_advance(self, empty_board):
        board = empty_board
        board[6][4] = ("pawnw", "white")
        expected = [(5, 4), (4, 4)]
        moves = engine.list_valid_move(board, (6, 4))
        assert sorted(moves) == sorted(expected)

    def test_pawn_promotion(self, empty_board):
        board = empty_board
        board[1][0] = ("pawnw", "white")
        engine.move_piece(board, 1, 0, 0, 0, "white")
        assert board[0][0] == ("queen", "white")

    def test_pawn_blocked_forward(self, empty_board):
        board = empty_board
        board[6][3] = ("pawnw", "white")
        board[5][3] = ("rook", "black")
        assert engine.move_piece(board, 6, 3, 5, 3, "white") is None

    def test_pawn_capture_diagonal(self, empty_board):
        board = empty_board
        board[6][3] = ("pawnw", "white")
        board[5][4] = ("rook", "black")
        result = engine.move_piece(board, 6, 3, 5, 4, "white")
        assert result[5][4] == ("pawnw", "white")
        assert result[6][3] == VOID_CELL

    def test_en_passant_capture_by_white(self, empty_board):
        board = empty_board
        board[1][5] = ("pawnb", "black")
        engine.move_piece(board, 1, 5, 3, 5, "black")
        board[3][4] = ("pawnw", "white")
        result = engine.move_piece(board, 3, 4, 2, 5, "white")
        assert result[2][5] == ("pawnw", "white")
        assert result[3][5] == VOID_CELL

    def test_en_passant_invalid_after_delay(self, empty_board):
        board = empty_board
        board[3][4] = ("pawnw", "white")
        board[3][5] = ("pawnb", "black")
        assert engine.move_piece(board, 3, 4, 2, 5, "white") is None


class TestMovePieceGeneral:
    def test_cannot_move_on_own_piece(self, empty_board):
        board = empty_board
        board[4][4] = ("rook", "white")
        board[4][6] = ("knight", "white")
        assert engine.move_piece(board, 4, 4, 4, 6, "white") is None

    def test_capture_opponent(self, empty_board):
        board = empty_board
        board[4][4] = ("rook", "white")
        board[4][7] = ("knight", "black")
        result = engine.move_piece(board, 4, 4, 4, 7, "white")
        assert result[4][7] == ("rook", "white")
        assert result[4][4] == VOID_CELL


class TestKingAndCheck:
    def test_king_cannot_move_into_check(self, empty_board):
        board = empty_board
        board[4][4] = ("king", "white")
        board[3][5] = ("rook", "black")
        # La case (4,5) est attaquée par la tour noire
        result = engine.move_piece(board, 4, 4, 4, 5, "white")
        assert result is None

    def test_king_cannot_capture_protected_piece(self, empty_board):
        board = empty_board
        board[4][4] = ("king", "white")
        board[3][5] = ("rook", "black")
        board[2][5] = ("rook", "black")  # Protège la tour noire
        result = engine.move_piece(board, 4, 4, 3, 5, "white")
        assert result is None

    def test_find_king_white(self, empty_board):
        board = empty_board
        board[7][4] = ("king", "white")
        assert engine.find_king(board, "white") == (7, 4)

    def test_find_king_none(self, empty_board):
        board = empty_board
        assert engine.find_king(board, "black") is None

    def test_check_by_rook(self, empty_board):
        board = empty_board
        board[0][0] = ("king", "black")
        board[0][7] = ("rook", "white")
        result = engine.is_check(board, (0, 0))
        assert (0, 7) in result

    def test_check_by_knight(self, empty_board):
        board = empty_board
        board[4][4] = ("king", "white")
        board[2][5] = ("knight", "black")
        result = engine.is_check(board, (4, 4))
        assert (2, 5) in result

    def test_no_check(self, empty_board):
        board = empty_board
        board[4][4] = ("king", "white")
        board[0][0] = ("rook", "black")
        assert engine.is_check(board, (4, 4)) == []

    def test_white_pawn_diagonal_check(self, empty_board):
        board = empty_board
        board[4][4] = ("king", "black")
        board[5][3] = ("pawnw", "white")
        result = engine.is_check(board, (4, 4))
        assert (5, 3) in result

    def test_black_pawn_diagonal_check(self, empty_board):
        board = empty_board
        board[4][4] = ("king", "white")
        board[3][3] = ("pawnb", "black")
        result = engine.is_check(board, (4, 4))
        assert (3, 3) in result

    def test_white_pawn_cannot_check_forward(self, empty_board):
        board = empty_board
        board[4][4] = ("king", "black")
        board[5][4] = ("pawnw", "white")
        result = engine.is_check(board, (4, 4))
        assert result == []

    def test_black_pawn_cannot_check_forward(self, empty_board):
        board = empty_board
        board[4][4] = ("king", "white")
        board[3][4] = ("pawnb", "black")
        result = engine.is_check(board, (4, 4))
        assert result == []

    def test_white_pawn_check_on_board_edge(self, empty_board):
        board = empty_board
        board[0][0] = ("king", "black")
        board[1][1] = ("pawnw", "white")
        result = engine.is_check(board, (0, 0))
        assert (1, 1) in result

    def test_black_pawn_check_on_board_edge(self, empty_board):
        board = empty_board
        board[7][7] = ("king", "white")
        board[6][6] = ("pawnb", "black")
        result = engine.is_check(board, (7, 7))
        assert (6, 6) in result

    def test_white_pawn_not_checking_straight(self, empty_board):
        board = empty_board
        board[4][4] = ("king", "black")
        board[5][4] = ("pawnw", "white")
        result = engine.is_check(board, (4, 4))
        assert result == []

    def test_black_pawn_not_checking_straight(self, empty_board):
        board = empty_board
        board[4][4] = ("king", "white")
        board[3][4] = ("pawnb", "black")
        result = engine.is_check(board, (4, 4))
        assert result == []


class TestIsCheckMat:
    def test_stalemate_not_checkmate(self, empty_board):
        board = empty_board
        # Roi noir en coin, roi blanc éloigné, dame blanche coupe les cases
        board[7][7] = ("king", "black")
        board[5][6] = ("queen", "white")
        board[5][5] = ("king", "white")
        # Le roi noir ne peut pas bouger mais il n'est pas en échec
        assert not engine.is_check_mat(board, (7, 7))

    def test_not_checkmate_alone(self, empty_board):
        board = empty_board
        board[7][4] = ("king", "white")
        assert not engine.is_check_mat(board, (7, 4))

    def test_simple_checkmate_backrank(self, empty_board):
        board = empty_board
        board[7][7] = ("king", "white")
        board[6][6] = ("queen", "black")
        board[6][7] = ("rook", "black")  # La fuite est coupée
        assert engine.is_check_mat(board, (7, 7))

    def test_not_checkmate_can_escape(self, empty_board):
        board = empty_board
        board[7][7] = ("king", "white")
        board[6][6] = ("rook", "black")
        assert not engine.is_check_mat(board, (7, 7))

    def test_not_checkmate_blocked_but_defended(self, empty_board):
        board = empty_board
        board[7][7] = ("king", "white")
        board[6][6] = ("rook", "black")
        board[6][7] = ("rook", "white")
        assert not engine.is_check_mat(board, (7, 7))

    def test_checkmate_corner_two_rooks(self, empty_board):
        board = empty_board
        board[0][0] = ("king", "black")
        board[0][1] = ("rook", "white")
        board[1][0] = ("rook", "white")
        board[1][1] = ("king", "white")  # Défend les tours
        assert engine.is_check_mat(board, (0, 0))

    def test_not_checkmate_stalemate(self, empty_board):
        board = empty_board
        board[7][7] = ("king", "black")
        board[6][6] = ("queen", "white")
        board[5][5] = ("king", "white")
        assert engine.is_check_mat(board, (7, 7))

    def test_checkmate_with_pawn(self, empty_board):
        board = empty_board
        board[7][7] = ("king", "black")
        board[6][6] = ("pawnw", "white")
        board[5][5] = ("king", "white")
        assert not engine.is_check_mat(board, (7, 7))

    def test_not_checkmate_king_can_capture(self, empty_board):
        board = empty_board
        board[7][6] = ("king", "black")
        board[6][6] = ("rook", "white")
        assert not engine.is_check_mat(board, (7, 6))
