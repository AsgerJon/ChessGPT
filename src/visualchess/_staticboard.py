"""StaticBoard draws the chessboard"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import time
from typing import NoReturn

from PySide6.QtCore import QSize, QPointF, QRectF, Qt, Signal, QSizeF, QRect
from PySide6.QtGui import QPaintEvent, QPainter, QResizeEvent
from icecream import ic
from worktoy.core import maybe

from visualchess import chessBoardFunc, Rank, File
from workstyle import WhereMouse
from workstyle.styles import BezelStyle, GridStyle, LightSquareStyle, \
  DarkSquareStyle, FileRankStyle, HoverStyle

ic.configureOutput(includeContext=True)

Labels = list[tuple[QRectF, QRectF, str]]


class StaticBoard(WhereMouse):
  """StaticBoard draws the chessboard
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  hoverSquare = Signal(File, Rank)
  boardSize = Signal(QSizeF)

  def __init__(self, *args, **kwargs) -> None:
    WhereMouse.__init__(self, *args, **kwargs)
    self._baseSize = QSize(400, 400)
    self.setMinimumSize(self._baseSize)
    self._allowResize = True
    self._fixedSize = QSize(400, 400)
    self._boardRect = None
    self._borderWidth = None
    self._square = None
    self._rank = None
    self._file = None
    self._hover = None
    self._hoverRects = None
    self.move.connect(self._handleMouseMove)
    self.enter.connect(self._handleMouseMove)
    self.leave.connect(self._handleMouseLeave)
    #  Styles
    self._lightSquareStyle = LightSquareStyle
    self._darkSquareStyle = DarkSquareStyle
    self._bezelStyle = BezelStyle
    self._gridStyle = GridStyle
    self._fileRankStyle = FileRankStyle
    self._hoverStyle = HoverStyle
    #  From chessBoardFunc
    self._bezelRect = None
    self._boardRect = None
    self._lightSquares = None
    self._darkSquares = None
    self._fileRects = None
    self._rankRects = None
    self._squares = []

  def _getBoard(self, rect: QRectF = None) -> NoReturn:
    """Updates the geometric information"""
    viewPort = maybe(rect, self.visibleRegion().boundingRect())
    if isinstance(viewPort, QRect):
      viewPort = viewPort.toRectF()
    if isinstance(viewPort, QRectF):
      res = chessBoardFunc(viewPort)
    else:
      raise TypeError
    self._bezelRect = res.get('bezelRect', None)
    self._boardRect = res.get('boardRect', None)
    self._lightSquares = res.get('light', None)
    self._darkSquares = res.get('dark', None)
    self._fileRects = res.get('files', None)
    self._rankRects = res.get('ranks', None)
    self._squares = []
    for light, dark in zip(self._lightSquares, self._darkSquares):
      self._squares.append(light)
      self._squares.append(dark)

  def _getBezelRect(self) -> QRectF:
    """Getter-Function for the QRectF including the surrounding bezels"""
    if self._bezelRect is None:
      self._getBoard()
      return self._getBezelRect()
    return self._bezelRect

  def _getBoardRect(self) -> QRectF:
    """Getter-Function for the QRectF including only the squares
    themselves"""
    if self._boardRect is None:
      self._getBoard()
      return self._getBoardRect()
    return self._boardRect

  def _getLightSquares(self) -> Labels:
    if self._lightSquares is None:
      self._getBoard()
      return self._getLightSquares()
    return self._lightSquares

  def _getDarkSquares(self) -> Labels:
    if self._darkSquares is None:
      self._getBoard()
      return self._getDarkSquares()
    return self._darkSquares

  def _getFileRects(self) -> list[QRectF]:
    """Getter-function for list of files"""
    if self._fileRects is None:
      self._getBoard()
      return self._getFileRects()
    return self._fileRects

  def _getRankRects(self) -> list[QRectF]:
    """Getter-function for list of ranks"""
    if self._rankRects is None:
      self._getBoard()
      return self._getRankRects()
    return self._rankRects

  def _handleMouseLeave(self) -> NoReturn:
    """Handles mouse leave"""
    self._file = None
    self._rank = None
    self._square = None
    self._hoverRects = None
    self.repaint()

  def _handleMouseMove(self, point: QPointF) -> NoReturn:
    """Handles mouse moves"""
    self._point = point
    if self._boardRect is None:
      return
    left, right, = self._boardRect.left(), self._boardRect.right()
    top, bottom = self._boardRect.top(), self._boardRect.bottom()
    width, height = self._boardRect.width(), self._boardRect.height()
    x, y = self._point.x(), self._point.y()
    if left < x < right and top < y < bottom:
      squareWidth, squareHeight = width / 8, height / 8
      _file = File.find(int((x - left) // squareWidth) + 1)
      _rank = Rank.find(int(8 - (y - top) // squareHeight))
      if self._file == _file:
        self._rank = _rank
        self.hoverSquare.emit(_file, _rank)
      else:
        self._file = _file
        self.hoverSquare.emit(_file, _rank)
      size = QSizeF(squareWidth, squareHeight)
      xHover = left + (_file.value - 1) * squareWidth
      yHover = top + (8 - _rank.value) * squareHeight
      topLeft = QPointF(xHover, yHover)
      hoverRect = QRectF(topLeft, size)
      self._setHoverRects(hoverRect)
    else:
      self._setHoverRects(QRectF())

  def _setHoverRects(self, hoverRect: QRectF) -> NoReturn:
    """Setter-function for hovered rectangle"""
    hoverRects = [hoverRect]
    self._hoverRects = hoverRect
    bezelRect, boardRect = self._bezelRect, self._boardRect
    leftLeft = bezelRect.left()
    leftRight = boardRect.left()
    rightLeft = boardRect.right()
    rightRight = bezelRect.right()
    topTop = bezelRect.top()
    topBottom = boardRect.top()
    bottomTop = boardRect.bottom()
    bottomBottom = bezelRect.bottom()
    #  Left Rank
    rankLeftTopLeft = QPointF(leftLeft, hoverRect.top())
    rankLeftBottomRight = QPointF(leftRight, hoverRect.bottom())
    leftRank = QRectF(rankLeftTopLeft, rankLeftBottomRight)
    hoverRects.append(leftRank)
    #  Right Rank
    rankRightTopLeft = QPointF(rightLeft, hoverRect.top())
    rankRightBottomRight = QPointF(rightRight, hoverRect.bottom())
    rightRank = QRectF(rankRightTopLeft, rankRightBottomRight)
    hoverRects.append(rightRank)
    self._hoverRects = hoverRects
    #  Top File
    fileTopTopLeft = QPointF(hoverRect.left(), topTop)
    fileTopBottomRight = QPointF(hoverRect.right(), topBottom)
    topFile = QRectF(fileTopTopLeft, fileTopBottomRight)
    hoverRects.append(topFile)
    #  Bottom File
    fileBottomTopLeft = QPointF(hoverRect.left(), bottomTop)
    fileBottomBottomRight = QPointF(hoverRect.right(), bottomBottom)
    bottomFile = QRectF(fileBottomTopLeft, fileBottomBottomRight)
    hoverRects.append(bottomFile)
    self._hoverRects = hoverRects
    return self.repaint()

  def _getHoverRects(self, ) -> list[QRectF]:
    """Getter-function for hovered rectangle"""
    if isinstance(self._hoverRects, list):
      if all([isinstance(h, QRectF) for h in self._hoverRects]):
        return self._hoverRects
    return [QRectF()]

  def lockSize(self) -> NoReturn:
    """Method locking the widget at its present size"""
    self._fixedSize = self.geometry().size()
    self._allowResize = False

  def unlockSize(self) -> NoReturn:
    """Method unlocking the widget allowing resizing"""
    self.setMinimumSize(self._baseSize)
    self._allowResize = True

  def getFile(self) -> File:
    """Getter-function for file"""
    return self._file

  def getRank(self) -> Rank:
    """Getter-function for rank"""
    return self._rank

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementing the paint event"""
    painter = QPainter()
    painter.begin(self)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    fixedRect = QRectF(QPointF(0., 0.), self._fixedSize)
    rect = painter.viewport() if self._allowResize else fixedRect
    self._getBoard(rect)
    self._bezelStyle @ painter
    painter.drawRoundedRect(self._getBezelRect(), 4, 4, )
    self._gridStyle @ painter
    painter.drawRect(self._getBoardRect())
    self._lightSquareStyle @ painter
    painter.drawRects(self._getLightSquares())
    self._darkSquareStyle @ painter
    painter.drawRects(self._getDarkSquares())
    centerFlag = Qt.AlignmentFlag.AlignCenter
    FileRankStyle @ painter
    for file in self._getFileRects():
      painter.drawText(file[0], centerFlag, file[2])
      painter.drawText(file[1], centerFlag, file[2])
    for rank in self._getRankRects():
      painter.drawText(rank[0], centerFlag, rank[2])
      painter.drawText(rank[1], centerFlag, rank[2])
    painter.end()

  def resizeEvent(self, event: QResizeEvent) -> NoReturn:
    """Implementation triggering the resize signal"""
    WhereMouse.resizeEvent(self, event)
    self.boardSize.emit(event.size())
