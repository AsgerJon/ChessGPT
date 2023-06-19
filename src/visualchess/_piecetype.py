"""PieceType defines chess piece types"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
from typing import Never

from icecream import ic
from worktoy.waitaminute import ReadOnlyError

ic.configureOutput(includeContext=True)


class PieceType(Enum):
  """Types of chess pieces"""
  EMPTY = 0
  KING = 1
  QUEEN = 2
  ROOK = 3
  BISHOP = 4
  KNIGHT = 5
  PAWN = 6

  def __bool__(self) -> bool:
    """Only the EMPTY instance is False, all other instances are True"""
    return False if self is PieceType.EMPTY else True

  def __eq__(self, other: PieceType) -> bool:
    """Equality operator compares to other instances of PieceType"""
    if self is PieceType.EMPTY or other is PieceType.EMPTY:
      return False
    return True if self.value == other.value else False

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

  nameLower = property(_getNameLower, _noAcc, _noAcc, )

  def __str__(self) -> str:
    """String Representation"""
    return self.name.capitalize()

  def __repr__(self) -> str:
    """Code Representation"""
    return 'PieceType.%s' % (self.name.upper())
