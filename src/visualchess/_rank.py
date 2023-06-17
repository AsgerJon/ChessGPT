"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum

from icecream import ic
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList, monoSpace

ic.configureOutput(includeContext=True)


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
  NULL = -1

  @classmethod
  def parse(cls, *args, **kwargs) -> Rank:
    """Parses arguments"""
    rankKeys = stringList('rank, y, row')
    rank, args, kwargs = extractArg(Rank, rankKeys, *args, **kwargs)
    if isinstance(rank, Rank):
      return rank
    rankStr, args, kwargs = extractArg(str, rankKeys, *args, **kwargs)
    if rankStr is not None:
      if isinstance(rankStr, str):
        return cls.fromStr(rankStr)
    rankInt, args, kwargs = extractArg(str, rankKeys, *args, **kwargs)
    if rankInt is not None:
      if isinstance(rankInt, int):
        return cls.fromValue(rankInt)
    msg = """Expected type %s, but received %s of type %s!"""
    raise TypeError(msg % (Rank, rank, type(rank)))

  @classmethod
  def fromValue(cls, y: int) -> Rank:
    """Finds the matching value"""
    if y < 0 or 7 < y:
      return Rank.NULL
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

  def __add__(self, y: int) -> Rank:
    """Adds other to self"""
    if isinstance(y, int):
      if -1 < y < 8:
        out = self.value + y
      else:
        return Rank.NULL
      return self.fromValue(out)
    raise TypeError

  def __sub__(self, y: int) -> Rank:
    """Subtracts given value from self"""
    return self.__add__(-y)

  def __bool__(self, ) -> bool:
    """Only NULL is False."""
    return False if self is Rank.NULL else True

  def __eq__(self, other) -> bool:
    """Tests equality between instances using the 'is' condition. Please
    note, that NULL is not equal to itself"""
    return True if self and other and self.value == other.value else False
