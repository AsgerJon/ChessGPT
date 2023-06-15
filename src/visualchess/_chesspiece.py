"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum
import os
from typing import Never, TYPE_CHECKING

from PySide6.QtCore import QPointF
from PySide6.QtGui import QPixmap, QColor, QCursor
from icecream import ic
from worktoy.core import maybe
from worktoy.parsing import maybeType, searchKeys
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError

from visualchess import PieceType, ChessColor

if TYPE_CHECKING:
  from visualchess import Widget

ic.configureOutput(includeContext=True)


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

  @classmethod
  def fromInt(cls, index: int, ) -> ChessPiece:
    """Returns the instance having the given int"""
    for piece in cls:
      if piece.value == index:
        return piece
    msg = """Expected an index greater than -7 and less than 7, 
    but received: %d"""
    raise IndexError(msg % index)

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

  def getColor(self) -> ChessColor:
    """Getter-function for color"""
    if not self.value:
      return ChessColor.NULL
    if self.value < 0:
      return ChessColor.WHITE
    return ChessColor.BLACK

  def setColor(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('color', 'set')

  def getPiece(self) -> PieceType:
    """Getter-function for piece"""
    for type_ in PieceType:
      if type_.value == abs(self.value):
        return type_
    raise ValueError('Could not recognize piece')

  def setPiece(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('piece', 'set')

  @classmethod
  def fromColorPiece(cls, *args, **kwargs) -> ChessPiece:
    """Finds the piece given the color and piece type"""
    pieceKeys = stringList('piece, pieceType, chessPiece')
    colorKeys = stringList('color, chessColor, pieceColor')
    pieceKwarg = searchKeys(*pieceKeys) @ PieceType >> kwargs
    colorKwarg = searchKeys(*colorKeys) @ PieceType >> kwargs
    pieceStrArg = PieceType.parseNames(*args)
    colorStrArg = ChessColor.parseNames(*args)
    pieceArg = maybeType(PieceType, *args)
    colorArg = maybeType(ChessColor, *args)
    piece_ = maybe(pieceKwarg, pieceStrArg, pieceArg, )
    color_ = maybe(colorKwarg, colorStrArg, colorArg, )
    for chessPiece in cls:
      if chessPiece.color == color_ and chessPiece.piece == piece_:
        return chessPiece
    return cls.EMPTY

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

  def __invert__(self, ) -> ChessPiece:
    """Returns the piece of the opposite color"""
    if not self:
      return self
    return ChessPiece.fromInt(-self.value)

  @classmethod
  def getKings(cls) -> list[ChessPiece]:
    """Returns a list of all the kings"""
    return [cls.BLACK_KING, cls.WHITE_KING]

  @classmethod
  def getKnights(cls) -> list[ChessPiece]:
    """Returns a list of all the knights"""
    return [cls.BLACK_KNIGHT, cls.WHITE_KNIGHT]

  @classmethod
  def getBishops(cls) -> list[ChessPiece]:
    """Returns a list of all the bishops"""
    return [cls.BLACK_BISHOP, cls.WHITE_BISHOP]

  @classmethod
  def getRooks(cls) -> list[ChessPiece]:
    """Returns a list of all the rooks"""
    return [cls.BLACK_ROOK, cls.WHITE_ROOK]

  @classmethod
  def getQueens(cls) -> list[ChessPiece]:
    """Returns a list of all the queens"""
    return [cls.BLACK_QUEEN, cls.WHITE_QUEEN]

  @classmethod
  def getPawns(cls) -> list[ChessPiece]:
    """Returns a list of all the pawns"""
    return [cls.BLACK_PAWN, cls.WHITE_PAWN]

  @classmethod
  def getQueenRookBishop(cls) -> list[ChessPiece]:
    """Returns a list of long range pieces"""
    return [*cls.getQueens(), *cls.getRooks(), *cls.getBishops(), ]

  color = property(getColor, setColor, setColor)
  piece = property(getPiece, setPiece, setPiece)
