"""Enums are necessary to have consistency across the modules"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum, Enum
from typing import TYPE_CHECKING, Never

from PySide6.QtCore import QRect, QRectF
from icecream import ic
from worktoy.stringtools import stringList
from worktoy.typetools import TypeBag, CallMeMaybe
from worktoy.waitaminute import ReadOnlyError

if TYPE_CHECKING:
  from visualchess import Square, ChessPiece

ic.configureOutput(includeContext=True)

Rect = TypeBag(QRectF, QRect)

_pieces = stringList('King, Queen, Rook, Bishop, Knight, Pawn')
_colors = stringList('white, black')


class ChessColor(Enum):
  """ChessColor enum"""
  WHITE = -1
  NULL = 0
  BLACK = 1

  @classmethod
  def fromString(cls, name: str) -> ChessColor:
    """Returns the ChessColor matching the given string"""
    for type_ in cls:
      if name.lower() == type_.name.lower():
        return type_

  def __str__(self, ) -> str:
    """String representation"""
    return self.name.capitalize()

  def __repr__(self, ) -> str:
    """Code representation"""
    return 'ChessColor.%s' % self.name

  def __bool__(self, ) -> bool:
    """The null or empty color is False, white and black are True"""
    return True if self.value else False

  def __eq__(self, other: ChessColor) -> bool:
    """The equality operator implementation. Please note that the empty
    color is not considered equal to itself."""
    if self and other:
      return True if self is other else False
    return False

  def __mul__(self, type_: PieceType) -> ChessPiece:
    """Creates an instance of ChessPiece having this color and the type
    indicated by the argument"""
    if isinstance(type_, PieceType):
      return ChessPiece.fromColorPiece(self, type_)
    return NotImplemented

  def __rmul__(self, type_: PieceType) -> ChessPiece:
    """By implementing the __rmul__, not multiplication implementation is
    required on the PieceType class."""
    if isinstance(type_, PieceType):
      return self * type_
    return NotImplemented

  def getEnPassantRank(self) -> Rank:
    """Getter-function for the rank at which pawns of this color may en
    passant. Rank.rank5 for white and 4 for black"""
    if self is ChessColor.WHITE:
      return Rank.rank5
    if self is ChessColor.BLACK:
      return Rank.rank4
    msg = """The empty color does not support en passant!"""
    raise AttributeError(msg)


class PieceType(Enum):
  """Types of chess pieces"""
  EMPTY = 0
  KING = 1
  QUEEN = 2
  ROOK = 3
  BISHOP = 4
  KNIGHT = 5
  PAWN = 6

  def __contains__(self, chessPiece: ChessPiece) -> bool:
    """Checks if given chess piece is of this type"""
    return True if chessPiece.piece is self else False

  def __bool__(self) -> bool:
    """Only the EMPTY instance is False, all other instances are True"""
    return False if self.name == 'EMPTY' else True

  def __eq__(self, other: PieceType) -> bool:
    """Equality operator compares to other instances of PieceType"""
    if not isinstance(other, PieceType):
      return NotImplemented
    if self is PieceType.EMPTY or other is PieceType.EMPTY:
      return False
    return False if self.value - other.value else True

  def _getNameLower(self) -> str:
    """Getter-function for lower-case version of name"""
    return self.name.lower()

  @classmethod
  def fromString(cls, name: str) -> PieceType:
    """Returns the PieceType matching the given string"""
    for type_ in cls:
      if name.lower() == type_.name.lower():
        return type_

  @classmethod
  def fromValue(cls, value: int) -> PieceType:
    """Getter-function for the instance matching the given value. Please
    note that the absolute value is used."""
    for type_ in PieceType:
      if abs(value) == type_.value:
        return type_

  nameLower = property(_getNameLower, )

  @classmethod
  def recognizeType(cls, piece: ChessPiece) -> PieceType:
    """Analyses the piece and returns the proper type"""
    return piece.piece


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
      if file.name.lower() == name.lower():
        return file
    raise TypeError

  def __str__(self, ) -> str:
    """String Representation"""
    return self.name.upper()[0]

  def __repr__(self, ) -> str:
    """Code Representation"""
    return """File.%s""" % self.name


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

  def __str__(self, ) -> str:
    """String Representation"""
    return '%s' % self.name[-1]

  def __repr__(self, ) -> str:
    """Code Representation"""
    return """Rank.%s""" % self.name


class Diagonal(IntEnum):
  """Like File and Rank, the Diagonals represent diagonal lines. They are
  identified by the file of the diagonal at row 1 as well as a sign.
  Positive means that as File increases from A through H, ranks increase,
  whereas negative indicates decreasing ranks. Like File and Rank,
  the integer value of a diagonal is hidden. Instead, the diagonals are
  named [File][LeftOrRight] as seen from both players. For example,
  AL means the diagonal starting at A1 going through H2, G3..."""

  AL = -1
  BL = -2
  CL = -3
  DL = -4
  EL = -5
  FL = -6
  GL = -7
  HL = -8
  _PLACEHOLDER = 0
  AR = 1
  BR = 2
  CR = 3
  DR = 4
  ER = 5
  FR = 6
  GR = 7
  HR = 8

  @classmethod
  def leftFile(cls, file: File) -> Diagonal:
    """Creates a Diagonal instance from the given file sloping left."""

  @classmethod
  def rightFile(cls, file: File) -> Diagonal:
    """Creates a Diagonal instance from the given file sloping right."""

  @classmethod
  def fromStr(cls, name: str) -> Diagonal:
    """Finds an instance from the given string"""
    if len(name) != 2:
      msg = """Diagonal names must be two characters, but received: %s of 
      length %d!"""
      raise ValueError(msg % (name, len(name)))
    for item in cls:
      if item.name == name:
        return item
    msg = """Unable to recognize given name as a diagonal: %s!"""
    raise ValueError(msg % name)

  @classmethod
  def fromValue(cls, value: int) -> Diagonal:
    """Finds the matching value"""
    for diagonal in Diagonal:
      if diagonal.value == value:
        return diagonal
    raise TypeError

  def getSquares(self) -> list[Square]:
    """Returns a list of squares contained in this diagonal"""
    squares = []
    file = File.fromStr(self.name[0])
    for (i, rank) in enumerate(Rank):
      squares.append(Square.fromFileRank(file, rank))
    return []
