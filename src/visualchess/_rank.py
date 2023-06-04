"""Rank Enum class"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING
from PySide6.QtCore import QRectF, QPointF, QSizeF
from icecream import ic

from visualchess import Shade, fitSquareRect, fitSquareMarginsRect

if TYPE_CHECKING:
  from visualchess import File

ic.configureOutput(includeContext=True)


class Rank(Enum):
  """Enumx representing the ranks on a chessboard"""
  rank1 = 7 - 0
  rank2 = 7 - 1
  rank3 = 7 - 2
  rank4 = 7 - 3
  rank5 = 7 - 4
  rank6 = 7 - 5
  rank7 = 7 - 6
  rank8 = 7 - 7

  def __str__(self) -> str:
    """String Representation"""
    return '%s' % self.name[-1]

  def __repr__(self) -> str:
    """Code Representation"""
    return 'Rank.%s' % self.name

  @classmethod
  def find(cls, index: int | str) -> Rank:
    """Lookup function"""
    if isinstance(index, int):
      return cls._getFromInt(index)
    if isinstance(index, str):
      return cls._getFromStr(index)
    raise TypeError

  @classmethod
  def _getFromInt(cls, index: int) -> Rank:
    """Getter-function for instance at given index"""
    for rank in Rank:
      if rank.value == index:
        return rank
    raise IndexError

  @classmethod
  def _getFromStr(cls, key: str) -> Rank:
    """Getter-function by string"""
    if len(key) - 1:
      raise KeyError
    chars = ['%d' % i for i in range(9)]
    for (i, char) in enumerate(chars):
      if char == key:
        return cls._getFromInt(i)
    raise KeyError

  @classmethod
  def byValue(cls, val: int) -> Rank:
    """Finds the rank by value"""
    for rank in cls:
      if rank.value == val:
        return rank

  def getLabelRects(self, viewPort: QRectF) -> tuple[QRectF, QRectF]:
    """Getter-function for the rectangle that would hold the label for
    this Rank when applied to the viewPort"""
    r = fitSquareMarginsRect(viewPort)
    b = fitSquareRect(viewPort)
    left0, top0, width, height = r.left(), r.top(), r.width(), r.height()
    s = width / 16 + height / 16
    leftLeft, leftRight = b.left(), r.left()
    rightLeft, rightRight = r.right(), b.right()
    top = int(r.top() + s * (1 + self.value))
    leftCorner = QPointF(leftLeft, top)
    rightCorner = QPointF(rightLeft, top)
    leftLabel = QRectF(leftCorner, QSizeF(leftLeft - leftRight, s))
    rightLabel = QRectF(rightCorner, QSizeF(rightLeft - rightRight, s))
    return (leftLabel, rightLabel)

  def __matmul__(self, other: File) -> Shade:
    """Determines the shade of the squares at self and other"""
    return Shade.LIGHT if self.value % 2 == other.value % 2 else Shade.DARK
