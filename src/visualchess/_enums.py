"""Enums are necessary to have consistency across the modules"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum, Enum
import os
from typing import NoReturn, Never, TYPE_CHECKING

from PySide6.QtCore import QRect, QRectF, QPointF
from PySide6.QtGui import QPixmap, QColor, QCursor
from icecream import ic
from worktoy.parsing import maybeType
from worktoy.stringtools import stringList
from worktoy.typetools import TypeBag
from worktoy.waitaminute import ReadOnlyError, UnexpectedStateError

from visualchess.chesspieces import initialPosition

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


_pieces = stringList('King, Queen, Rook, Bishop, Knight, Pawn')
_colors = stringList('white, black')


class ChessPiece(IntEnum):
  """Chess piece enum"""
  BLACK_KING = 6
  BLACK_QUEEN = 5
  BLACK_ROOK = 4
  BLACK_BISHOP = 3
  BLACK_KNIGHT = 2
  BLACK_PAWN = 1
  EMPTY = 0
  WHITE_PAWN = -1
  WHITE_KNIGHT = -2
  WHITE_BISHOP = -3
  WHITE_ROOK = -4
  WHITE_QUEEN = -5
  WHITE_KING = -6

  def getPixmap(self) -> QPixmap:
    """Generates QPixmap representation of the piece"""
    if not self.value:
      pix = QPixmap(64, 64)
      pix.fill(QColor(0, 0, 0, 0, ))
      return pix
    root = os.getenv('CHESSGPT')
    there = stringList('src, visualchess, chesspieces, images')
    os.path.join(root, *there)
    fileName = '%s.png' % self.name.lower()
    filePath = os.path.join(root, *there, fileName)
    return QPixmap(filePath)

  def getCursor(self, point: QPointF = None) -> QCursor:
    """Generates a QCursor instance at the given point as hot. Please
    note, that passing a point to this function will create a QCursor
    whose hot point is that point. The point defaults to origin which is
    likely safe for most situations."""
    pix = self.getPixmap()
    x, y = -1, -1
    if isinstance(point, QPointF):
      x, y = point.x(), point.y()
    return QCursor(pix, hotX=x, hotY=y)

  def __rshift__(self, other: Widget) -> Widget:
    """Creates an instance of QCursor representing the piece and applies
    it to other widget. """

  def getColor(self) -> str:
    """Getter-function for color"""
    if not self.value:
      return 'empty'
    if self.value < 0:
      return 'white'
    return 'black'

  def setColor(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('color', 'set')

  def getPiece(self) -> str:
    """Getter-function for piece"""
    if not self.value:
      return 'empty'
    return self.name.split('_')[-1]

  def setPiece(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('piece', 'set')

  color = property(getColor, setColor, setColor)
  piece = property(getPiece, setPiece, setPiece)

  @classmethod
  def fromColorPiece(cls, color: str, piece: str) -> ChessPiece:
    """Finds the piece given the color and piece type"""
    for chessPiece in ChessPiece:
      if chessPiece.value:
        if chessPiece.getPiece().lower() == piece:
          if chessPiece.getColor().lower() == color:
            return chessPiece

  def __bool__(self) -> bool:
    """EMPTY is False, all other instances are True"""
    return False if self is self.EMPTY else True

  def __eq__(self, other: ChessPiece) -> bool:
    """Pieces must have same color and piece to be equal. EMPTY is not
    equal to any, not even itself."""
    if not (self and other):
      return False
    if self.color != other.color:
      return False
    if self.piece != other.piece:
      return False
    return True


class File(IntEnum):
  """File enum"""
  A = 0
  B = 1
  C = 2
  D = 3
  E = 4
  F = 5
  G = 6
  H = 7

  @classmethod
  def fromValue(cls, x: int) -> File:
    """Finds the matching value"""
    for file in File:
      if file.value == x:
        return file
    raise TypeError

  @classmethod
  def fromStr(cls, name: str) -> File:
    """Finds the file based on str name"""
    for file in File:
      if file.name == name:
        return file
    raise TypeError


class Rank(IntEnum):
  """Rank enum"""
  rank1 = 7 - 0
  rank2 = 7 - 1
  rank3 = 7 - 2
  rank4 = 7 - 3
  rank5 = 7 - 4
  rank6 = 7 - 5
  rank7 = 7 - 6
  rank8 = 7 - 7

  @classmethod
  def fromValue(cls, y: int) -> Rank:
    """Finds the matching value"""
    for rank in Rank:
      if rank.value == y:
        return rank
    raise TypeError

  @classmethod
  def fromStr(cls, name: str) -> Rank:
    """Finds the rank based on str name"""
    for rank in Rank:
      if rank.name[-1] == name[-1]:
        return rank
    raise TypeError


class Square(Enum):
  """Square Enum"""
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

  def setX(self, *_) -> NoReturn:
    """Illegal setter-function"""
    raise ReadOnlyError()

  def getY(self, ) -> int:
    """Getter-function for the rank number"""
    return self.value[1].value

  def setY(self, *_) -> NoReturn:
    """Illegal setter-function"""
    raise ReadOnlyError()

  x = property(getX, setX, setX)
  y = property(getY, setY, setY)

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


class BoardState:
  """BoardState represents a chess board with each squared occupied by a
  member, possibly the empty one, of the Piece Enum."""

  @classmethod
  def InitialPosition(cls) -> BoardState:
    """Creates an instance with piece at the starting position"""
    instance = cls()
    for line in initialPosition:
      square = Square.fromStr(line[0])
      piece = ChessPiece.fromColorPiece(line[1], line[2])
      instance[square] = piece
    return instance

  def __init__(self, *args, **kwargs) -> None:
    self._contents = {s: ChessPiece.EMPTY for s in Square}

  def __getitem__(self, square: Square) -> ChessPiece:
    """Returns the piece at given square"""
    return self._contents.get(square)

  def __setitem__(self, square: Square, piece: ChessPiece) -> NoReturn:
    """Places given piece and given square"""
    self._contents |= {square: piece}

  def __delitem__(self, square: Square) -> NoReturn:
    """Deletes the item at given square. Deleting means placing the EMPTY
    piece."""
    self._contents |= {square: ChessPiece.EMPTY}

  def keys(self) -> list[Square]:
    """Implementation of keys method"""
    return [key for key in self._contents.keys()]

  def values(self) -> list[ChessPiece]:
    """Implementation of values"""
    return [piece for piece in self._contents.values()]

  def items(self) -> list[tuple[Square, ChessPiece]]:
    """Implementation of items method"""
    return [(k, v) for (k, v) in self._contents.items()]

  def getPiece(self, square: Square) -> ChessPiece:
    """Getter-function for the piece on the given square"""
    piece = self._contents.get(square, None)
    if piece is not None:
      if isinstance(piece, ChessPiece):
        return piece
      raise TypeError
    ic(square, piece)
    os.abort()
    raise UnexpectedStateError

  def setPiece(self, square: Square, piece: ChessPiece) -> NoReturn:
    """Setter-function for the piece on the given square"""
    if piece is not None:
      if isinstance(piece, ChessPiece):
        self._contents[square] = piece
      else:
        raise TypeError
    else:
      raise UnexpectedStateError

  def delPiece(self, square: Square) -> ChessPiece:
    """Deleter-function for the given square. This removes the piece from
    it. Invoking the deleter returns the chess piece"""
    piece = self.getPiece(square)
    self.setPiece(square, ChessPiece.EMPTY)
    return piece
