"""This file contains general geometric functions used frequently without
being specific to anything."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import cmath
from math import atan2, sin, cos

from PySide6.QtCore import QRectF, QSizeF, QPointF
from PySide6.QtGui import QTransform
from icecream import ic
from worktoy.core import maybe

from workstyle.styles import BoardDims

Polar = tuple[float, float]
Cartesian = complex
ic.configureOutput(includeContext=True)


def fitSquareRect(rect: QRectF) -> QRectF:
  """Returns the largest square QRectF that fits in rect"""
  dim = min(rect.width(), rect.height())
  size = QSizeF(dim, dim)
  squareRect = QRectF(BoardDims.origin, size)
  squareRect.moveCenter(rect.center())
  return squareRect


def fitSquareMarginsRect(rect: QRectF) -> QRectF:
  """Returns the largest square QRectF that fits in given rect with the
  style margins deducted"""
  marginLeft = BoardDims.marginLeft
  marginTop = BoardDims.marginTop
  marginRight = BoardDims.marginRight
  marginBottom = BoardDims.marginBottom
  rect.adjust(marginLeft, marginTop, -marginRight, -marginBottom)
  return fitSquareRect(rect)


def complexPoint(point: QPointF) -> complex:
  """Returns the complex number such that:
  complexPoint(point).real = point.x()
  complexPoint(point).imag = point.y()
  """
  return point.x() + point.y() * 1j


def polarPoint(point: QPointF) -> tuple[float, float]:
  """Creates a representation of given point in polar coordinates."""


class Scalify:
  """Applies scaling"""

  @staticmethod
  def asComplex(point: QPointF) -> complex:
    """Renders complex number"""
    return point.x() + point.y() * 1j

  @staticmethod
  def cartesianToPolar(num: Cartesian) -> Polar:
    """Renders tuple of radius and angle"""
    return (abs(num).real, cmath.phase(num).real)

  @staticmethod
  def polarToCartesian(complexNumber: complex) -> Polar:
    """Returns to cartesian format"""

  @staticmethod
  def scaleDownPoint(point: QPointF, scale: float = None) -> QPointF:
    """Central scale function"""
    s = maybe(scale, 0.5)
    if not isinstance(s, float):
      raise TypeError
    num = point.x() + point.y() * 1j
    r, t = s * abs(num).real, cmath.phase(num).real
    return r * QPointF(cos(t), sin(t))

  @staticmethod
  def rotatePoint(point: QPointF, scale: float = None) -> QPointF:
    """Central rotate function"""
    r, t = s * abs(num).real, cmath.phase(num).real
    return r * QPointF(cos(t), sin(t))
