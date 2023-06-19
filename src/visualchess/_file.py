"""File is a class representation of the files on the chess board"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
from typing import Never, TYPE_CHECKING

from icecream import ic
from worktoy.waitaminute import ReadOnlyError

if TYPE_CHECKING:
  from visualchess import Square
ic.configureOutput(includeContext=True)


class File(Enum):
  """File enum"""
  NULL = -1
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

  def __bool__(self, ) -> bool:
    """Only NULL is False"""
    return False if self is File.NULL else True

  def __eq__(self, other: File) -> bool:
    """Equality operator. NULL is not equal to itself"""
    if self is File.NULL or other is File.NULL:
      return False
    if self is other:
      return True

  def __add__(self, other: Square | File | int) -> File:
    """Implementation of addition. Together with subtraction implements
    arithmetic. If the value be out of range, NULL is returned"""
    if self is File.NULL or other is File.NULL:
      return File.NULL
    if other.__class__.__name__ == 'Square':
      return self + other.file
    if isinstance(other, File):
      return self + other.x
    if isinstance(other, int):
      if other < 0:
        return self - (-other)
      val = self.x + other
      if val < 0 or 7 < val:
        return File.NULL
      return File.fromValue(val)

  def __sub__(self, other: Square | File | int) -> File:
    """Implementation of subtraction. Together with addition implements
    arithmetic. If the value be out of range, NULL is returned"""
    if self is File.NULL or other is File.NULL:
      return File.NULL
    if other.__class__.__name__ == 'Square':
      return self - other.file
    if isinstance(other, File):
      return self - other.x
    if isinstance(other, int):
      if other < 0:
        return self + (-other)
      val = self.x + other
      if val < 0 or 7 < val:
        return File.NULL
      return File.fromValue(val)

  def _getX(self) -> int:
    """Getter-function for x coordinate"""
    return self.value

  def _noAcc(self, *_) -> Never:
    """Illegal Accessor Function"""
    raise ReadOnlyError('lowerName')

  def __str__(self, ) -> str:
    """String Representation"""
    return self.name.upper()[0]

  def __repr__(self, ) -> str:
    """Code Representation"""
    return """File.%s""" % self.name

  x = property(_getX, _noAcc, _noAcc)
