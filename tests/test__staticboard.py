"""Testing staticBoard"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import unittest

from PySide6.QtGui import QColor

from visualchess import staticBoard


class ChessboardImageTestCase(unittest.TestCase):
  """Test case for the create_chessboard_image function."""

  def test_default_colors(self):
    """Test that the function generates a chessboard image with default
    colors."""
    image = staticBoard(600)
    self.assertEqual(image.width(), 600)
    self.assertEqual(image.height(), 600)

  def test_custom_colors(self):
    """Test that the function generates a chessboard image with custom
    colors."""
    square_color1 = QColor("blue")
    square_color2 = QColor("green")
    file_color = QColor("red")
    rank_color = QColor("yellow")
    image = create_chessboard_image(600, square_color1=square_color1,
                                    square_color2=square_color2,
                                    file_color=file_color,
                                    rank_color=rank_color)
    self.assertEqual(image.width(), 600)
    self.assertEqual(image.height(), 600)

  def test_custom_font(self):
    """Test that the function generates a chessboard image with a custom
    font."""
    font_name = "Courier"
    font_size = 20
    font = QFont(font_name, font_size)
    image = create_chessboard_image(600, font=font)
    self.assertEqual(image.width(), 600)
    self.assertEqual(image.height(), 600)

  def test_custom_font_and_colors(self):
    """Test that the function generates a chessboard image with custom
    font and colors."""
    font_name = "Helvetica"
    font_size = 24
    font = QFont(font_name, font_size)
    square_color1 = QColor("gray")
    square_color2 = QColor("lightGray")
    file_color = QColor("black")
    rank_color = QColor("darkGray")
    image = create_chessboard_image(600,
                                    font=font,
                                    square_color1=square_color1,
                                    square_color2=square_color2,
                                    file_color=file_color,
                                    rank_color=rank_color)
    self.assertEqual(image.width(), 600)
    self.assertEqual(image.height(), 600)


if __name__ == "__main__":
  unittest.main()
