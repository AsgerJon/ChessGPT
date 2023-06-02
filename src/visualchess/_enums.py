"""File and Rank enums"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import string
from enum import Enum
from typing import Optional, NoReturn

from PySide6.QtCore import QPointF, QRectF, QSizeF
from PySide6.QtGui import QPainter
from icecream import ic
from worktoy.core import plenty
from worktoy.parsing import maybeType, maybeTypes
from worktoy.typetools import TypeBag

from workstyle.styles import LightSquareStyle, DarkSquareStyle, BoardDims

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
    if self.value:
      return '%s' % self.name
    return 'NULL'

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

  def __matmul__(self, other: Rank) -> Shade:
    """Determines the shade of the squares at self and other"""
    return Shade.LIGHT if self.value % 2 == other.value % 2 else Shade.DARK


class Rank(Enum):
  """Enumx representing the ranks on a chessboard"""
  rank1 = 0
  rank2 = 1
  rank3 = 2
  rank4 = 3
  rank5 = 4
  rank6 = 5
  rank7 = 6
  rank8 = 7

  def __str__(self) -> str:
    """String Representation"""
    if self.value:
      return '%s' % (int(self.name.replace('rank', '')))
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


class IterMeta(type):

  def __init__(cls, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    cls.createAll()

  def __len__(cls) -> int:
    return len(cls.__instances__)

  def __iter__(cls) -> IterMeta:
    return cls

  def __next__(cls) -> object:
    return cls.__next__()


class Square(metaclass=IterMeta):
  """Instances of Squares represent squares on the chess board"""

  @staticmethod
  def fitSquareRect(rect: QRectF) -> QRectF:
    """Returns the largest square QRectF that fits in rect"""
    dim = min(rect.width(), rect.height())
    size = QSizeF(dim, dim)
    squareRect = QRectF(BoardDims.origin, size)
    squareRect.moveCenter(rect.center())
    return squareRect

  @staticmethod
  def fitSquareMarginsRect(rect: QRectF) -> QRectF:
    """Returns the largest square QRectF that fits in given rect with the
    style margins deducted"""
    marginLeft = BoardDims.marginLeft
    marginTop = BoardDims.marginTop
    marginRight = BoardDims.marginRight
    marginBottom = BoardDims.marginBottom
    rect.adjust(marginLeft, marginTop, -marginRight, -marginBottom)
    print(marginLeft, marginTop, -marginRight, -marginBottom)
    return Square.fitSquareRect(rect)

  __instances__ = []
  __index__ = 0

  @classmethod
  def getIndex(cls) -> int:
    """Getter-function for the index"""
    return cls.__index__

  @classmethod
  def setIndex(cls, index: int) -> NoReturn:
    """Setter-function for the index"""
    cls.__index__ = index

  @classmethod
  def incIndex(cls) -> NoReturn:
    """Incrementing index"""
    cls.__index__ += 1

  @classmethod
  def decIndex(cls) -> NoReturn:
    """Decrementing index"""
    cls.__index__ -= 1

  @classmethod
  def __len__(cls, ) -> int:
    """Iteration"""
    return len(cls.__instances__)

  @classmethod
  def __iter__(cls, ) -> type:
    """Iteration"""
    cls.__index__ = 0
    return cls

  @classmethod
  def __next__(cls) -> Square:
    """Iteration"""
    cls.incIndex()
    if cls.getIndex() > len(cls):
      raise StopIteration
    return cls.__instances__[cls.getIndex() - 1]

  @classmethod
  def createAll(cls, ) -> NoReturn:
    """Creates all instances"""
    for file in File:
      for rank in Rank:
        cls(file, rank, _root=True)

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
    for item in cls:
      if item.getFile() == file and item.getRank() == rank:
        return item

  @classmethod
  def __new__(cls, *args, **kwargs) -> Square:
    if not cls.__instances__ and not kwargs.get('_root', False):
      cls.createAll()
    if kwargs.get('_root', False):
      cunt = super().__new__(cls)
      cls.__instances__.append(cunt)
      return cunt
    if not cls.__instances__:
      cls.createAll()
    _file = maybeType(File, *args)
    _rank = maybeType(Rank, *args)
    if plenty(_file, _rank):
      for item in cls.__instances__:
        if item.getFile() == _file and item.getRank() == _rank:
          return item
      raise ValueError
    point = maybeTypes(QPointF, *args)
    rect = maybeTypes(QRectF, *args)
    if isinstance(point, QPointF) and isinstance(rect, QRectF):
      return cls.pointRect(point, rect)

  def __init__(self, *args, **_) -> None:
    self._file = maybeType(File, *args)
    self._rank = maybeType(Rank, *args)
    self._piece = None
    self._pieceColor = None

  def __str__(self) -> str:
    """String Representation"""
    return '%s%s' % (self._file, self._rank)

  def __repr__(self) -> str:
    """Code Representation"""
    words = [self.getFile().__repr__(), self.getRank().__repr__()]
    return 'Square(%s, %s)' % (*words,)

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
    top0, height = boardRect.top(), boardRect.height()
    left = left0 + int(self.getFile().value * (width / 8))
    top = top0 + int(self.getRank().value * (height / 8))
    size = QSizeF(width / 8, height / 8)
    return QRectF(QPointF(left, top), size)

  def applyPaint(self, painter: QPainter) -> NoReturn:
    """Applies self to given painter"""
    style = self.getShade().getStyle()
    style @ painter
    viewPort = painter.viewport()
    boardRect = self.fitSquareMarginsRect(viewPort)
    rect = self.rectOnBoard(boardRect)
    painter.drawRect(rect)
