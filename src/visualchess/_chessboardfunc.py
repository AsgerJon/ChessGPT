"""The chessBoardFunc function takes a QRectF and returns the necessary
rectangles"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QRectF, QSizeF, QPointF, QSize
from icecream import ic

from visualchess import File, Rank
from workstyle.styles import BoardDims

ic.configureOutput(includeContext=True)


def chessBoardFunc(rect: QRectF, ) -> dict[str, list[QRectF]]:
  """The chessBoardFunc function takes a QSizeF and returns the necessary
  rectangles
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""
  files = [f for f in File if f.value]
  ranks = [r for r in Rank if r.value]
  viewPort = rect
  origin = QPointF(0, 0)
  bezelRatio = BoardDims.bezelRatio
  boardRatio = BoardDims.boardRatio
  gridRatio = BoardDims.gridRatio
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
  squares = []
  left0, top0, step, = _boardLeft, _boardTop, _squareStep
  size = QSize(_squareSide, _squareSide)
  for (i, file) in enumerate(files):
    for (j, rank) in enumerate(ranks):
      topLeft = QPointF(left0 + i * step, top0 + j * step)
      rect = QRectF(topLeft, size)
      color = 'light' if i % 2 == j % 2 else 'dark'
      entry = {'rect': rect, 'file': file, 'rank': rank, 'color': color}
      squares.append(entry)
      if i % 2 == j % 2:
        light.append(rect)
      else:
        dark.append(rect)
  _borderMid = bezelRatio * _bezelHeight / 2
  _size = QSize(2 * _borderMid, 2 * _borderMid)
  fileRects, rankRects = [], []
  left0 = _boardLeft
  right0 = _boardRect.right() + _borderMid
  top0 = _boardTop
  bottom0 = _boardRect.bottom()
  file0 = left0 + step / 2
  for (i, file) in enumerate(files):
    topRect = QRectF(origin, _size)
    bottomRect = QRectF(origin, _size)
    bottomCenter = QPointF(file0 + i * step, bottom0 + _borderMid)
    topCenter = QPointF(file0 + i * step, top0 - _borderMid)
    topRect.moveCenter(topCenter)
    bottomRect.moveCenter(bottomCenter)
    fileRects.append((bottomRect, topRect, '%s' % file))
  fileY0 = bottom0 - step / 2
  left0 = _boardLeft - _borderMid
  for (i, rank) in enumerate(ranks):
    leftRect, rightRect = QRectF(origin, _size), QRectF(origin, _size)
    leftCenter = QPointF(left0, fileY0 - step * i)
    rightCenter = QPointF(right0, fileY0 - step * i)
    leftRect.moveCenter(leftCenter)
    rightRect.moveCenter(rightCenter)
    rankRects.append((leftRect, rightRect, '%s' % rank))

  grid = _boardRect
  return dict(light=light, dark=dark, bezel=[viewPort], grid=[grid],
              files=fileRects, ranks=rankRects,
              debug=_bezelWidth - _borderMid, bezelRect=viewPort,
              boardRect=_boardRect, squares=squares)
