"""Instances of class Square represent a location on a chess board. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
import os
from typing import TYPE_CHECKING, Never, Optional

from PySide6.QtCore import QRect, QRectF, QPointF
from icecream import ic
from worktoy.parsing import maybeType, extractArg
from worktoy.stringtools import stringList
from worktoy.typetools import TypeBag
from worktoy.waitaminute import ReadOnlyError, UnexpectedStateError

from moreworktoy import ArgumentError
from visualchess import File, Rank, PieceMove

if TYPE_CHECKING:
  from visualchess import Widget

ic.configureOutput(includeContext=True)

Rect = TypeBag(QRectF, QRect)


def guardRect(boardRect: Rect) -> QRectF:
  """Applies type guarding"""
  if isinstance(boardRect, QRect):
    boardRect = boardRect.toRectF()
  if not isinstance(boardRect, QRectF):
    raise TypeError
  return boardRect


class Square(Enum):
  """Enum for the chess board squares"""
  A1 = (File.A, Rank.rank1)
  A2 = (File.A, Rank.rank2)
  A3 = (File.A, Rank.rank3)
  A4 = (File.A, Rank.rank4)
  A5 = (File.A, Rank.rank5)
  A6 = (File.A, Rank.rank6)
  A7 = (File.A, Rank.rank7)
  A8 = (File.A, Rank.rank8)
  B1 = (File.B, Rank.rank1)
  B2 = (File.B, Rank.rank2)
  B3 = (File.B, Rank.rank3)
  B4 = (File.B, Rank.rank4)
  B5 = (File.B, Rank.rank5)
  B6 = (File.B, Rank.rank6)
  B7 = (File.B, Rank.rank7)
  B8 = (File.B, Rank.rank8)
  C1 = (File.C, Rank.rank1)
  C2 = (File.C, Rank.rank2)
  C3 = (File.C, Rank.rank3)
  C4 = (File.C, Rank.rank4)
  C5 = (File.C, Rank.rank5)
  C6 = (File.C, Rank.rank6)
  C7 = (File.C, Rank.rank7)
  C8 = (File.C, Rank.rank8)
  D1 = (File.D, Rank.rank1)
  D2 = (File.D, Rank.rank2)
  D3 = (File.D, Rank.rank3)
  D4 = (File.D, Rank.rank4)
  D5 = (File.D, Rank.rank5)
  D6 = (File.D, Rank.rank6)
  D7 = (File.D, Rank.rank7)
  D8 = (File.D, Rank.rank8)
  E1 = (File.E, Rank.rank1)
  E2 = (File.E, Rank.rank2)
  E3 = (File.E, Rank.rank3)
  E4 = (File.E, Rank.rank4)
  E5 = (File.E, Rank.rank5)
  E6 = (File.E, Rank.rank6)
  E7 = (File.E, Rank.rank7)
  E8 = (File.E, Rank.rank8)
  F1 = (File.F, Rank.rank1)
  F2 = (File.F, Rank.rank2)
  F3 = (File.F, Rank.rank3)
  F4 = (File.F, Rank.rank4)
  F5 = (File.F, Rank.rank5)
  F6 = (File.F, Rank.rank6)
  F7 = (File.F, Rank.rank7)
  F8 = (File.F, Rank.rank8)
  G1 = (File.G, Rank.rank1)
  G2 = (File.G, Rank.rank2)
  G3 = (File.G, Rank.rank3)
  G4 = (File.G, Rank.rank4)
  G5 = (File.G, Rank.rank5)
  G6 = (File.G, Rank.rank6)
  G7 = (File.G, Rank.rank7)
  G8 = (File.G, Rank.rank8)
  H1 = (File.H, Rank.rank1)
  H2 = (File.H, Rank.rank2)
  H3 = (File.H, Rank.rank3)
  H4 = (File.H, Rank.rank4)
  H5 = (File.H, Rank.rank5)
  H6 = (File.H, Rank.rank6)
  H7 = (File.H, Rank.rank7)
  H8 = (File.H, Rank.rank8)

  @classmethod
  def parse(cls, *args, **kwargs) -> Square:
    """Parses the arguments to appropriate instance of Square"""
    keys = stringList('square, field, position')
    square, args, kwargs = extractArg(Square, keys, *args, **kwargs)
    if square is not None:
      if isinstance(square, Square):
        return square
    fileKeys = stringList('file, column, col, x')
    rankKeys = stringList('rank, row, y')
    file, args_, kwargs_ = extractArg(File, fileKeys, *args, **kwargs)
    if file is not None:
      rank, args_, kwargs_ = extractArg(Rank, rankKeys, *args_, **kwargs_)
      if rank is not None:
        if isinstance(file, File) and isinstance(rank, Rank):
          return cls.fromFileRank(file, rank)
    x, args_, kwargs_ = extractArg(int, fileKeys, *args, **kwargs)
    if x is not None:
      y, _, __ = extractArg(int, rankKeys, *args_, **kwargs_)
      if y is not None:
        if isinstance(x, int) and isinstance(y, int):
          return cls.fromInts(x, y)
    z, args_, kwargs_ = extractArg(complex, keys, *args, **kwargs)
    if z is not None:
      if isinstance(z, complex):
        return cls.fromInts(int(z.real), int(z.imag))
    raise ArgumentError('Unable to parse arguments to a valid instance!')

  def getX(self, ) -> int:
    """Getter-function for the file number"""
    return self.value[0].value

  def getY(self, ) -> int:
    """Getter-function for the rank number"""
    return self.value[1].value

  def _noSet(self, *_) -> Never:
    """Illegal accessor function"""
    raise ReadOnlyError()

  def _getFile(self) -> File:
    """Getter-function for file"""
    return self.value[0]

  def _getRank(self) -> Rank:
    """Getter-function for rank"""
    return self.value[1]

  def __matmul__(self, other: Rect) -> QRectF:
    """Given a board rectangle, this function returns a QRectF indicating
    the space this square should take up. Please note that this is the
    full rectangle, not including any gridlines or margins."""
    if isinstance(other, QRect):
      return self @ (other.toRectF())
    if isinstance(other, QRectF):
      return self._fitInRect(other)
    if isinstance(other, Widget):
      return self @ other.getBoardRect()

  def __rmatmul__(self, other: Rect) -> QRectF:
    """Support for right matmul"""
    return self @ other

  def _fitInRect(self, boardRect: Rect) -> QRectF:
    """Fits in rectangle"""
    boardRect = guardRect(boardRect)
    b = boardRect
    left0, top0, right0, bottom0 = b.left(), b.top(), b.right(), b.bottom()
    width, height = boardRect.width(), boardRect.height()
    left = left0 + self.x * width / 8
    right = right0 - (7 - self.x) * width / 8
    top = top0 + self.y * height / 8
    bottom = bottom0 - (7 - self.y) * height / 8
    leftTop = QPointF(left, top)
    rightBottom = QPointF(right, bottom)
    return QRectF(leftTop, rightBottom)

  @classmethod
  def fromFileRank(cls, file: File, rank: Rank) -> Square:
    """Returns the instance of matching file and rank"""
    for square in Square:
      if square.value[0] == file and square.value[1] == rank:
        return square

  @classmethod
  def fromInts(cls, x: int, y: int) -> Optional[Square]:
    """Returns the instance of matching ints"""
    if -1 < x < 8 and -1 < y < 8:
      file = File.fromValue(x)
      rank = Rank.fromValue(y)
      out = cls.fromFileRank(file, rank)
      return out

  @classmethod
  def fromStr(cls, code: str) -> Square:
    """Returns a square from short Name such as E4"""
    if len(code) != 2:
      raise ValueError()
    fileStr, rankStr = code[0], code[1]
    file = File.fromStr(fileStr)
    rank = Rank.fromStr(rankStr)
    return cls.fromFileRank(file, rank)

  @classmethod
  def fromPointRect(cls, *args) -> Square:
    """Finds the square that would contain given point if squares were
    distributed on given rect"""
    rect = maybeType(QRectF, *args)
    point = maybeType(QPointF, *args)
    if isinstance(rect, QRectF) and isinstance(point, QPointF):
      left0, top0 = rect.left(), rect.top()
      width, height = rect.width(), rect.height()
      x, y = point.x() - left0, point.y() - top0
      fileVal, rankVal = int(x / width * 8), int(y / height * 8)
      return cls.fromInts(fileVal, rankVal)
    else:
      raise TypeError

  @classmethod
  def getCorners(cls) -> list[Square]:
    """Getter-function for corners"""
    out = []
    for f in [File.A, File.H]:
      for r in [Rank.rank1, Rank.rank8]:
        out.append(cls.fromFileRank(f, r))
    return out

  # @classmethod
  # def getKingSquares(cls) -> list[Square]:
  #   """Getter-function for squares where kings start"""
  #   white = Square.fromFileRank(File.E, Rank.rank1)
  #   black = Square.fromFileRank(File.E, Rank.rank8)
  #   return [white, black]

  def _guardSelfComparison(self, other: Square) -> bool:
    """Raises an error if self and other is in fact the same square"""
    if self is other:
      msg = """Comparing a square with itself is not supported. This 
      occurrence is an indication of a deeper problem with the code, which
      is the reason for this being considered an error."""
      raise UnexpectedStateError(msg)
    return True

  def __add__(self, other: PieceMove) -> Square:
    """Returns the instance of Square that is 'other' away from self"""
    x = self.getX() + other.x
    y = self.getY() + other.y
    return self.fromInts(x, y)

  def __or__(self, other: Square) -> bool:
    """The pipe operator | is used to indicate that the squares are on the
    same file"""
    self._guardSelfComparison(other)
    return True if self.file == other.file else False

  def __rshift__(self, other: Square) -> bool:
    """Use of the right shift operator >> is taken to mean that the two
    squares would be connected along a right-directed diagonal. Please note
    that this is as seen from the player, which is the reverse of the
    direction of the inner logic because PySide6 and Qt has the vertical
    axis upside down.

    The computation compares the different between ranks and files. If
    they share a diagonal, the ratio between their differences in files
    and ranks will be 1 or 1-. Since the PySide6 is positive from top to
    down, a positive unit ratio means a left moving diagonal.
    """
    self._guardSelfComparison(other)
    df = self.file - other.file
    dr = self.rank - other.rank
    return False if df + dr else True

  def __lshift__(self, other: Square) -> bool:
    """Left shift << is implemented to test the left moving diagonal. See
    the docstring for the right shift above."""
    self._guardSelfComparison(other)
    df = self.file - other.file
    dr = self.rank - other.rank
    return True if df + dr else False

  def __sub__(self, other: Square) -> bool:
    """The subtraction operator - is taken to mean horizontal match"""
    self._guardSelfComparison(other)
    return True if self.rank == other.rank else False

  x = property(getX, _noSet, _noSet)
  y = property(getY, _noSet, _noSet)
  file = property(_getFile, _noSet, _noSet)
  rank = property(_getRank, _noSet, _noSet)
