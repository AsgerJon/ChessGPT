"""The loadPiece function is responsible for loading images, in particular
chess pieces, to instances of QPixmap which may then be inserted by the
rest of the PySide6 widget framework"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from enum import IntEnum

from PIL import ImageQt, Image
from PySide6.QtGui import QPixmap
from icecream import ic

ic.configureOutput(includeContext=True)


class Piece(IntEnum):
  """The Piece enum defines the chess pieces"""
  KING = 0
  QUEEN = 1
  ROOK = 2
  BISHOP = 3
  KNIGHT = 4
  PAWN = 5

  def __str__(self) -> str:
    """String Representation"""
    return self.name.capitalize()

  def __repr__(self) -> str:
    """Code Representation"""
    return '%s.%s' % (self.__class__.__qualname__, self._name_)

  def __add__(self, other: ChessColor) -> str:
    """Returns the filename of the image combining this color and that
    piece type."""
    return '%s_%s.png' % (other.name.lower(), self.name.lower())


class ChessColor(IntEnum):
  """Enum for White and Black"""
  WHITE = 0
  BLACK = 1

  def __str__(self) -> str:
    """String Representation"""
    return self.name.capitalize()

  def __repr__(self) -> str:
    """Code Representation"""
    return '%s.%s' % (self.__class__.__qualname__, self._name_)

  def __add__(self, other: Piece) -> str:
    """Returns the filename of the image combining this color and that
    piece type."""
    return '%s_%s.png' % (self.name.lower(), other.name.lower())


def loadPiece(piece: Piece, color: ChessColor) -> QPixmap:
  """Loads the piece defined by piece and color"""
  _root = os.getenv('CHESSGPT')
  there = os.path.join('src', 'visualchess', 'chesspieces', 'images')
  name = piece + color
  filePath = os.path.join(_root, there, name)
  return QPixmap(filePath)
