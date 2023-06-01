"""The loadPiece function is responsible for loading images, in particular
chess pieces, to instances of QPixmap which may then be inserted by the
rest of the PySide6 widget framework"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from enum import IntEnum

from icecream import ic


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


class ChessColor(IntEnum):
  """Enum for White and Black"""
  WHITE = 0
  BLACK = 1


def loadPiece(piece: Piece, sideColor: ChessColor):
  """The loadPiece function is responsible for loading images, in particular
  chess pieces, to instances of QPixmap which may then be inserted by the
  rest of the PySide6 widget framework"""
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen

  ic(os.getcwd())
  ic(os.getenv('CHESSGPT'))
