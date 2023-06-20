"""RegularMove subclasses ChessMove and defines a regular move"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import NoReturn

from icecream import ic

from visualchess import ChessMove, ChessPiece

ic.configureOutput(includeContext=True)


class RegularMove(ChessMove):
  """RegularMove subclasses ChessMove and defines a regular move
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    ChessMove.__init__(self, *args, **kwargs)

  def applyMove(self, *args, **kwargs) -> NoReturn:
    """Implementation of the method applying the move"""
    self.state.setPiece(self.state.grabbedSquare, ChessPiece.EMPTY)
    self.state.setPiece(self.state.hoverSquare, self.state.grabbedPiece)

  @abstractmethod
  def validateMove(self, *args, **kwargs) -> bool:
    """Validation is left to subclasses."""
