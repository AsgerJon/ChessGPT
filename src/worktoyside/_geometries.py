"""The geometries file contains functions related to the Qt
representations of various geometrical shapes"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TypeAlias, Union

from PySide6.QtGui import QPolygon, QPolygonF
from PySide6.QtCore import QPointF, QLineF, QSizeF, QRectF, QMarginsF
from PySide6.QtCore import QPoint, QLine, QSize, QRect, QMargins
from worktoy import searchKeys, maybe

GeometriesF: TypeAlias = Union[
  QPointF, QLineF, QSizeF, QRectF, QPolygonF, QMarginsF]
GeometriesInt: TypeAlias = Union[
  QPoint, QLine, QSize, QRect, QPolygon, QMargins]
Geometries: TypeAlias = Union[
  QPointF, QLineF, QSizeF, QRectF, QPolygonF, QMarginsF,
  QPoint, QLine, QSize, QRect, QPolygon, QMargins]


def geometriesF2Int(obj: Geometries, **kwargs) -> Geometries:
  """Converts instances of QPointF, QLineF, QSizeF, QRectF, QPolygonF,
  QMarginsF to instances of the corresponding QPoint, QLine, QSize, QRect,
  QPolygon, QMargins.

  Args:
    obj (object): The object to convert.

  Returns:
    object: The converted object.

  Raises:
    TypeError: If the type of the input object is not supported for
    conversion.
  """
  strictKwarg = searchKeys('strict', ) @ bool >> kwargs
  defaultKwarg = searchKeys('default') >> kwargs
  strictDefault = True
  defaultDefault = None
  strict = maybe(strictKwarg, strictDefault)
  default_ = maybe(defaultKwarg, defaultDefault)
  if default_ is not None:
    strict = True
  if isinstance(obj, QPointF):
    return QPoint(obj.x(), obj.y())
  elif isinstance(obj, QLineF):
    return QLine(obj.p1().x(), obj.p1().y(), obj.p2().x(), obj.p2().y())
  elif isinstance(obj, QSizeF):
    return QSize(obj.width(), obj.height())
  elif isinstance(obj, QRectF):
    return QRect(obj.x(), obj.y(), obj.width(), obj.height())
  elif isinstance(obj, QPolygonF):
    return QPolygon([QPoint(p.x(), p.y()) for p in obj])
  elif isinstance(obj, QMarginsF):
    return QMargins(obj.left(), obj.top(), obj.right(), obj.bottom())
  elif isinstance(obj, QPoint):
    return QPointF(obj.x(), obj.y())
  elif isinstance(obj, QLine):
    return QLineF(obj.x1(), obj.y1(), obj.x2(), obj.y2())
  elif isinstance(obj, QSize):
    return QSizeF(obj.width(), obj.height())
  elif isinstance(obj, QRect):
    return QRectF(obj.x(), obj.y(), obj.width(), obj.height())
  elif isinstance(obj, QPolygon):
    return QPolygonF([QPointF(p.x(), p.y()) for p in obj])
  elif isinstance(obj, QMargins):
    return QMarginsF(obj.left(), obj.top(), obj.right(), obj.bottom())
  else:
    if strict:
      raise TypeError("Unsupported type for conversion")
    if default_:
      return default_
  return obj
