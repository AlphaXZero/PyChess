"""
test for main.py
__author__ = Gvanderveen
__version__ = 0.1
"""

import main
import pytest


# @pytest.fixture
# def rand_width():
#     return np.random.randint(5, 20)


# @pytest.fixture
# def rand_height():
#     return np.random.randint(5, 20)


# @pytest.mark.loop(10)
# def test_init_empty_board(rand_width, rand_height):
#     board = main.init_board(rand_width, rand_height)
#     a, b = board.shape
#     assert b == rand_width
#     assert a == rand_height

"""
tets for main.py
__author__ = Gvanderveen
__version__ = 0.1
"""

import main
import pytest


# @pytest.fixture
# def rand_width():
#     return np.random.randint(5, 20)


# @pytest.fixture
# def rand_height():
#     return np.random.randint(5, 20)


# @pytest.mark.loop(10)
# def test_init_empty_board(rand_width, rand_height):
#     board = main.init_board(rand_width, rand_height)
#     a, b = board.shape
#     assert b == rand_width
#     assert a == rand_height


# j'utilise une class faire des catégories pour mes tests mais on peut enlever si c'est vraiment interdit les objets (:
class TestKnight:
    def test_knight_moves_center(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[3][3] = ("knight", "b")
        moves = main.list_valid_move(board, (3, 3))
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
        moves = main.list_valid_move(board, (3, 3))
        expected_moves = [(5, 2), (1, 4), (1, 2), (4, 5), (4, 1), (2, 5), (2, 1)]
        assert sorted(moves) == sorted(expected_moves)

    def test_knight_can_capture_enemy(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[3][3] = ("knight", "w")
        board[5][4] = ("pawnb", "b")
        moves = main.list_valid_move(board, (3, 3))
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
        moves = main.list_valid_move(board, (0, 0))
        expected_moves = [(2, 1), (1, 2)]
        assert sorted(moves) == sorted(expected_moves)

    def test_knight_outbound2(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[6][7] = ("knight", "w")
        moves = main.list_valid_move(board, (6, 7))
        expected_moves = [(4, 6), (7, 5), (5, 5)]
        assert sorted(moves) == sorted(expected_moves)


class TestRook:
    def test_rook_center(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][4] = ("rook", "w")
        moves = main.list_valid_move(board, (4, 4))
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
        board[4][6] = ("pawnw", "w")  # Alliée à droite
        board[2][4] = ("pawnw", "w")  # Alliée en haut

        expected_moves = [
            (3, 4),  # Vers le haut (avant l'alliée)
            (5, 4),
            (6, 4),
            (7, 4),  # Vers le bas
            (4, 3),
            (4, 2),
            (4, 1),
            (4, 0),  # Vers la gauche
            (4, 5),  # Vers la droite, avant l'alliée
        ]

        actual_moves = main.list_valid_move(board, (4, 4))
        assert sorted(actual_moves) == sorted(expected_moves)

    def test_rook_can_capture_enemies(self):
        board = [["00" for _ in range(8)] for _ in range(8)]
        board[4][4] = ("rook", "w")
        board[4][6] = ("pawnb", "b")  # Ennemi à droite
        board[1][4] = ("queen", "b")  # Ennemi en haut

        expected_moves = [
            (3, 4),
            (2, 4),
            (1, 4),  # Monte jusqu'à l'ennemi
            (5, 4),
            (6, 4),
            (7, 4),  # Vers le bas
            (4, 3),
            (4, 2),
            (4, 1),
            (4, 0),  # Vers la gauche
            (4, 5),
            (4, 6),  # Jusqu'à l'ennemi à droite
        ]

        actual_moves = main.list_valid_move(board, (4, 4))
        assert sorted(actual_moves) == sorted(expected_moves)
