"""The squareFactory creates QRectF instances matching the light and dark
squares on the chess board. As argument the function takes a target QRect
or QRectF and fills the centered square with the checkerboard pattern. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRectF, QRect, QPointF, QSizeF, QMargins
from PySide6.QtCore import QMarginsF
from icecream import ic
from worktoy.stringtools import justify
from worktoy.typetools import TypeBag

ic.configureOutput(includeContext=True)

Rect = TypeBag(QRectF, QRect)
Grid = TypeBag(int, float)
Float4 = tuple[float, float, float, float]
Int4 = tuple[int, int, int, int]
Margin = TypeBag(QMarginsF, QMargins, Float4)


def _parseMargins(targetRect: Rect, margins: Margin) -> Int4:
  """Parses the margins"""
  if isinstance(margins, tuple):
    margins = [m for m in margins if isinstance(m, float)]
    if len(margins) < 4:
      raise TypeError
    if all([m * m < 1 for m in margins]):
      sideLength = targetRect.width() / 2 + targetRect.height() / 2
      left, top, right, bottom = [int(m * sideLength) for m in margins]
      return (left, top, right, bottom)
  if isinstance(margins, QMargins):
    return _parseMargins(targetRect, margins.toMarginsF())
  if not isinstance(margins, QMarginsF):
    raise TypeError
  left, top = int(margins.left()), int(margins.top())
  right, bottom = int(margins.right()), int(margins.bottom())
  return (left, top, right, bottom)


def _centerTarget(targetRect: Rect, margins: Margin):
  """The squareFactory creates QRectF instances matching the light and dark
  squares on the chess board. As argument the function takes a target QRect
  or QRectF and fills the centered square with the checkerboard pattern.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  if isinstance(targetRect, QRect):
    targetRect = targetRect.toRectF()
  if not isinstance(targetRect, QRectF):
    msg = """Expected rectangle to be of type QRect or QRectF but 
    received: %s!""" % (type(targetRect))
    raise TypeError(justify(msg))
  left, top, right, bottom = _parseMargins(targetRect, margins)
  width = targetRect.width() - left - right
  height = targetRect.height() - top - bottom
  sideLength = min(width, height)
  size = QSizeF(sideLength, sideLength)
  targetCenterX = targetRect.center().x() + left - right
  targetCenterY = targetRect.center().y() + top - bottom
  targetCenter = QPointF(targetCenterX, targetCenterY)
  newTarget = QRectF(QPointF(0, 0), size)
  newTarget.moveCenter(targetCenter)
  return newTarget


def _parseGrid(target: Rect, grid: Grid) -> Grid:
  """Parses the grid. Use floats in unit range to indicate relative grids.
  Integer valued grids are understood as absolute"""
  if isinstance(grid, int):
    return grid if grid > 1 else 1
  if grid ** 2 > 1:
    raise ValueError
  return grid * target.width() / 2 + grid * target.height() / 2


def squareFactory(target: Rect,
                  margins: Margin,
                  grid: Grid) -> tuple[list[QRectF], list[QRectF]]:
  """The squareFactory creates QRectF instances matching the light and dark
  squares on the chess board. As argument the function takes a target QRect
  or QRectF and fills the centered square with the checkerboard pattern.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  target = _centerTarget(target, margins)
  targetSide = target.width() / 2 + target.height() / 2
  left0, top0, right0, bottom0 = _parseMargins(target, margins)
  grid = _parseGrid(target, grid)
  squareStep = targetSide / 8
  squareSize = (targetSide - 7 * grid) / 8
  lightSquares, darkSquares = [], []
  size = QSizeF(squareSize, squareSize)
  for i in range(8):
    for j in range(8):
      topLeft = QPointF(left0 + squareStep * i, top0 + squareStep * j)
      if i % 2 == j % 2:
        darkSquares.append(QRectF(topLeft, size))
      else:
        lightSquares.append(QRectF(topLeft, size))
  return (lightSquares, darkSquares)
