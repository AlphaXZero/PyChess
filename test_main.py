import pytest
from engine import (
    list_valid_move,
    VOID_CELL,
    Board,
    HISTORY,
    move_piece,
    is_check,
    is_check_mat,
    is_stalemate,
    is_castling,
)


@pytest.fixture(autouse=True)
def reset_history():
    HISTORY.clear()


def empty_board() -> Board:
    return [[VOID_CELL for _ in range(8)] for _ in range(8)]


class TestListValidMove:
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
            expected_moves = [(i, 0) for i in range(1, 8)] + [
                (0, i) for i in range(1, 8)
            ]
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

    class TestKingListValidMove:
        def test_king_moves_center(self):
            board = empty_board()
            board[4][4] = ("king", "white")
            expected = [(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), (5, 5)]
            result = list_valid_move(board, (4, 4), ignore_king_safety=True)
            assert sorted(result) == sorted(expected)

        def test_pawn_cannot_move_if_king_in_check_but_can_capture(self):
            board = empty_board()
            board[7][4] = ("king", "white")
            board[5][4] = ("rook", "black")
            board[6][3] = ("pawnw", "white")
            result = list_valid_move(board, (6, 3), ignore_king_safety=False)
            assert result == [(5, 4)]

        def test_pawn_cannot_move_and_cannot_capture_because_king_still_checked(self):
            board = empty_board()
            board[7][4] = ("king", "white")
            board[4][4] = ("rook", "black")
            board[6][3] = ("pawnw", "white")
            board[5][2] = ("rook", "black")
            result = list_valid_move(board, (6, 3), ignore_king_safety=False)
            assert result == []

    class TestBishopListValidMove:
        def test_bishop_center_of_board(self):
            board = empty_board()
            board[4][4] = ("bishop", "white")
            expected_moves = [
                (3, 3),
                (2, 2),
                (1, 1),
                (0, 0),
                (3, 5),
                (2, 6),
                (1, 7),
                (5, 3),
                (6, 2),
                (7, 1),
                (5, 5),
                (6, 6),
                (7, 7),
            ]
            result = list_valid_move(board, (4, 4), ignore_king_safety=True)
            assert sorted(result) == sorted(expected_moves)

        def test_bishop_blocked_by_own_pieces(self):
            board = empty_board()
            board[4][4] = ("bishop", "white")
            board[2][2] = ("pawnw", "white")
            board[6][6] = ("pawnw", "white")
            expected_moves = [
                (3, 3),
                (3, 5),
                (2, 6),
                (1, 7),
                (5, 3),
                (6, 2),
                (7, 1),
                (5, 5),
            ]
            result = list_valid_move(board, (4, 4), ignore_king_safety=True)
            assert sorted(result) == sorted(expected_moves)
            assert (2, 2) not in result
            assert (6, 6) not in result

        def test_bishop_can_capture_enemy(self):
            board = empty_board()
            board[4][4] = ("bishop", "white")
            board[1][7] = ("pawnw", "black")
            board[7][1] = ("queen", "black")
            expected_moves = [
                (3, 3),
                (2, 2),
                (1, 1),
                (0, 0),
                (3, 5),
                (2, 6),
                (1, 7),
                (5, 3),
                (6, 2),
                (7, 1),
                (5, 5),
                (6, 6),
                (7, 7),
            ]
            result = list_valid_move(board, (4, 4), ignore_king_safety=True)
            assert (1, 7) in result
            assert (7, 1) in result
            assert sorted(result) == sorted(expected_moves)

        def test_bishop_on_corner(self):
            board = empty_board()
            board[0][0] = ("bishop", "white")
            expected_moves = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)]
            result = list_valid_move(board, (0, 0), ignore_king_safety=True)
            assert sorted(result) == sorted(expected_moves)

        def test_bishop_no_moves_when_blocked(self):
            board = empty_board()
            board[3][3] = ("bishop", "white")
            board[2][2] = ("pawnw", "white")
            board[2][4] = ("pawnw", "white")
            board[4][2] = ("pawnw", "white")
            board[4][4] = ("pawnw", "white")
            result = list_valid_move(board, (3, 3), ignore_king_safety=True)
            assert result == []

        def test_bishop_pinned_cannot_move(self):
            board = empty_board()
            board[7][1] = ("king", "white")
            board[4][1] = ("bishop", "white")
            board[2][1] = ("rook", "black")
            result = list_valid_move(board, (4, 1), ignore_king_safety=False)
            assert result == []


class TestMovePiece:
    def test_move_valid_knight(self):
        board = empty_board()
        board[0][0] = ("king", "black")
        board[0][2] = ("king", "white")
        board[4][4] = ("knight", "white")
        new_board = move_piece(board, 4, 4, 6, 5, "white")
        assert new_board is not None
        assert new_board[6][5] == ("knight", "white")
        assert new_board[4][4] == VOID_CELL

    def test_move_wrong_color(self):
        board = empty_board()
        board[0][0] = ("king", "black")
        board[0][2] = ("king", "white")
        board[4][4] = ("knight", "white")
        result = move_piece(board, 4, 4, 6, 5, "black")
        assert result is None

    def test_cannot_move_to_same_color(self):
        board = empty_board()
        board[0][0] = ("king", "black")
        board[0][2] = ("king", "white")
        board[4][4] = ("rook", "white")
        board[6][4] = ("pawnw", "white")
        result = move_piece(board, 4, 4, 6, 4, "white")
        assert result is None

    def test_move_invalid_destination(self):
        board = empty_board()
        board[0][0] = ("king", "black")
        board[0][2] = ("king", "white")
        board[4][4] = ("bishop", "white")
        result = move_piece(board, 4, 4, 4, 3, "white")
        assert result is None

    def test_capture_enemy_piece(self):
        board = empty_board()
        board[0][0] = ("king", "black")
        board[0][2] = ("king", "white")
        board[3][3] = ("rook", "white")
        board[3][7] = ("pawnw", "black")
        new_board = move_piece(board, 3, 3, 3, 7, "white")
        assert new_board is not None
        assert new_board[3][7] == ("rook", "white")
        assert new_board[3][3] == VOID_CELL

    def test_pawn_promotion(self):
        board = empty_board()
        board[0][0] = ("king", "black")
        board[0][2] = ("king", "white")
        board[1][7] = ("pawnw", "white")
        new_board = move_piece(board, 1, 7, 0, 7, "white")
        assert new_board is not None
        assert new_board[0][7][0] == "queen"
        assert new_board[0][7][1] == "white"

    def test_black_pawn_promotion(self):
        board = empty_board()
        board[0][0] = ("king", "black")
        board[0][2] = ("king", "white")
        board[6][7] = ("pawnb", "black")
        new_board = move_piece(board, 6, 7, 7, 7, "black")
        assert new_board is not None
        assert new_board[7][7][0] == "queen"
        assert new_board[7][7][1] == "black"

    def test_move_pawn_double_step(self):
        board = empty_board()
        board[0][0] = ("king", "black")
        board[0][2] = ("king", "white")
        board[6][3] = ("pawnw", "white")
        new_board = move_piece(board, 6, 3, 4, 3, "white")
        assert new_board is not None
        assert new_board[4][3] == ("pawnw", "white")
        assert new_board[6][3] == VOID_CELL

    def test_en_passant_capture(self):
        board = empty_board()
        board[0][0] = ("king", "black")
        board[0][2] = ("king", "white")
        board[3][4] = ("pawnb", "black")
        board[6][5] = ("pawnw", "white")
        move_piece(board, 6, 5, 4, 5, "white")
        new_board = move_piece(board, 3, 4, 4, 5, "black")
        assert new_board is not None
        assert new_board[4][5] == ("pawnb", "black")
        assert new_board[3][4] == VOID_CELL
        assert new_board[5][5] == VOID_CELL

    def test_illegal_move_does_not_update_board(self):
        board = empty_board()
        board[4][4] = ("rook", "white")
        result = move_piece(board, 4, 4, 5, 5, "white")  # Invalid for rook
        assert result is None
        assert board[4][4] == ("rook", "white")

    def test_move_with_king_safety(self):
        board = empty_board()
        board[7][4] = ("king", "white")
        board[5][4] = ("rook", "black")
        board[6][3] = ("pawnw", "white")
        valid = move_piece(board, 6, 3, 5, 4, "white")
        assert valid is not None
        assert valid[5][4] == ("pawnw", "white")
        assert valid[6][3] == VOID_CELL
        board = empty_board()
        board[7][4] = ("king", "white")
        board[5][4] = ("rook", "black")
        board[6][3] = ("pawnw", "white")
        invalid = move_piece(board, 6, 3, 5, 3, "white")
        assert invalid is None


class TestIsCheck:
    def test_king_not_in_check(self):
        board = empty_board()
        board[7][4] = ("king", "white")
        result = is_check(board, (7, 4))
        assert result == []

    def test_king_in_check_by_rook(self):
        board = empty_board()
        board[7][4] = ("king", "white")
        board[5][4] = ("rook", "black")
        result = is_check(board, (7, 4))
        assert (5, 4) in result
        assert len(result) == 1

    def test_king_in_check_by_multiple(self):
        board = empty_board()
        board[7][4] = ("king", "white")
        board[5][4] = ("rook", "black")
        board[6][3] = ("bishop", "black")
        result = is_check(board, (7, 4))
        assert (5, 4) in result
        assert (6, 3) in result
        assert len(result) == 2

    def test_king_in_check_by_knight(self):
        board = empty_board()
        board[4][4] = ("king", "white")
        board[2][5] = ("knight", "black")
        result = is_check(board, (4, 4))
        assert (2, 5) in result
        assert len(result) == 1


class TestIsCheckMat:
    def test_king_not_checked_but_cant_move(self):
        board = empty_board()
        board[7][7] = ("king", "white")
        board[1][1] = ("king", "black")
        board[0][1] = ("pawnb", "black")
        board[0][0] = ("pawnb", "black")
        board[0][2] = ("pawnb", "black")
        board[1][0] = ("pawnb", "black")
        board[1][2] = ("pawnb", "black")
        board[2][0] = ("pawnb", "black")
        board[2][1] = ("pawnb", "black")
        board[2][2] = ("pawnb", "black")
        assert not is_check_mat(board, (1, 1))

    def test_pawn_can_block_check_mate(self):
        board = empty_board()
        board[4][4] = ("king", "white")
        board[3][0] = ("rook", "black")
        board[5][0] = ("rook", "black")
        board[4][0] = ("rook", "black")
        board[5][1] = ("pawnw", "white")
        assert not is_check_mat(board, (4, 4))

    def test_king_in_double_rook_checkmate(self):
        board = empty_board()
        board[7][7] = ("king", "white")
        board[0][0] = ("king", "black")
        board[6][5] = ("rook", "black")
        board[7][1] = ("rook", "black")
        assert is_check_mat(board, (7, 7))

    def test_king_can_escape(self):
        board = empty_board()
        board[4][4] = ("king", "white")
        board[2][5] = ("knight", "black")
        assert not is_check_mat(board, (4, 4))


class TestIsStalemate:
    def test_not_stalemate_if_in_check(self):
        board = empty_board()
        board[7][4] = ("king", "white")
        board[5][4] = ("rook", "black")
        assert not is_stalemate(board, (7, 4))

    def test_not_stalemate_if_moves_available(self):
        board = empty_board()
        board[4][4] = ("king", "white")
        board[2][5] = ("knight", "black")
        assert not is_stalemate(board, (4, 4))

    def test_stalemate_position(self):
        board = empty_board()
        board[0][0] = ("king", "white")
        board[2][1] = ("queen", "black")
        board[1][2] = ("king", "black")
        assert is_stalemate(board, (0, 0))


class TestIsCastling:
    def test_black_king_can_castle_both_side_white_king_cant_castle(self):
        board = empty_board()
        board[7][0] = ("rook", "white")
        board[7][3] = ("king", "white")
        board[7][1] = ("pawn", "white")
        board[0][0] = ("rook", "black")
        board[0][4] = ("king", "black")
        board[0][7] = ("rook", "black")
        assert is_castling(board, "white") == []
        assert is_castling(board, "black") == ["left", "right"]

    def test_black_king_cant_castle_because_moved_white_can_castle_left(self):
        board = empty_board()
        board[7][0] = ("rook", "white")
        board[7][3] = ("king", "white")
        board[7][1] = ("pawnw", "white")
        board[0][0] = ("rook", "black")
        board[0][4] = ("king", "black")
        board[0][7] = ("rook", "black")
        board = move_piece(board, 7, 1, 6, 1, "white")
        board = move_piece(board, 0, 4, 0, 3, "black")
        board = move_piece(board, 6, 1, 5, 1, "white")
        board = move_piece(board, 0, 3, 0, 4, "black")
        assert is_castling(board, "white") == ["left"]
        assert is_castling(board, "black") == []

    def test_white_cant_castle_left_because_rook_moved(self):
        board = empty_board()
        board[7][0] = ("rook", "white")
        board[7][3] = ("king", "white")
        board[7][1] = ("pawnw", "white")
        board[0][0] = ("rook", "black")
        board[0][4] = ("king", "black")
        board[0][7] = ("rook", "black")
        board = move_piece(board, 7, 1, 6, 1, "white")
        board = move_piece(board, 0, 4, 0, 3, "black")
        board = move_piece(board, 6, 1, 5, 1, "white")
        board = move_piece(board, 0, 3, 0, 4, "black")
        board = move_piece(board, 7, 0, 6, 0, "white")
        board = move_piece(board, 0, 4, 0, 3, "black")
        board = move_piece(board, 6, 0, 7, 0, "white")
        assert is_castling(board, "white") == []
