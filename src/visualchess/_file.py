"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum
import os

from icecream import ic
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList, monoSpace

ic.configureOutput(includeContext=True)


class File(IntEnum):
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
  def parse(cls, *args, **kwargs) -> File:
    """Parses arguments"""
    fileKeys = stringList('file, x, col, column')
    file, args, kwargs = extractArg(File, fileKeys, *args, **kwargs)
    if isinstance(file, File):
      return file
    fileStr, args, kwargs = extractArg(str, fileKeys, *args, **kwargs)
    if fileStr is not None:
      if isinstance(fileStr, str):
        return cls.fromStr(fileStr)
    fileInt, args, kwargs = extractArg(str, fileKeys, *args, **kwargs)
    if fileInt is not None:
      if isinstance(fileInt, int):
        return cls.fromValue(fileInt)
    msg = """Expected type %s, but received %s of type %s!"""
    raise TypeError(msg % (File, file, type(file)))

  @classmethod
  def fromValue(cls, x: int) -> File:
    """Finds the matching value"""
    if x < 0 or 7 < x:
      return File.NULL
    for file in File:
      if file.value == x:
        return file
    os.abort()
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

  def __add__(self, x: int) -> File:
    """Adds other to self"""
    if isinstance(x, int):
      if -1 < x < 8:
        out = self.value + x
      else:
        msg = """The file must be in the range from 0 to 7 inclusive, 
        but received: %d""" % x
        raise OverflowError(monoSpace(msg))
      return File.fromValue(out)
    raise TypeError

  def __sub__(self, x: int) -> File:
    """Subtracts given value from self"""
    return self.__add__(-x)

  def __bool__(self, ) -> bool:
    """Only NULL is False."""
    return False if self is File.NULL else True

  def __eq__(self, other) -> bool:
    """Tests equality between instances using the 'is' condition. Please
    note, that NULL is not equal to itself"""
    return True if self and other and self.value == other.value else False

  def __hash__(self, ) -> int:
    """LOL"""
    return self.value
