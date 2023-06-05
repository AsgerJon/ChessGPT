"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Signal
from icecream import ic

from visualchess import BoardLayout, ChessPiece, Square

ic.configureOutput(includeContext=True)


class _BoardMouseProperties(BoardLayout):
  """Property class"""

  enterBoardRect = Signal()
  leaveBoardRect = Signal()
  changedHoverSquare = Signal(Square)
  clearedHoverSquare = Signal()
  changedHoverPiece = Signal(ChessPiece)

  def __init__(self, *args, **kwargs) -> None:
    BoardLayout.__init__(self, *args, **kwargs)
    self._hoverBoard = None
    self._hoverSquare = None
    self._hoverPiece = None

  def getHoverSquare(self) -> Square:
    """Getter-function for the hovered square"""
    if isinstance(self._hoverSquare, Square):
      return self._hoverSquare

  def setHoverSquare(self, square: Square) -> NoReturn:
    """Setter-function for the hovered square"""
    if isinstance(square, Square):
      if self._hoverSquare == square:
        return
      self._hoverSquare = square
      self.changedHoverSquare.emit(square)

  def delHoverSquare(self) -> NoReturn:
    """Deleter-function for the hovered square"""
    self._hoverSquare = None
    self.clearedHoverSquare.emit()

  def getHoverPiece(self) -> ChessPiece:
    """Getter-function for the chess piece currently hovered"""
    return self._hoverPiece

  def setHoverPiece(self, piece: ChessPiece) -> NoReturn:
    """Setter-function for the chess piece currently hovered"""
    if isinstance(piece, ChessPiece):
      if piece == self._hoverPiece:
        return
      self._hoverPiece = piece
      self.changedHoverPiece.emit(piece)

  def getHoverBoard(self) -> bool:
    """Getter-function for board hover flag. This flag indicates that the
    mouse cursor is hovering within the chess squares."""
    return True if self._hoverBoard else False

  def setHoverBoard(self, hover: bool) -> NoReturn:
    """Setter-function for board hover flag."""
    if self._hoverBoard ^ hover:
      self._hoverBoard = True if hover else False
      if hover:
        self.enterBoardRect.emit()
      else:
        self.leaveBoardRect.emit()

  def activateHoverBoard(self) -> NoReturn:
    """Sets the board hover flag to True"""
    self._hoverBoard = True
    self.enterBoardRect.emit()

  def deActivateHoverBoard(self) -> NoReturn:
    """Sets the board hover flag to False"""
    self._hoverBoard = False
    self.leaveBoardRect.emit()
