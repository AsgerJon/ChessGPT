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


class Move(Enum):
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

  def getKingMoves(self) -> list[Move]:
    """Getter-function for the list of king moves"""
    out = [Move.UP, Move.LEFT, Move.DOWN, Move.RIGHT]
    return [*out, Move.UPRIGHT, Move.UPLEFT, Move.DOWNLEFT, Move.DOWNRIGHT, ]

  def getKnightMoves(self) -> list[Move]:
    """Getter-function for the knight moves"""
    return [Move.Knight30, Move.Knight60, Move.Knight120, Move.Knight150,
            Move.Knight210, Move.Knight240, Move.Knight300, Move.Knight330, ]

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
  def fromValue(cls, file: int, rank: int) -> Move:
    """Finds the move matching the given values as integers"""
    for instance in cls:
      if instance.x == file and instance.y == rank:
        return instance
    raise KeyError

  def __invert__(self) -> Move:
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
