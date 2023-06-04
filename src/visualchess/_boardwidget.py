"""BoardWidget is a subclass showing the chessboard"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from math import floor
from typing import NoReturn

from PySide6.QtCore import QSize, QPointF, QRectF, Signal
from PySide6.QtGui import QPaintEvent, QPainter, QResizeEvent
from icecream import ic

from visualchess import BoardView, Rank, File
from workstyle import WhereMouse

ic.configureOutput(includeContext=True)


class BoardWidget(WhereMouse):
  """BoardWidget is a subclass showing the chessboard
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  resized = Signal(QSize)
  newHover = Signal(File, Rank)

  def __init__(self, *args, **kwargs) -> None:
    WhereMouse.__init__(self, *args, **kwargs)
    self.setMinimumSize(QSize(400, 400))
    self._view = BoardView(self)
    self._view.onUpdate(self.repaint)
    self._rectangles = None
    self._boardRect = None
    self._hoverSquare = None
    self._hoverFile = None
    self._hoverRank = None
    self.move.connect(self._moveHandle)
    self.resized.connect(self._view.setViewSize)
    self.newHover.connect(self._view.setHoverSquare)

  def _moveHandle(self, point: QPointF) -> NoReturn:
    """Handles mouse move events"""
    if not self.getBoardRect().contains(point):
      self._hoverSquare = None
      return
    board = self.getBoardRect()
    mouseX = point.x() - board.left()
    mouseY = point.y() - board.top()
    x = int(mouseX / board.width() * 8)
    y = int(mouseY / board.height() * 8)
    file = File.byValue(x)
    rank = Rank.byValue(y)
    if file == self._hoverFile and rank == self._hoverRank:
      return
    if file is None or rank is None:
      return
    if file is not None:
      self._hoverFile = file
    if rank is not None:
      self._hoverFile, self._hoverRank = file, rank
      self.newHover.emit(file, rank)
    self._hoverSquare = self._view.getSquareRect(file, rank)

  def getBoardRect(self) -> QRectF:
    """Getter-function for board rect"""
    return self._view.getBoardRect()

  def setBoardRect(self, rect: QRectF) -> NoReturn:
    """Setter-function for board rectangle"""
    self._boardRect = rect

  def setRectangles(self, *rects) -> NoReturn:
    """Setter-function for rectangles. Triggered at the end of paint
    event."""
    self._rectangles = [*rects, ]

  def resizeEvent(self, event: QResizeEvent) -> NoReturn:
    """Resizing alerts the board view"""
    self._view.clearHoverSquare()
    self.resized.emit(event.size())
    WhereMouse.resizeEvent(self, event)

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementation"""
    painter = QPainter()
    painter.begin(self)
    self._view(painter)
    painter.end()
