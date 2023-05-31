"""The chessBoardFunc function takes a QRectF and returns the necessary
rectangles"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRectF, QSizeF, QPointF, QSize
from worktoy.core import maybe


def chessBoardFunc(rect: QRectF, **kwargs) -> dict[str, list[QRectF]]:
  """The chessBoardFunc function takes a QSizeF and returns the necessary
  rectangles
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""
  origin = QPointF(0, 0)
  bezelRatio = kwargs.get('bezelRatio', None)
  boardRatio = kwargs.get('boardRatio', None)
  gridRatio = kwargs.get('gridRatio', None)
  if boardRatio is None and bezelRatio is None:
    bezelRatio = 32 / 400
    boardRatio = 1 - bezelRatio
  if boardRatio is None:
    boardRatio = 1 - bezelRatio
  if bezelRatio is None:
    bezelRatio = 1 - boardRatio
  gridRatio = maybe(gridRatio, float(8 / 400))
  _globalRect = rect
  _globalCenter = _globalRect.center()
  _globalSize = _globalRect.size()
  _globalWidth = _globalRect.width()
  _globalHeight = _globalRect.height()
  _bezelWidth = _globalWidth * boardRatio
  _bezelHeight = _globalHeight * boardRatio
  _bezelSide = min(_bezelHeight, _bezelWidth)
  _bezelSize = QSizeF(_bezelSide, _bezelSide)
  _bezelSquare = QRectF(origin, _bezelSize)
  _bezelSquare.moveCenter(_globalCenter)
  _bezelTopLeft = _bezelSquare.topLeft()
  _boardWidth = _bezelWidth * boardRatio
  _boardHeight = _bezelHeight * boardRatio
  _boardSide = min(_boardWidth, _boardHeight)
  _boardSize = QSizeF(_boardSide, _boardSide)
  _boardRect = QRectF(origin, _boardSize)
  _boardRect.moveCenter(_globalCenter)
  _boardLeft = _boardRect.left()
  _boardTop = _boardRect.top()
  _squareSide = _boardSide * (1 - float(gridRatio)) / 8
  _squareStep = _boardSide / 8
  light, dark = [], []
  left0, top0, step, = _boardLeft, _boardTop, _squareStep
  size = QSize(_squareSide, _squareSide)
  for i in range(8):
    for j in range(8):
      topLeft = QPointF(left0 + i * step, top0 + j * step)
      rect = QRectF(topLeft, size)
      if i % 2 == j % 2:
        light.append(rect)
      else:
        dark.append(rect)

  bezel = _bezelSquare
  grid = _boardRect
  return dict(light=light, dark=dark, bezel=[bezel], grid=[grid])
