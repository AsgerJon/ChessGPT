"""Instances of class Square represent a location on a chess board. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Never

from PySide6.QtCore import QRect, QRectF, QPointF
from icecream import ic
from worktoy.parsing import maybeType
from worktoy.typetools import TypeBag
from worktoy.waitaminute import ReadOnlyError, UnexpectedStateError

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
  NULL = (File.NULL, Rank.NULL)
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

  def getX(self, ) -> int:
    """Getter-function for the file number"""
    return self.value[0].value

  def getY(self, ) -> int:
    """Getter-function for the rank number"""
    return self.value[1].value

  def _noAcc(self, *_) -> Never:
    """Illegal accessor function"""
    raise ReadOnlyError()

  def _getFile(self) -> File:
    """Getter-function for file"""
    return self.value[0]

  def _getRank(self) -> Rank:
    """Getter-function for rank"""
    return self.value[1]

  def __bool__(self, ) -> bool:
    """The null square is False, other squares are True"""
    return False if self is Square.NULL else True

  def __eq__(self, other: Square) -> bool:
    """The null square is not equal to itself. Otherwise returns True when
    self and other are the same Square"""
    return True if self and other and self is other else False

  def __hash__(self) -> int:
    """Returns 8 times file plus rank"""
    return 8 * self.file.value + self.rank.value if self else -1

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
    if not (file and rank):
      return Square.NULL
    for square in Square:
      if square.value[0] == file and square.value[1] == rank:
        return square
    raise TypeError

  @classmethod
  def fromInts(cls, x: int, y: int) -> Square:
    """Returns the instance of matching ints"""
    file = File.fromValue(x)
    rank = Rank.fromValue(y)
    return cls.fromFileRank(file, rank)

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

  @classmethod
  def getKingSquares(cls) -> list[Square]:
    """Getter-function for squares where kings start"""
    white = Square.fromFileRank(File.E, Rank.rank1)
    black = Square.fromFileRank(File.E, Rank.rank8)
    return [white, black]

  def _guardSelfComparison(self, other: Square) -> bool:
    """Raises an error if self and other is in fact the same square"""
    if self is other:
      msg = """Comparing a square with itself is not supported. This 
      occurrence is an indication of a deeper problem with the code, which
      is the reason for this being considered an error."""
      raise UnexpectedStateError(msg)
    return True

  @classmethod
  def fromComplex(cls, complexArg: complex) -> Square:
    """Creates an instance of Square from complex"""
    return cls.fromInts(int(complexArg.real), int(complexArg.imag))

  def __add__(self, other: PieceMove | Square | complex | int) -> Square:
    """Finds the square that is 'other' from self."""
    if isinstance(other, complex):
      x, y = self.x + int(other.real), self.y + int(other.imag)
      return Square.fromInts(x, y)
    if isinstance(other, int):
      return Square.fromInts(self.x + other, self.y)
    return Square.fromInts(self.x + other.x, self.y + other.y)

  def __radd__(self, other: PieceMove | Square | complex | int) -> Square:
    """Allowing adding from the left."""
    return self + other

  #
  # def __sub__(self, other: PieceMove | Square | complex | int):
  #   """Implementation is the same as for addition with sign applied"""
  #   if isinstance(other, complex):
  #     x, y = self.x - int(other.real), self.y - int(other.imag)
  #     return Square.fromInts(x, y)
  #   if isinstance(other, int):
  #     return Square.fromInts(self.x - other, self.y)
  #   return Square.fromInts(self.x - other.x, self.y - other.y)
  #
  # def __rsub__(self, other: PieceMove | Square | complex | int) -> Square:
  #   """Allowing adding from the left."""
  #   if isinstance(other, Square):
  #     return other - self
  #   raise TypeError('Squares support only other squares for rsub')

  def __sub__(self, other: Square) -> int:
    """The differences between the squares is taken as the supremum length
    between them."""
    df = abs(self.file.value - other.file.value)
    dr = abs(self.rank.value - other.rank.value)
    return max(dr, df)

  def __mul__(self, other: Square) -> int:
    """The multiplication between the squares is taken as the supremum
    length between them"""
    df = abs(self.file.value - other.file.value)
    dr = abs(self.rank.value - other.rank.value)
    return min(dr, df)

  def __rshift__(self, other: Square) -> Square:
    """Returns the square that is one step nearer to other"""
    df = self.file.value - other.file.value
    dr = self.rank.value - other.rank.value
    if df and dr and abs(df) - abs(dr) or self is other:
      return Square.NULL  # Incompatible
    if df and not dr:
      step = int(df / abs(df))
      return Square.fromInts(self.file.value + step, self.rank.value)
    if not df and dr:
      step = int(dr / abs(dr))
      return Square.fromInts(self.file.value, self.rank.value + step)
    if abs(df) == abs(dr):
      stepX, stepY = int(df / abs(df)), int(dr / abs(dr))
      return Square.fromInts(self.file.value + stepX,
                             self.rank.value + stepY)

  def __pow__(self, other: Square) -> tuple[int, int]:
    """Returns the steps between self and other"""
    df = self.file.value - other.file.value
    dr = self.rank.value - other.rank.value
    if df and dr and abs(df) - abs(dr) or self is other:
      return (0, 0)  # Incompatible
    return (int(df / abs(df)), int(dr / abs(dr)))

  def _getRight(self) -> Square:
    """Getter-function for the square to the right of this square as seen
    from the white side"""
    return self + 1

  def _getInFront(self) -> Square:
    """Getter-function for the square in front of this square"""
    return self - 1j

  def _getLeft(self) -> Square:
    """Getter-function for the square to the left of this square"""
    return self - 1

  def _getBehind(self) -> Square:
    """Getter-function for the square behind this square"""
    return self + 1j

  x = property(getX, _noAcc, _noAcc)
  y = property(getY, _noAcc, _noAcc)
  file = property(_getFile, _noAcc, _noAcc)
  rank = property(_getRank, _noAcc, _noAcc)
  right = property(_getRight, _noAcc, _noAcc)
  front = property(_getInFront, _noAcc, _noAcc)
  left = property(_getLeft, _noAcc, _noAcc)
  behind = property(_getBehind, _noAcc, _noAcc)
