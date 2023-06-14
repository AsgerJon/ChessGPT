"""KingMove specifies an enum for one-step moves. These do not apply to pawn,
knight and king."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
from typing import Never, Optional

from icecream import ic
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError

from visualchess import Square

ic.configureOutput(includeContext=True)


class PieceMove(Enum):
  """KingMove enum"""
  UP = (0, 1)
  DOWN = (0, -1)
  LEFT = (-1, 0)
  RIGHT = (1, 0)
  UPRIGHT = (1, 1)
  UPLEFT = (-1, 1)
  DOWNLEFT = (-1, -1)
  DOWNRIGHT = (1, -1)

  Knight30 = (1, 2)
  Knight60 = (2, 1)
  Knight120 = (2, -1)
  Knight150 = (1, -2)
  Knight210 = (-1, -2)
  Knight240 = (-2, -1)
  Knight300 = (-2, 1)
  Knight330 = (-1, 2)

  @classmethod
  def getKingMoves(cls) -> list[PieceMove]:
    """Getter-function for the list of king moves"""
    return [cls.UP, cls.LEFT, cls.DOWN, cls.RIGHT, cls.UPRIGHT, cls.UPLEFT,
            cls.DOWNLEFT, cls.DOWNRIGHT]

  @classmethod
  def getKnightMoves(cls) -> list[PieceMove]:
    """Getter-function for the knight moves"""
    return [cls.Knight30, cls.Knight60, cls.Knight120, cls.Knight150,
            cls.Knight210, cls.Knight240, cls.Knight300, cls.Knight330, ]

  @classmethod
  def getRookMoves(cls) -> list[PieceMove]:
    """Getter-function for the Rook moves"""
    return [cls.UP, cls.DOWN, cls.LEFT, cls.RIGHT]

  @classmethod
  def getBishopMoves(cls) -> list[PieceMove]:
    """Getter-function for the bishop moves"""
    return [cls.UPLEFT, cls.UPRIGHT, cls.DOWNLEFT, cls.DOWNRIGHT]

  def __add__(self, other: Square) -> Optional[Square]:
    """Offsets the given square if possible"""
    x, y = other.x + self.x, other.y + self.y
    if -1 < x < 8 and -1 < y < 8:
      return Square.fromInts(x, y)
    return None

  def __sub__(self, other: Square) -> Optional[Square]:
    """Offsets the given square if possible"""
    x, y = other.x() - self.x, other.y() - self.y
    if -1 < x < 8 and -1 < y < 8:
      return Square.fromInts(x, y)
    return None

  def __radd__(self, other: Square) -> Optional[Square]:
    """Offsets the given square if possible"""
    return self + other

  def __rsub__(self, other: Square) -> Optional[Square]:
    """Offsets the given square if possible"""
    return self - other

  def _getX(self) -> int:
    """Getter-function for horizontal move"""
    return self.value[0]

  def _getY(self) -> int:
    """Getter-function for vertical move"""
    return self.value[1]

  def _noSet(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('move')

  @classmethod
  def fromValue(cls, file: int, rank: int) -> PieceMove:
    """Finds the move matching the given values as integers"""
    for instance in cls:
      if instance.x == file and instance.y == rank:
        return instance
    raise KeyError

  def __invert__(self) -> PieceMove:
    """Inverts the move"""
    x, y = -self.x, -self.y
    return self.fromValue(x, y)

  x = property(_getX, _noSet, _noSet)
  y = property(_getX, _noSet, _noSet)

  def __str__(self) -> str:
    """String Representation"""
    board = [stringList('X, X, X, X, X, X, X') for _ in range(7)]
    board[3][3] = '0'
    board[3 + self.y][3 + self.x] = '1'
    return '\n'.join(['-'.join(rank) for rank in board])
