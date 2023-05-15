"""Creates static images of the chess board"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from builtins import str
from typing import NoReturn

from PySide6.QtCore import QPoint, QRect, QSize, QMargins, Qt
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont, QPaintEvent, \
  QBrush, QPen
from icecream import ic
from worktoy import maybe, maybeTypes, searchKeys, maybeType, stringList

from worktoyside import LayoutWidget

ic.configureOutput(includeContext=True)


def staticBoard(imageSize, fontFamily=None, fontSize=None,
                lightColor=None,
                darkColor=None, fileColor=None,
                rankColor=None):
  """Creates static images of the chess board
  #  MIT License
  #  Copyright (c) 2023 Asger Jon Vistisen"""
  imageSize = maybe(imageSize, 320)
  lightColor = maybe(lightColor, QColor(191, 191, 191))
  darkColor = maybe(darkColor, QColor(31, 13, 31))
  fileColor = maybe(fileColor, QColor(0, 0, 0))
  rankColor = maybe(rankColor, QColor(0, 0, 0, ))
  fontFamily = maybe(fontFamily, 'Courier')
  fontSize = maybe(fontSize, 16)
  font = QFont()
  font.setFamily(fontFamily)
  font.setPointSize(fontSize)

  ic(lightColor, darkColor)
  sideLength = imageSize // 10
  boardSize = sideLength * 10
  pixmap = QPixmap(boardSize, boardSize)
  pixmap.fill(QColor(223, 223, 255))
  painter = QPainter(pixmap)
  centerFlag = Qt.AlignmentFlag.AlignCenter
  rect = None
  brush = QBrush()
  brush.setStyle(Qt.BrushStyle.SolidPattern)
  pen = QPen()
  pen.setStyle(Qt.PenStyle.SolidLine)
  pen.setColor(QColor(0, 0, 0, ))
  painter.setPen(pen)
  painter.setBrush(brush)
  painter.setFont(font)
  coords = {}

  squareSize = QSize(sideLength, sideLength)
  # Draw the squares
  X = stringList(' , a, b, c, d, e, f, g, h,  ')
  # X = [x for x in X if x in 'abcdefgh']
  Y = stringList(' , 1, 2, 3, 4, 5, 6, 7, 8,  ')
  # Y = [y for y in Y if y in '12345678']
  print(X, Y)
  for (i, x) in enumerate(X):
    for (j, y) in enumerate(Y):
      point = QPoint(sideLength * i, sideLength * j)
      rect = QRect(point, squareSize)
      if i % 9 and j % 9:
        coords |= {'%s %s' % (x, y): rect}
        color = lightColor if (i + j) % 2 else darkColor
        painter.fillRect(rect, color)
      elif not i % 9:
        painter.drawText(rect, centerFlag, '%s' % (y))
      elif not j % 9:
        painter.drawText(rect, centerFlag, '%s' % (x))

  painter.end()

  return (pixmap, coords)


class StaticBoard(LayoutWidget):
  """Static Board widget"""

  def __init__(self, *args, **kwargs) -> None:
    LayoutWidget.__init__(self, *args, **kwargs)
    colorArgs = maybeTypes(QColor, *args, padLen=4, padChar=None)
    intArgs = maybeTypes(int, *args, padLen=2, padChar=None)
    imageSizeKeys = ['imageSize', 'sideLength', 'side']
    imageSizeKwarg = searchKeys(*imageSizeKeys) @ int >> kwargs
    fontFamilyKeys = ['font', 'family', 'fontFamily']
    fontFamilyKwarg = searchKeys(*fontFamilyKeys) @ str >> kwargs
    fontFamilyArg = maybeType(str, *args)
    fontFamilyDefault = 'Courier'
    fontFamily = maybe(fontFamilyKwarg, fontFamilyArg, fontFamilyDefault)
    fontSizeKeys = ['font', 'fontSize', 'pointSize']
    fontSizeKwarg = searchKeys(*fontSizeKeys) @ str >> kwargs
    fontSizeArg, imageSizeArg = intArgs
    imageSizeDefault = 320
    imageSize = maybe(imageSizeKwarg, imageSizeArg, imageSizeDefault)
    fontSizeDefault = 16
    fontSize = maybe(fontSizeKwarg, fontSizeArg, fontSizeDefault)
    self._font = QFont()
    self._font.setFamily(fontFamily)
    self._font.setPointSize(fontSize)
    lightColorKwarg = searchKeys('light', 'white') @ QColor >> kwargs
    darkColorKwarg = searchKeys('dark', 'black') @ QColor >> kwargs
    fileColorKwarg = searchKeys('file', 'fileColor') @ QColor >> kwargs
    rankColorKwarg = searchKeys('rank', 'rankColor') @ QColor >> kwargs
    fileColorArg, rankColorArg, lightColorArg, darkColorArg = colorArgs
    fileColorDefault = QColor(0, 0, 31)
    rankColorDefault = QColor(31, 0, 0)
    darkColorDefault = QColor(15, 15, 15)
    lightColorDefault = QColor(191, 191, 191)
    rankColor = maybe(rankColorKwarg, rankColorArg, rankColorDefault)
    fileColor = maybe(fileColorKwarg, fileColorArg, fileColorDefault)
    lightColor = maybe(lightColorKwarg, lightColorArg, lightColorDefault)
    darkColor = maybe(darkColorKwarg, darkColorArg, darkColorDefault)
    self._pix, self._coords = staticBoard(imageSize,
                                          fontFamily,
                                          fontSize,
                                          lightColor,
                                          darkColor,
                                          fileColor,
                                          rankColor)

    if not isinstance(self._pix, QPixmap):
      e = """Expected pix to be of type QPixmap, but received %s"""
      raise TypeError(e % type(self._pix))

  def _getCoords(self) -> dict[str, QPoint]:
    """Getter-function for the coordinates dictionary"""
    return self._coords

  def _getPixmap(self) -> QPixmap:
    """Getter-function for the QPixmap"""
    return self._pix

  def _setPixmap(self, *_) -> NoReturn:
    """Illegal setter-function"""
    raise TypeError('Read Only Variable')

  def _delPixmap(self) -> NoReturn:
    """Illegal deleter-function"""
    raise TypeError('Read Only Variable')

  pixmap = property(_getPixmap, _setPixmap, _delPixmap)

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementation"""
    p = QPainter()
    p.begin(self)
    viewRect = p.viewport()
    viewSideLength = min([viewRect.height(), viewRect.width()])
    targetSize = QSize(viewSideLength, viewSideLength)
    origin = QPoint()
    targetRect = QRect(origin, targetSize) - QMargins(2, 2, 2, 2, )
    targetRect.moveCenter(viewRect.center())
    sourceRect = self.pix.rect()
    p.drawPixmap(targetRect, self.pix, sourceRect)
    p.end()

  pix = property(_getPixmap, _setPixmap, _delPixmap)
