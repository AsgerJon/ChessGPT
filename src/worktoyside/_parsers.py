"""The parsers found here helps extract desired variables from positional
and keyword arguments"""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QSize, QRect, QSizeF, QRectF, QMargins, QMarginsF
from PySide6.QtGui import QColor
from worktoy import maybeTypes, maybeType, searchKeys, maybe


def parseSize(*args, **kwargs) -> QSize:
  """Parses arguments to instance of QSize"""
  intArgs = maybeTypes(int, *args, padLen=2, padChar=None)
  sizeArg = maybeType(QSize, *args)
  rectArg = maybeType(QRect)
  sizeFArg = maybeType(QSizeF, *args)
  rectFArg = maybeType(QRectF, *args)
  heightKwarg = searchKeys('h', 'height') @ int >> kwargs
  widthKwarg = searchKeys('w', 'width') @ int >> kwargs
  sizeKwarg = searchKeys('size', ) @ (QSize, QSizeF) >> kwargs
  rectKwarg = searchKeys('rect', 'rectangle') @ (QRect, QRectF) >> kwargs
  rect = maybe(rectKwarg, rectArg, rectFArg, None)
  size = maybe(sizeKwarg, sizeArg, sizeFArg, None)
  widthArg, heightArg = intArgs
  height = maybe(heightKwarg, heightArg, None)
  width = maybe(widthKwarg, widthArg, None)
  if rect is not None:
    return rect if isinstance(rect, QRect) else rect.toRect()
  if size is not None:
    return size if isinstance(size, QSize) else size.toSize()
  if height is None and width is None:
    return QSize(24, 24)
  if height is None:
    return QSize(width, width)
  if width is None:
    return QSize(height, height)
  width, height = [min([width, height]) for _ in [0, 1]]
  return QSize(width, height)


def parseColor(*args, **kwargs) -> QColor:
  """Parses arguments to QColor"""
  intArgs = maybeTypes(int, *args, padLen=3, padChar=None)
  colorKwarg = searchKeys('color') @ QColor >> kwargs
  colorArg = maybeType(QColor, *args)
  redKwarg = searchKeys('r', 'red') @ int >> kwargs
  greenKwarg = searchKeys('g', 'green') @ int >> kwargs
  blueKwarg = searchKeys('b', 'blue') @ int >> kwargs
  redArg, greenArg, blueArg = intArgs
  redDefault, greenDefault, blueDefault = (255, 255, 255)
  color = maybe(colorKwarg, colorArg, None)
  red = maybe(redKwarg, redArg, redDefault)
  green = maybe(greenKwarg, greenArg, greenDefault)
  blue = maybe(blueKwarg, blueArg, blueDefault)
  if color is None:
    return QColor(red, green, blue)
  return color


def parseMargins(*args, **kwargs) -> QMargins:
  """Parses arguments to margins"""
  intArgs = maybeTypes(int, *args, padLen=4, padChar=None)
  marginsKwarg = searchKeys('margins', ) @ QMargins >> kwargs
  marginsFKwarg = searchKeys('margins', ) @ QMarginsF >> kwargs
  marginsArg = maybeType(QMargins, *args)
  marginsFArg = maybeType(QMarginsF, *args)
  leftKwarg = searchKeys('left', 'xmin') @ int >> kwargs
  topKwarg = searchKeys('top', 'ymin') @ int >> kwargs
  rightKwarg = searchKeys('right', 'xmax') @ int >> kwargs
  bottomKwarg = searchKeys('bottom', 'ymax') @ int >> kwargs
  leftArg, topArg, rightArg, bottomArg = intArgs
  leftDefault, topDefault, rightDefault, bottomDefault = [0, 0, 0, 0]
  left = maybe(leftKwarg, leftArg, leftDefault)
  top = maybe(topKwarg, topArg, topDefault)
  right = maybe(rightKwarg, rightArg, rightDefault)
  bottom = maybe(bottomKwarg, bottomArg, bottomDefault)
  margins = maybe(marginsKwarg, marginsArg, None)
  marginsF = maybe(marginsFKwarg, marginsFArg, None)
  if marginsF is not None:
    marginsF = margins.toMargins()
  intArgMargins = QMargins(left, top, right, bottom)
  return maybe(margins, marginsF, intArgMargins)
