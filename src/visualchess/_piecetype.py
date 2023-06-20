"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
from typing import Never, Optional, TYPE_CHECKING

from icecream import ic
from worktoy.parsing import maybeTypes
from worktoy.waitaminute import ReadOnlyError

if TYPE_CHECKING:
  from visualchess import ChessPiece

ic.configureOutput(includeContext=True)


class PieceType(Enum):
  """Types of chess pieces"""
  EMPTY = 0
  PAWN = 1
  KNIGHT = 2
  BISHOP = 3
  ROOK = 4
  QUEEN = 5
  KING = 6

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

  def __hash__(self) -> int:
    """LOL"""
    return self.value

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

  def _noAcc(self, *_) -> Never:
    """Illegal Accessor Function"""
    raise ReadOnlyError('lowerName')

  @classmethod
  def recognizeType(cls, piece: ChessPiece) -> PieceType:
    """Analyses the piece and returns the proper type"""
    return piece.piece

  @classmethod
  def parseNames(cls, *args) -> Optional[PieceType]:
    """Parses through the names and returns the first instance class
    instance which matches it or returns None."""
    names = maybeTypes(str, *args)
    for name in names:
      if isinstance(name, str):
        for instance in cls:
          if name.lower() == instance.nameLower:
            return instance

  nameLower = property(_getNameLower, _noAcc, _noAcc, )
