"""File and Rank enums"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import string
from enum import Enum


class File(Enum):
  """Enums representing the files on a chessboard"""
  NULL = 0
  A = 1
  B = 2
  C = 3
  D = 4
  E = 5
  F = 6
  G = 7
  H = 8

  def __str__(self) -> str:
    """String Representation"""
    if self.value:
      return '%s' % self.name
    return 'NULL'

  @classmethod
  def find(cls, index: int | str) -> File:
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


class Rank(Enum):
  """Enumx representing the ranks on a chessboard"""
  NULL = 0
  rank0 = 1
  rank1 = 2
  rank2 = 3
  rank3 = 4
  rank4 = 5
  rank5 = 6
  rank6 = 7
  rank7 = 8

  def __str__(self) -> str:
    """String Representation"""
    if self.value:
      return '%s' % (int(self.name.replace('rank', '')) + 1)
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
