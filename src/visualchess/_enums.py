"""File and Rank enums"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import string
from enum import Enum
from typing import Optional, NoReturn

from PySide6.QtCore import QPointF, QRectF, QSizeF
from PySide6.QtGui import QPainter
from worktoy.core import plenty
from worktoy.parsing import maybeType, maybeTypes
from worktoy.typetools import TypeBag

from moreworktoy import InstanceIteration
from workstyle.styles import LightSquareStyle, DarkSquareStyle


class File(Enum):
  """Enums representing the files on a chessboard"""
  NULL = 0
  A = 1
  B = 2
  C = 3
  D = 4
  E = 5
  F = 6
  G = 7
  H = 8

  def __str__(self) -> str:
    """String Representation"""
    if self.value:
      return '%s' % self.name
    return 'NULL'

  @classmethod
  def find(cls, index: int | str) -> File:
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

  def __matmul__(self, other: Rank) -> Shade:
    """Determines the shade of the squares at self and other"""
    return Shade.LIGHT if self.value % 2 == other.value % 2 else Shade.DARK


class Rank(Enum):
  """Enumx representing the ranks on a chessboard"""
  NULL = 0
  rank0 = 1
  rank1 = 2
  rank2 = 3
  rank3 = 4
  rank4 = 5
  rank5 = 6
  rank6 = 7
  rank7 = 8

  def __str__(self) -> str:
    """String Representation"""
    if self.value:
      return '%s' % (int(self.name.replace('rank', '')) + 1)
    return 'NULL'

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

  def __matmul__(self, other: File) -> Shade:
    """Determines the shade of the squares at self and other"""
    return Shade.LIGHT if self.value % 2 == other.value % 2 else Shade.DARK


class Shade(Enum):
  """Enum for light and dark squares"""
  DARK = 0
  LIGHT = 1

  def __bool__(self) -> bool:
    """Light is True, and Dark is False"""
    return True if '%s' % self.name.lower() == 'light' else False

  def __eq__(self, other: Shade) -> bool:
    """Equality operator implementation"""
    return True if self is other else False

  def __str__(self) -> str:
    """String Representation"""
    return 'Light' if self else 'Dark'

  def __repr__(self) -> str:
    """Code Representation"""
    return 'Shade.%s' % ('%s' % self).upper()

  def getStyle(self) -> TypeBag(LightSquareStyle, DarkSquareStyle):
    """Style getter function"""
    return LightSquareStyle if self else DarkSquareStyle


class Square(InstanceIteration):
  """Instances of Squares represent squares on the chess board"""

  _instances = []
  _NULL = None
  __index__ = None

  @classmethod
  def getNull(cls) -> Square:
    """Getter-function for NULL instance"""
    if cls._NULL is None:
      cls._NULL = cls(_root=True)
    return cls._NULL

  @classmethod
  def createAll(cls, ) -> NoReturn:
    """Creates all instances"""
    files = [f for f in File if f.value]
    ranks = [r for r in Rank if r.value]
    for file in files:
      for rank in ranks:
        cls._instances.append(cls(file, rank, _root=True))

  @classmethod
  def pointRect(cls, point: QPointF, boardRect: QRectF) -> Optional[Square]:
    """Finds locates the square that would contain the point if the
    squares covered the given rectangles."""
    x0, y0 = point.x(), point.y()
    left, top = boardRect.left(), boardRect.top()
    right, bottom = boardRect.right(), boardRect.bottom()
    width, height = boardRect.width(), boardRect.height()
    if not (left < x0 < right and top < y0 < bottom):
      return None
    file = File.byValue(int((x0 - left) / width * 8))
    rank = Rank.byValue(int((bottom - y0) / height * 8))
    for item in cls._instances:
      if item.getFile() == file and item.getRank() == rank:
        return item
    return cls._NULL

  @classmethod
  def __new__(cls, *args, **kwargs) -> Square:
    if kwargs.get('_root', False):
      return super().__new__(cls)
    if not cls._instances:
      cls.createAll()
    _file = maybeType(File, *args)
    _rank = maybeType(Rank, *args)
    if plenty(_file, _rank):
      for item in cls._instances:
        if item.getFile() == _file and item.getRank() == _rank:
          return item
      raise ValueError
    point = maybeTypes(QPointF, *args)
    rect = maybeTypes(QRectF, *args)
    if isinstance(point, QPointF) and isinstance(rect, QRectF):
      return cls.pointRect(point, rect)
    return cls._NULL

  def __init__(self, *args, **kwargs) -> None:
    self._file = maybeType(File, *args)
    self._rank = maybeType(Rank, *args)
    self._piece = None
    self._pieceColor = None

  def getFile(self) -> File:
    """Getter-function for file"""
    if isinstance(self._file, File):
      return self._file
    raise TypeError

  def getRank(self) -> Rank:
    """Getter-function for rank"""
    if isinstance(self._rank, Rank):
      return self._rank
    raise TypeError

  def getShade(self) -> Shade:
    """Getter-function for the shade"""
    return self.getFile() @ self.getRank()

  def rectOnBoard(self, boardRect: QRectF) -> QRectF:
    """Transforms the square to its QRectF representation """
    left0, width = boardRect.left(), boardRect.width(),
    top0, height = boardRect.top0(), boardRect.height()
    left = left0 + int(self.getFile().value - 1 * (width / 8))
    top = top0 + int(self.getFile().value - 1 * (height / 8))
    size = QSizeF(width / 8, height / 8)
    return QRectF(QPointF(left, top), size)

  def applyPaint(self, painter: QPainter) -> NoReturn:
    """Applies self to given painter"""
    self.getShade().getStyle() @ painter
    viewPort = painter.viewport()
    rect = self.rectOnBoard(viewPort)
    painter.drawRect(rect)
