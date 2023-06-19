"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum
from typing import Optional, Never

from icecream import ic
from worktoy.core import maybe
from worktoy.parsing import maybeTypes, extractArg
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError

ic.configureOutput(includeContext=True)


class ChessColor(Enum):
  """ChessColor enum"""
  WHITE = -1
  NULL = 0
  BLACK = 1

  @classmethod
  def parse(cls, *args, **kwargs) -> ChessColor:
    """Parses arguments"""
    colorKeys = stringList('color, side, chessColor')
    color, args, kwargs = extractArg(ChessColor, colorKeys, *args, **kwargs)
    if isinstance(color, ChessColor):
      return color
    colorInt, args, kwargs = extractArg(int, colorKeys, *args, **kwargs)
    if isinstance(colorInt, int):
      return cls.fromValue(colorInt)

  @classmethod
  def fromString(cls, name: str) -> ChessColor:
    """Returns the ChessColor matching the given string"""
    for color in cls:
      if name.lower() == color.nameLower:
        return color
    msg = """Failed to find an instance of %s having name: %s!"""
    raise NameError(msg % (cls.getClassName(), name))

  @classmethod
  def fromValue(cls, value: int) -> ChessColor:
    """Returns the ChessColor having given value"""
    for color in cls:
      if color.value == value:
        return color
    msg = """Failed to find an instance of %s matching given value: %s!"""
    raise ValueError(msg % (cls.getClassName(), value))

  @classmethod
  def getClassName(cls) -> str:
    """String representation of class"""
    className = getattr(cls, '__qualname__', None)
    className = maybe(className, getattr(cls, '__name__', None))
    className = maybe(className, '%s' % cls)
    if isinstance(className, str):
      return className
    msg = """Expected class name to be %s, but found %s of type %s"""
    raise TypeError(msg % (str, className, type(className)))

  def __str__(self, ) -> str:
    """String representation"""
    if not self:
      return 'Colorless'
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
    if self is ChessColor.BLACK and other is ChessColor.BLACK:
      return True
    if self is ChessColor.WHITE and other is ChessColor.WHITE:
      return True
    return False

  def __hash__(self, ) -> int:
    """Implementation of hash"""
    return 2 if not self else (3 if self is ChessColor.BLACK else 5)

  def getEnPassantRank(self) -> int:
    """Getter-function for the rank from which a pawn can capture en
    passant. """
    if self is ChessColor.WHITE:
      return 3
    if self is ChessColor.BLACK:
      return 4
    msg = """The empty color does not support en passant!"""
    raise AttributeError(msg)

  def _getNameLower(self) -> str:
    """Getter-function for lower-case version of name"""
    return self.name.lower()

  def _noAcc(self, *_) -> Never:
    """Illegal Accessor Function"""
    raise ReadOnlyError('lowerName')

  @classmethod
  def parseNames(cls, *args) -> Optional[ChessColor]:
    """Parses through the names and returns the first instance class
    instance which matches it or returns None."""
    names = maybeTypes(str, *args)
    for name in names:
      if isinstance(name, str):
        for instance in cls:
          if name.lower() == instance.nameLower:
            return instance

  def __invert__(self) -> ChessColor:
    """NULL inverted is NULL. Otherwise ~BLACK==WHITE"""
    if self is ChessColor.NULL:
      return ChessColor.NULL
    return ChessColor.WHITE if self is ChessColor.BLACK else ChessColor.BLACK

  nameLower = property(_getNameLower, _noAcc, _noAcc, )
