"""PawnMove subclasses ChessMove"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import NoReturn

from icecream import ic

from visualchess import ChessMove, ChessColor, Square, ChessPiece, \
  StateChange

ic.configureOutput(includeContext=True)


class PawnMove(ChessMove):
  """PawnMove subclasses ChessMove
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    ChessMove.__init__(self, *args, **kwargs)

  def pieceCompatibility(self, *args, **kwargs) -> bool:
    """This abstract method determines if the source piece is of a piece
    type supported by the subclass"""
    return True if self.sourcePiece.isPawn else False

  def baseValidation(self, *args, **kwargs) -> bool:
    """Reimplementation of the special pawn behaviour"""
    dx = abs(self.sourceX - self.targetX)
    dy = abs(self.sourceY - self.targetY)
    if dx == 1 and dy == 1:
      ic()
      if self.sourceColor == self.targetColor:
        return False
      if self.sourceColor == ~self.targetColor:
        return True
      return False
    if dx:
      return False
    if dy > 2:
      return False
    return True

  def isMovePossible(self, *args, **kwargs) -> bool:
    """Checks if the pawn is possible. Please note that this is piece
    color dependant. This method implements the pawn specific behaviour of
    capturing only diagonally and that these moves are available only for
    capture."""
    r = -1 if self.sourceColor is ChessColor.WHITE else 1
    minusCapture = Square.fromInts(self.sourceX - 1, self.sourceY + r)
    oneStep = Square.fromInts(self.sourceX, self.sourceY + r)
    twoStep = Square.fromInts(self.sourceX, self.sourceY + 2 * r)
    plusCapture = Square.fromInts(self.sourceX + 1, self.sourceY + r)
    if self.targetSquare in [minusCapture, oneStep, twoStep, plusCapture]:
      return True
    return False

  def obstructSquares(self, *args, **kwargs) -> list[Square]:
    """Reimplementation of the special pawn behaviour"""
    r = -1 if self.sourceColor is ChessColor.WHITE else 1
    oneStep = Square.fromInts(self.sourceX, self.sourceY + r)
    twoStep = Square.fromInts(self.sourceX, self.sourceY + 2 * r)
    return [oneStep, twoStep]

  def updateBoardState(self) -> list[StateChange]:
    """Places the king at the target square"""
    if abs(self.sourceY - self.targetY) == 2:
      self.state.enPassantFile = self.sourceFile
    out = [self.state.setPiece(self.targetSquare, self.sourcePiece),
           self.state.setPiece(self.sourceSquare, ChessPiece.EMPTY)]
    return out
