"""SquarePaint is responsible for applying painting operations on the
StaticBoard on a square by square basis"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Slot, QRectF, QSizeF, QSize
from PySide6.QtGui import QPaintEvent, QPainter

from visualchess import ChessColor, Piece, Square
from visualchess.chesspieces import Load
from workstyle import WhereMouse
from workstyle.styles import BezelStyle, BoardDims, GridStyle


class SquarePaint(WhereMouse):
  """SquarePaint is responsible for applying painting operations on the
  StaticBoard on a square by square basis.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @staticmethod
  def fitSquareRect(rect: QRectF) -> QRectF:
    """Returns the largest square QRectF that fits in rect"""
    dim = min(rect.width(), rect.height())
    size = QSizeF(dim, dim)
    squareRect = QRectF(BoardDims.origin, size)
    squareRect.moveCenter(rect.center())
    return squareRect

  @staticmethod
  def fitSquareMarginsRect(rect: QRectF) -> QRectF:
    """Returns the largest square QRectF that fits in given rect with the
    style margins deducted"""
    marginLeft = BoardDims.marginLeft
    marginTop = BoardDims.marginTop
    marginRight = BoardDims.marginRight
    marginBottom = BoardDims.marginBottom
    rect.adjust(marginLeft, marginTop, -marginRight, -marginBottom)
    return SquarePaint.fitSquareRect(rect)

  def __init__(self, *args, **kwargs) -> None:
    WhereMouse.__init__(self, *args, **kwargs)
    self._pixMaps = None
    self.setMinimumSize(QSize(400, 400))

  #
  # @Slot(str, str)
  # def applyMove(self) -> NoReturn:
  #   """Triggers repaint updating chess position"""
  #
  # def _collectPixMaps(self) -> NoReturn:
  #   """Loads all pix maps"""
  #   self._pixMaps = {}
  #   for piece in Piece:
  #     for color in ChessColor:
  #       key = (color, piece)
  #       val = Load(piece, color).loadPieceQPixmap()
  #       if isinstance(self._pixMaps, dict):
  #         self._pixMaps |= {key: val}
  #       else:
  #         raise TypeError

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """First calls the parent paintEvent before applying the context
    specific operation"""
    painter = QPainter()
    painter.begin(self)
    BezelStyle @ painter
    rX, rY = BoardDims.cornerRadiusX, BoardDims.cornerRadiusY
    painter.drawRoundedRect(self.fitSquareRect(painter.viewport()), rX, rY, )
    GridStyle @ painter
    boardRect = self.fitSquareMarginsRect(painter.viewport())
    painter.drawRect(boardRect)
    for square in Square:
      square.applyPaint(painter)
    painter.end()
