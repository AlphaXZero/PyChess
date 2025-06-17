"""
draw_pieces.py

This module contains functions to draw chess pieces and board highlights on a tkinter Canvas.
Each function draws a specific chess piece or helper shapes at the given (x, y) board coordinates.

Constants:
    SIZE (int): The size of a single square on the chess board.
    LINE_SETTINGS (dict): Default line styling for piece outlines.
"""

from typing import Dict, Any, List, Tuple
import tkinter as tk

SIZE: int = 110
LINE_SETTINGS: Dict = {"width": 3}


def gp(percent: int) -> float:
    """
    Returns the pixel value corresponding to a percentage of the SIZE constant.

    Args:
        percent (int): The percentage of SIZE.

    Returns:
        float: The computed pixel value.
    """
    return SIZE * (percent / 100)


def draw_warn_circles(cell: Tuple[int, int], canvas: tk.Canvas) -> None:
    """
    Draws an orange warning circle on the given cell.

    Args:
        cell (Tuple[int, int]): (row, col) coordinates of the cell.
        canvas (tk.Canvas): The canvas to draw on.

    Returns:
        None
    """
    canvas.create_oval(
        (cell[1] * SIZE) + gp(6),
        (cell[0] * SIZE) + gp(6),
        (cell[1] * SIZE) + gp(94),
        (cell[0] * SIZE) + gp(94),
        outline="orange",
        width=4,
    )


def draw_help_circles(cells: List[Tuple[int, int]], canvas: tk.Canvas) -> None:
    """
    Draws blue help circles on a list of board coordinates.

    Args:
        coords (List[Tuple[int, int]]): List of (row, col) coordinates.
        canvas (tk.Canvas): The canvas to draw on.

    Returns:
        None
    """
    for cell in cells:
        canvas.create_oval(
            (cell[1] * SIZE) + gp(40),
            (cell[0] * SIZE) + gp(40),
            (cell[1] * SIZE) + gp(60),
            (cell[0] * SIZE) + gp(60),
            outline="blue",
            width=4,
        )


def draw_knight(x: int, y: int, settings: Dict[str, Any], canvas: tk.Canvas) -> None:
    """
    Draws a knight chess piece at the specified board position.

    Args:
        x (int): Column on the board.
        y (int): Row on the board.
        settings (Dict[str, Any]): Drawing settings (color, fill, etc.).
        canvas (tk.Canvas): The canvas to draw on.

    Returns:
        None
    """
    x, y = x * SIZE, y * SIZE
    # Rectangle for the nose
    canvas.create_rectangle(
        x + gp(20),
        y + gp(40),
        x + gp(90),
        y + gp(60),
        **settings,
    )
    # Triangle for the nose
    canvas.create_polygon(
        x + gp(20),
        y + gp(40),
        x + gp(68),
        y + gp(40),
        x + gp(70),
        y + gp(20),
        **settings,
    )
    # Rectangle for the body
    canvas.create_rectangle(
        x + gp(60),
        y + gp(20),
        x + gp(90),
        y + gp(90),
        **settings,
    )
    # Base
    canvas.create_rectangle(
        x + gp(40),
        y + gp(80),
        x + gp(90),
        y + gp(90),
        **settings,
    )
    # Triangle for the foot
    canvas.create_polygon(
        x + gp(40),
        y + gp(80),
        x + gp(70),
        y + gp(60),
        x + gp(70),
        y + gp(80),
        **settings,
    )
    # Rectangle for the ear
    canvas.create_rectangle(
        x + gp(60),
        y + gp(10),
        x + gp(80),
        y + gp(20),
        **settings,
    )
    # Lines for ear details
    canvas.create_line(x + gp(60), y + gp(10), x + gp(60), y + gp(24), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(10), x + gp(80), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(60), y + gp(10), x + gp(80), y + gp(10), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(20), x + gp(90), y + gp(20), **LINE_SETTINGS)
    # Body vertical line
    canvas.create_line(x + gp(90), y + gp(20), x + gp(90), y + gp(90), **LINE_SETTINGS)
    # Foot lines
    canvas.create_line(x + gp(40), y + gp(90), x + gp(90), y + gp(90), **LINE_SETTINGS)
    canvas.create_line(x + gp(40), y + gp(80), x + gp(40), y + gp(90), **LINE_SETTINGS)
    # Diagonal for foot
    canvas.create_line(x + gp(40), y + gp(80), x + gp(60), y + gp(65), **LINE_SETTINGS)
    # Middle left
    canvas.create_line(x + gp(60), y + gp(66), x + gp(60), y + gp(62), **LINE_SETTINGS)
    # Horizontal middle
    canvas.create_line(x + gp(20), y + gp(62), x + gp(60), y + gp(62), **LINE_SETTINGS)
    # Vertical nose
    canvas.create_line(x + gp(20), y + gp(62), x + gp(20), y + gp(40), **LINE_SETTINGS)
    # Diagonal nose
    canvas.create_line(x + gp(20), y + gp(40), x + gp(60), y + gp(23), **LINE_SETTINGS)
    # Eye (black circle)
    eye_settings = settings.copy()
    eye_settings["fill"] = "black"
    canvas.create_oval(x + gp(60), y + gp(30), x + gp(70), y + gp(40), **eye_settings)


def draw_rook(x: int, y: int, settings: Dict[str, Any], canvas: tk.Canvas) -> None:
    """
    Draws a rook chess piece at the specified board position.

    Args:
        x (int): Column on the board.
        y (int): Row on the board.
        settings (Dict[str, Any]): Drawing settings (color, fill, etc.).
        canvas (tk.Canvas): The canvas to draw on.

    Returns:
        None
    """
    x, y = x * SIZE, y * SIZE
    # Rectangle for the body
    canvas.create_rectangle(
        x + gp(30),
        y + gp(40),
        x + gp(70),
        y + gp(80),
        **settings,
    )
    # Rectangle for the top
    canvas.create_rectangle(
        x + gp(24),
        y + gp(20),
        x + gp(76),
        y + gp(40),
        **settings,
    )
    # Small rectangles for the battlements
    canvas.create_rectangle(
        x + gp(24),
        y + gp(10),
        x + gp(34),
        y + gp(20),
        **settings,
    )
    canvas.create_rectangle(
        x + gp(44),
        y + gp(10),
        x + gp(56),
        y + gp(20),
        **settings,
    )
    canvas.create_rectangle(
        x + gp(66),
        y + gp(10),
        x + gp(76),
        y + gp(20),
        **settings,
    )
    # Base
    base_settings = settings.copy()
    base_settings.update(
        {"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS.get("fill", "black")}
    )
    canvas.create_rectangle(
        x + gp(20),
        y + gp(70),
        x + gp(80),
        y + gp(90),
        **base_settings,
    )
    # Small lines on the base
    canvas.create_line(x + gp(20), y + gp(70), x + gp(30), y + gp(70), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(70), x + gp(70), y + gp(70), **LINE_SETTINGS)
    # Body lines
    canvas.create_line(x + gp(30), y + gp(70), x + gp(30), y + gp(40), **LINE_SETTINGS)
    canvas.create_line(x + gp(70), y + gp(70), x + gp(70), y + gp(40), **LINE_SETTINGS)
    # Small top lines
    canvas.create_line(x + gp(24), y + gp(40), x + gp(76), y + gp(40), **LINE_SETTINGS)
    canvas.create_line(x + gp(76), y + gp(40), x + gp(70), y + gp(40), **LINE_SETTINGS)
    # Sides
    canvas.create_line(x + gp(24), y + gp(40), x + gp(24), y + gp(10), **LINE_SETTINGS)
    canvas.create_line(x + gp(76), y + gp(40), x + gp(76), y + gp(10), **LINE_SETTINGS)
    # Small lines at the top
    canvas.create_line(x + gp(24), y + gp(10), x + gp(34), y + gp(10), **LINE_SETTINGS)
    canvas.create_line(x + gp(44), y + gp(10), x + gp(56), y + gp(10), **LINE_SETTINGS)
    canvas.create_line(x + gp(66), y + gp(10), x + gp(76), y + gp(10), **LINE_SETTINGS)
    # Small lines below the top
    canvas.create_line(x + gp(34), y + gp(20), x + gp(44), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(66), y + gp(20), x + gp(56), y + gp(20), **LINE_SETTINGS)
    # Small vertical lines
    canvas.create_line(x + gp(24), y + gp(10), x + gp(24), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(34), y + gp(10), x + gp(34), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(44), y + gp(10), x + gp(44), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(56), y + gp(10), x + gp(56), y + gp(20), **LINE_SETTINGS)
    canvas.create_line(x + gp(66), y + gp(10), x + gp(66), y + gp(20), **LINE_SETTINGS)


def draw_pawn(x: int, y: int, settings: Dict[str, Any], canvas: tk.Canvas) -> None:
    """
    Draws a pawn chess piece at the specified board position.

    Args:
        x (int): Column on the board.
        y (int): Row on the board.
        settings (Dict[str, Any]): Drawing settings (color, fill, etc.).
        canvas (tk.Canvas): The canvas to draw on.

    Returns:
        None
    """
    x, y = x * SIZE, y * SIZE
    # Base
    canvas.create_rectangle(
        x + gp(20),
        y + gp(70),
        x + gp(80),
        y + gp(90),
        **settings,
    )
    # Trapezoid body
    canvas.create_polygon(
        x + gp(30),
        y + gp(70),
        x + gp(40),
        y + gp(50),
        x + gp(60),
        y + gp(50),
        x + gp(70),
        y + gp(70),
        **settings,
    )
    # Rectangle top
    top_settings = settings.copy()
    top_settings.update(
        {"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS.get("fill", "black")}
    )
    canvas.create_rectangle(
        x + gp(34), y + gp(30), x + gp(66), y + gp(50), **top_settings
    )
    # Round top
    canvas.create_oval(x + gp(40), y + gp(10), x + gp(60), y + gp(30), **top_settings)
    # Base lines
    canvas.create_line(x + gp(20), y + gp(90), x + gp(80), y + gp(90), **LINE_SETTINGS)
    canvas.create_line(x + gp(20), y + gp(90), x + gp(20), y + gp(70), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(90), x + gp(80), y + gp(70), **LINE_SETTINGS)
    # Upper base lines
    canvas.create_line(x + gp(80), y + gp(70), x + gp(70), y + gp(70), **LINE_SETTINGS)
    canvas.create_line(x + gp(20), y + gp(70), x + gp(30), y + gp(70), **LINE_SETTINGS)
    # Side triangles
    canvas.create_line(x + gp(30), y + gp(70), x + gp(40), y + gp(50), **LINE_SETTINGS)
    canvas.create_line(x + gp(70), y + gp(70), x + gp(60), y + gp(50), **LINE_SETTINGS)


def draw_bishop(x: int, y: int, settings: Dict[str, Any], canvas: tk.Canvas) -> None:
    """
    Draws a bishop chess piece at the specified board position.

    Args:
        x (int): Column on the board.
        y (int): Row on the board.
        settings (Dict[str, Any]): Drawing settings (color, fill, etc.).
        canvas (tk.Canvas): The canvas to draw on.

    Returns:
        None
    """
    x, y = x * SIZE, y * SIZE
    bishop_settings = settings.copy()
    bishop_settings.update(
        {"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS.get("fill", "black")}
    )
    # Oval body
    canvas.create_oval(
        x + gp(35),
        y + gp(20),
        x + gp(65),
        y + gp(80),
        **bishop_settings,
    )
    # Round top
    canvas.create_oval(
        x + gp(46),
        y + gp(10),
        x + gp(54),
        y + gp(20),
        **bishop_settings,
    )
    # Base
    canvas.create_rectangle(
        x + gp(25),
        y + gp(75),
        x + gp(75),
        y + gp(90),
        **bishop_settings,
    )


def draw_queen(x: int, y: int, settings: Dict[str, Any], canvas: tk.Canvas) -> None:
    """
    Draws a queen chess piece at the specified board position.

    Args:
        x (int): Column on the board.
        y (int): Row on the board.
        settings (Dict[str, Any]): Drawing settings (color, fill, etc.).
        canvas (tk.Canvas): The canvas to draw on.

    Returns:
        None
    """
    x, y = x * SIZE, y * SIZE
    # Base
    canvas.create_rectangle(
        x + gp(10),
        y + gp(80),
        x + gp(90),
        y + gp(90),
        **settings,
    )
    # Large triangle
    canvas.create_polygon(
        x + gp(20),
        y + gp(80),
        x + gp(80),
        y + gp(80),
        x + gp(50),
        y + gp(40),
        **settings,
    )
    queen_settings = settings.copy()
    queen_settings.update(
        {"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS.get("fill", "black")}
    )
    # Small triangle
    canvas.create_polygon(
        x + gp(50),
        y + gp(44),
        x + gp(30),
        y + gp(20),
        x + gp(70),
        y + gp(20),
        **queen_settings,
    )
    # Round top
    canvas.create_oval(
        x + gp(46),
        y + gp(10),
        x + gp(54),
        y + gp(20),
        **queen_settings,
    )
    # Base lines
    canvas.create_line(x + gp(10), y + gp(90), x + gp(90), y + gp(90), **LINE_SETTINGS)
    canvas.create_line(x + gp(10), y + gp(90), x + gp(10), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(90), y + gp(90), x + gp(90), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(10), y + gp(80), x + gp(20), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(90), y + gp(80), x + gp(80), y + gp(80), **LINE_SETTINGS)
    # Triangle base
    canvas.create_line(x + gp(20), y + gp(80), x + gp(50), y + gp(44), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(80), x + gp(50), y + gp(44), **LINE_SETTINGS)


def draw_king(x: int, y: int, settings: Dict[str, Any], canvas: tk.Canvas) -> None:
    """
    Draws a king chess piece at the specified board position.

    Args:
        x (int): Column on the board.
        y (int): Row on the board.
        settings (Dict[str, Any]): Drawing settings (color, fill, etc.).
        canvas (tk.Canvas): The canvas to draw on.

    Returns:
        None
    """
    x, y = x * SIZE, y * SIZE
    # Base
    canvas.create_rectangle(
        x + gp(10),
        y + gp(80),
        x + gp(90),
        y + gp(90),
        **settings,
    )
    # Trapezoid
    canvas.create_polygon(
        x + gp(20),
        y + gp(80),
        x + gp(80),
        y + gp(80),
        x + gp(70),
        y + gp(50),
        x + gp(30),
        y + gp(50),
        **settings,
    )
    # Vertical top
    king_settings = settings.copy()
    king_settings.update(
        {"width": LINE_SETTINGS["width"], "outline": LINE_SETTINGS.get("fill", "black")}
    )
    canvas.create_rectangle(
        x + gp(46),
        y + gp(50),
        x + gp(54),
        y + gp(10),
        **king_settings,
    )
    # Horizontal top
    canvas.create_rectangle(
        x + gp(28),
        y + gp(24),
        x + gp(72),
        y + gp(28),
        **king_settings,
    )
    # Base lines
    canvas.create_line(x + gp(10), y + gp(90), x + gp(90), y + gp(90), **LINE_SETTINGS)
    canvas.create_line(x + gp(10), y + gp(90), x + gp(10), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(90), y + gp(90), x + gp(90), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(10), y + gp(80), x + gp(20), y + gp(80), **LINE_SETTINGS)
    canvas.create_line(x + gp(90), y + gp(80), x + gp(80), y + gp(80), **LINE_SETTINGS)
    # Trapezoid lines
    canvas.create_line(x + gp(20), y + gp(80), x + gp(30), y + gp(50), **LINE_SETTINGS)
    canvas.create_line(x + gp(80), y + gp(80), x + gp(70), y + gp(50), **LINE_SETTINGS)
    canvas.create_line(x + gp(30), y + gp(50), x + gp(70), y + gp(50), **LINE_SETTINGS)
