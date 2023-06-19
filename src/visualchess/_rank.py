"""Rank is a class representation of the ranks on the chess board"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum
from typing import Never, TYPE_CHECKING

from icecream import ic
from worktoy.waitaminute import ReadOnlyError

if TYPE_CHECKING:
  from visualchess import Square
ic.configureOutput(includeContext=True)


class Rank(IntEnum):
  """Rank is a class representation of the ranks on the chess board.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""
  rank1 = 7 - 0
  rank2 = 7 - 1
  rank3 = 7 - 2
  rank4 = 7 - 3
  rank5 = 7 - 4
  rank6 = 7 - 5
  rank7 = 7 - 6
  rank8 = 7 - 7
  NULL = -1

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

  def __bool__(self, ) -> bool:
    """Only NULL is False"""
    return False if self is Rank.NULL else True

  def __eq__(self, other: Rank) -> bool:
    """Equality operator. NULL is not equal to itself"""
    if self is Rank.NULL or other is Rank.NULL:
      return False
    if self is other:
      return True

  def __sub__(self, other: Square | Rank | int) -> Rank:
    """Implementation of subtraction. Together with addition implements
    arithmetic. If the value be out of range, NULL is returned"""
    if self is Rank.NULL or other is Rank.NULL:
      return Rank.NULL
    if other.__class__.__name__ == 'Square':
      return self - other.rank
    if isinstance(other, Rank):
      return self - other.y
    if isinstance(other, int):
      if other < 0:
        return self + (-other)
      val = self.y + other
      if val < 0 or 7 < val:
        return Rank.NULL
      return Rank.fromValue(val)

  def __add__(self, other: Square | Rank | int) -> Rank:
    """Implementation of addition. Together with subtraction implements
    arithmetic. If the value be out of range, NULL is returned"""
    if self is Rank.NULL or other is Rank.NULL:
      return Rank.NULL
    if other.__class__.__name__ == 'Square':
      return self + other.rank
    if isinstance(other, Rank):
      return self + other.y
    if isinstance(other, int):
      if other < 0:
        return self - (-other)
      val = self.y + other
      if val < 0 or 7 < val:
        return Rank.NULL
      return Rank.fromValue(val)

  def _getY(self) -> int:
    """Getter-function for y coordinate"""
    return self.value

  def _noAcc(self, *_) -> Never:
    """Illegal Accessor Function"""
    raise ReadOnlyError('lowerName')

  def __str__(self, ) -> str:
    """String Representation"""
    return self.name.upper()[0]

  def __repr__(self, ) -> str:
    """Code Representation"""
    return """Rank.%s""" % self.name

  y = property(_getY, _noAcc, _noAcc)
