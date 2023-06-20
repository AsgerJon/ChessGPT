"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum

from icecream import ic
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList

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
