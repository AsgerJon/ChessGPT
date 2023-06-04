"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
import string

from PySide6.QtCore import QRectF, QSizeF, QPointF
from icecream import ic
from worktoy.typetools import TypeBag

from visualchess import Shade, fitSquareMarginsRect, fitSquareRect
from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from visualchess import Rank

ic.configureOutput(includeContext=True)


class File(Enum):
  """Enums representing the files on a chessboard"""
  A = 0
  B = 1
  C = 2
  D = 3
  E = 4
  F = 5
  G = 6
  H = 7

  def __str__(self) -> str:
    """String Representation"""
    return '%s' % self.name

  def __repr__(self) -> str:
    """Code Representation"""
    return 'File.%s' % (self.name)

  @classmethod
  def find(cls, index: TypeBag(int, str)) -> File:
    """Lookup function"""
    if isinstance(index, int):
      return cls._getFromInt(index)
    if isinstance(index, str):
      return cls._getFromStr(index)
    raise KeyError

  @classmethod
  def _getFromInt(cls, index: int) -> File:
    """Getter-function for instance at given index"""
    for file in File:
      if file.value == index:
        return file
    raise IndexError

  @classmethod
  def _getFromStr(cls, key: str) -> File:
    """Getter-function by string"""
    if len(key) - 1:
      raise KeyError
    chars = ['NULL', *string.ascii_lowercase[:8]]
    for (i, char) in enumerate(chars):
      if char == key.lower():
        return cls._getFromInt(i)
    raise KeyError

  @classmethod
  def byValue(cls, val: int) -> File:
    """Finds the file by value"""
    for file in cls:
      if file.value == val:
        return file

  def getLabelRects(self, viewPort: QRectF) -> tuple[QRectF, QRectF]:
    """Getter-function for the rectangle that would hold the label for
    this File when applied to the viewPort"""
    r = fitSquareMarginsRect(viewPort)
    b = fitSquareRect(viewPort)
    left0, top0, width, height = r.left(), r.top(), r.width(), r.height()
    s = width / 16 + height / 16
    upperTop, upperBottom = b.top(), r.top()
    lowerTop, lowerBottom = r.bottom(), b.bottom()
    left = int(r.left() + s * (1 + self.value))
    upperCorner = QPointF(left, upperTop)
    lowerCorner = QPointF(left, lowerTop)
    upperLabel = QRectF(upperCorner, QSizeF(s, upperTop - upperBottom))
    lowerLabel = QRectF(lowerCorner, QSizeF(s, lowerTop - lowerBottom))
    return (upperLabel, lowerLabel)

  def __matmul__(self, other: Rank) -> Shade:
    """Determines the shade of the squares at self and other"""
    return Shade.LIGHT if self.value % 2 == other.value % 2 else Shade.DARK
