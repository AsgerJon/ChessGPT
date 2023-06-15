"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum
import os

from icecream import ic
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList

ic.configureOutput(includeContext=True)


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
    for file in File:
      if file.value == x:
        return file
    ic(x)
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
