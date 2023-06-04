"""Geometry is a class representation points and shapes in PySide6"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QRect, QRectF, QLineF, QLine, QPointF
from icecream import ic
from worktoy.core import maybe
from worktoy.field import BaseField
from worktoy.parsing import extractArg, maybeType
from worktoy.stringtools import stringList
from worktoy.waitaminute import UnexpectedStateError

from moreworktoy import FloatField, OverLoadify, overload

ic.configureOutput(includeContext=True)


@FloatField('x', 0)
@FloatField('y', 0)
class Point:
  """Points are instances of QPointF using complex number operations to
  perform scaling, rotation and translation."""
  x: float
  y: float

  def __init__(self, *args, **kwargs) -> None:
    xKeys = stringList('x, left')
    yKeys = stringList('y, top')
    x, args, kwargs = extractArg(float, xKeys, *args, **kwargs)
    y, args, kwargs = extractArg(float, yKeys, *args, **kwargs)
    self.x = x if isinstance(maybe(x, self.x), float) else 0
    self.y = y if isinstance(maybe(y, self.y), float) else 0

  def __str__(self, ) -> str:
    """String Representation"""
    return 'Point: (%.2f, %.2f)' % (self.x, self.y)

  def __repr__(self, ) -> str:
    """String Representation"""
    return 'Point(%.2f, %.2f)' % (self.x, self.y)

  def __complex__(self) -> complex:
    """Complex number representation"""
    return self.x + self.y * 1j


Points = tuple[Point, ...]
ParseFloats = tuple[bool, Optional[tuple[float]]]


class Rect:
  """Rect"""

  @staticmethod
  def _parseQLine(*args, ) -> ParseFloats:
    """From QLineF"""
    line = maybe(maybeType(QLineF, *args), maybeType(QLine, *args))
    if line is None:
      return (False, None)
    if isinstance(line, QLine):
      line = line.toLineF()
    if isinstance(line, QLineF):
      x = (line.p1().x(), line.p2().x(),)
      y = (line.p1().y(), line.p2().y(),)
      left, right = min(x), max(x)
      top, bottom = min(y), max(y)
      return Rect._parseFloats(left, top, right, bottom)
    raise UnexpectedStateError()

  @staticmethod
  def _parseQRectF(*args, ) -> ParseFloats:
    """From QRectF"""
    rect = maybeType(QRect, *args)
    rectF = maybeType(QRectF, *args)
    rect = maybe(rectF, rect)
    if rect is None:
      return (False, None)
    vals = (args[0].left(), args[0].top(), args[0].right(), args[0].bottom())
    return Rect._parseFloats(*vals)

  @staticmethod
  def _parseComplex(*args, ) -> ParseFloats:
    """Parses 2 complex numbers"""
    if len(args) < 2:
      return (False, None)
    complexArgs = []
    for arg in args:
      if isinstance(arg, complex):
        complexArgs.append(arg)
    if len(complexArgs) < 2:
      return (False, None)
    z0, z1 = args[:2]
    return Rect._parseFloats(z0.real, z0.imag, z1.real, z1.imag)

  @staticmethod
  def _parseFloats(*args, ) -> ParseFloats:
    """Parses four floats"""
    if len(args) < 4:
      return (False, None)
    floatArgs = []
    for arg in args:
      if isinstance(arg, float):
        floatArgs.append(arg)
      elif isinstance(arg, int):
        floatArgs.append(float(arg))
    if len(floatArgs) < 4:
      return (False, None)
    args = [float(arg) for arg in args[:4]]
    if all([isinstance(arg, float) for arg in args]):
      return (True, (*args))

  @classmethod
  def _parsePositional(cls, *args) -> tuple[Optional[float], ...]:
    """Applies positional parsing"""
    _parseFunctions = [
      cls._parseFloats,
      cls._parseComplex,
      cls._parseQRectF,
      cls._parseQLine,
    ]
    for _parse in _parseFunctions:
      res = _parse(*args, )
      if res[0]:
        return res[1]
    return (*[None for _ in range(4)],)

  @staticmethod
  def _parseKey(**kwargs) -> Points:
    """Parses keyword arguments. These take precedence against the
    positional arguments"""
    left = kwargs.get('left', None)
    top = kwargs.get('top', None)
    right = kwargs.get('right', None)
    bottom = kwargs.get('bottom', None)
    return (left, top, bottom, right)

  @staticmethod
  def _parse(*args, **kwargs, ) -> Points:
    """Parses arguments"""
    leftKwarg, topKwarg, rightKwarg, bottomKwarg = Rect._parseKey(**kwargs)
    leftArg, topArg, rightArg, bottomArg = Rect._parsePositional(*args)
    leftDefault, topDefault, rightDefault, bottomDefault = 0, 0, 1, 1,
    left = maybe(leftKwarg, leftArg, leftDefault)
    top = maybe(topKwarg, topArg, topDefault)
    right = maybe(rightKwarg, rightArg, rightDefault)
    bottom = maybe(bottomKwarg, bottomArg, bottomDefault)
    return (Point(left, top), Point(right, bottom))

  def __init__(self, *args, **kwargs) -> None:
    self._topLeft, self._bottomRight = self._parse(*args, **kwargs)
