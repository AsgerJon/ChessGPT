"""PointLike enables polymorphisms relating to point like structures."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic
from worktoy.parsing import extractArg, maybeTypes, maybeType
from worktoy.stringtools import stringList

from visualchess import Square

ic.configureOutput(includeContext=True)


class PointLike:
  """Takes an instance: Square, Move, tuple, list, complex or two ints and
  applies addition. """

  @staticmethod
  def maybeTypeName(type_: str, *objs: object) -> object:
    """Performs a named type test. Please note that this method is unaware
    of parent classes. For example, let Fraction be a subclass of Number,
    and let fraction be an instance of Fraction. Then:
    isinstance(fraction, Number) -> True, but
    maybeTypeName(Number, [None, False, fraction, ... ]) -> None
    This is because the method relies on the value found with:
    name: str = '%s' % type(arg).__name__"""
    
    for obj in objs:
      pass

  @staticmethod
  def parseArguments(*args, **kwargs) -> tuple[int, int]:
    """Parses arguments"""
    intArgs = maybeTypes(int, *args, padLen=2, padChar=None)
    complexArg = maybeType(complex, *args)

  def __init__(self, *args, **kwargs) -> None:
    self._x = None
    self._y = None
