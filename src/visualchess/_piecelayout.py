"""PieceLayout subclasses BoardLayout and adds chess piece rendering"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtGui import QPaintEvent, QPainter
from icecream import ic

from visualchess import BoardLayout, Square, BoardState, ChessPiece

ic.configureOutput(includeContext=True)


class PieceLayout(BoardLayout):
  """PieceLayout subclasses BoardLayout and adds chess piece rendering.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    BoardLayout.__init__(self, *args, **kwargs)
    self._boardState = BoardState.InitialPosition()

  def getBoardState(self) -> BoardState:
    """Getter-function for board state"""
    return self._boardState

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Re implementation of the paint event"""
    BoardLayout.paintEvent(self, event)
    painter = QPainter()
    painter.begin(self)
    for (square, piece) in self.getBoardState().items():
      if isinstance(square, Square):
        target = square @ self.getBoardRect()
        if isinstance(piece, ChessPiece):
          if piece:
            pix = piece.pixMap()
            source = pix.rect().toRectF()
            painter.drawPixmap(target, pix, source)
    painter.end()
