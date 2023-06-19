"""ChessMove is a class specifying the type of move about to be applied"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import NoReturn, TYPE_CHECKING

from icecream import ic
from worktoy.core import plenty

from visualchess import Square
from visualchess._chessmoveproperties import _ChessMoveProperties

if TYPE_CHECKING:
  from visualchess import BoardState

ic.configureOutput(includeContext=True)


class ChessMove(_ChessMoveProperties):
  """ChessMove is a class specifying the type of move about to be applied
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    _ChessMoveProperties.__init__(self, *args, **kwargs)

  def __str__(self, ) -> str:
    """String Representation"""
    return 'ChessMove'

  def __repr__(self, ) -> str:
    """Code Representation"""
    return 'ChessMove(\'...\')'

  @abstractmethod
  def pieceCompatibility(self, *args, **kwargs) -> bool:
    """This abstract method determines if the source piece is of a piece
    type supported by the subclass"""

  @abstractmethod
  def isMovePossible(self, *args, **kwargs) -> bool:
    """This abstract method determines if the proposed move would be a
    valid instance of the present subclass. Suggested moves for which
    this method returns False may still be possible, just not as an
    instance of this class. Subclasses must implement this method."""

  def obstructSquares(self, *args, **kwargs) -> list[Square]:
    """Returns a list of the squares the piece travel through during the
    move and which must be empty."""
    out = []
    dx = abs(self.sourceX - self.targetX)
    dy = abs(self.sourceY - self.targetY)
    if (dx - dy) * dx * dy:
      return []
    x0, y0 = self.sourceX, self.sourceY
    d = max(dx, dy)
    rx = self.state.sign(self.sourceX - self.targetX)
    ry = self.state.sign(self.sourceY - self.targetY)
    for i in range(1, d):
      out.append(Square.fromInts(x0 + rx * i, y0 + ry * i))
    return out

  @abstractmethod
  def updateBoardState(self, *args, **kwargs) -> BoardState:
    """This abstract method defines how the board should be updated if
    this move is validated. Subclasses must implement this method.
    Promotion of pawn logic should be implemented in this method."""

  def kingChecked(self, *args, **kwargs) -> bool:
    """Return True if king is checked"""
    return True if self.state.colorKingCheck(self.sourceColor) else False

  def baseValidation(self, *args, **kwargs) -> bool:
    """This method validates that sufficient piece information is
    available and that the move is not capturing a piece of same color as
    the capturing piece. Subclasses having implemented the abstract
    methods will not receive moves that fail this basic validation. Unless
    the subclass directly reimplements this method."""
    self._updateMove(*args, **kwargs)
    if not plenty(self.sourceSquare,
                  self.sourcePiece,
                  self.targetSquare,
                  self.targetPiece):
      return False  # Ensures that all are not None
    if not all([self.sourceSquare, self.sourcePiece, self.targetSquare]):
      return False  # Ensures that required information is present
    if self.sourceColor == self.targetColor:
      return False  # Prevents capture of same color.

  def applyMove(self, *args, **kwargs) -> bool:
    """This method applies the move to the board, if it passes validation"""
    if not self.pieceCompatibility(*args, **kwargs):
      return False
    if not self.kingChecked(*args, **kwargs):
      return False
    if not self.baseValidation(*args, **kwargs):
      return False
    if not self.isMovePossible(*args, **kwargs):
      return False
    for square in self.obstructSquares(*args, **kwargs):
      if self.state.getPiece(square):
        return False
    self.updateBoardState(*args, **kwargs)
    return True
