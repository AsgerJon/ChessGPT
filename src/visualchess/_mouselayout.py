"""PieceLayout subclasses BoardLayout and adds chess piece rendering"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtGui import QPaintEvent, QPainter
from icecream import ic

from visualchess import BoardLayout, Square, BoardState, ChessPiece
from workstyle.stylesettings import hoveredSquareStyle

ic.configureOutput(includeContext=True)


class _MouseLayoutProperties(BoardLayout):
  """PieceLayout subclasses BoardLayout and adds chess piece rendering.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    BoardLayout.__init__(self, *args, **kwargs)
    self._boardState = None
    self._hoverSquare = None
    self._hoverPiece = None

  #########################################################################
  ################### Accessor Functions for Chess Board ##################
  def _createBoardState(self) -> bool:
    """Creator-function for BoardState instance"""
    self._boardState = BoardState.InitialPosition()
    if isinstance(self._boardState, BoardState):
      return True
    raise TypeError

  def getBoardState(self) -> BoardState:
    """Getter-function for board state"""
    if self._boardState is None:
      if self._createBoardState():
        return self.getBoardState()
    if isinstance(self._boardState, BoardState):
      return self._boardState
    raise TypeError

  ############### END OF Accessor Functions for Chess Board ###############
  ######################### Hover square accessors ########################
  def getHoverSquare(self) -> Square:
    """Getter-function for hovered rectangle"""
    return self._hoverSquare

  def setHoverSquare(self, square: Square) -> NoReturn:
    """Setter-function for hovered rectangle"""
    if self._hoverSquare == square:
      return
    self._hoverSquare = square

  def delHoverSquare(self) -> NoReturn:
    """Deleter-function for the hovered rectangle"""
    if self._hoverSquare:
      self._hoverSquare = None

  ##################### END of Hover square accessors #####################
  # --------------------------------------------------------------------- #
  ######################### Hover piece Accessors #########################
  def getHoverPiece(self) -> object:
    """Getter-function for hover piece"""
    return self._hoverPiece

  def setHoverPiece(self, hoverPiece: ChessPiece) -> NoReturn:
    """Setter-function for hover piece"""
    if hoverPiece == self._hoverPiece:
      return
    self._hoverPiece = hoverPiece

  def delHoverPiece(self) -> NoReturn:
    """Deleter-function for hover piece"""
    if self._hoverPiece:
      self._hoverPiece = None

  ###################### END of Hover piece accessors #####################
  #########################################################################


class MouseLayout(_MouseLayoutProperties):
  """The mouse layout subclass of piece layout brings mouse functionality."""

  def __init__(self, *args, **kwargs) -> None:
    _MouseLayoutProperties.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)

  ################## Reimplementation of QWidget Events  ##################

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """The MouseLayout subclass provides the painting of chess pieces and
    the hovering functionality."""
    BoardLayout.paintEvent(self, event)
    painter = QPainter()
    painter.begin(self)
    if self.getHoverSquare():
      hoveredSquareStyle @ painter
      painter.drawRect(self.getHoverSquare() @ self.getBoardRect())
    for (square, piece) in self.getBoardState().items():
      if isinstance(square, Square):
        target = square @ self.getBoardRect()
        if isinstance(piece, ChessPiece):
          if piece:
            pix = piece.getPixmap()
            source = pix.rect().toRectF()
            painter.drawPixmap(target, pix, source)
    painter.end()

  ########################### END OF MouseLayout ##########################
  #########################################################################
