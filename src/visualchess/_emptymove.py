"""Empty is a subclass of ChessMove defining a move that should not be
completed."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from icecream import ic

from visualchess import ChessMove, BoardState

ic.configureOutput(includeContext=True)


class Empty(ChessMove):
  """Empty is a subclass of ChessMove defining a move that should not be
  completed.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  _valid = False

  @classmethod
  def isValid(cls) -> bool:
    """Flag indicated that the move is valid meaning that it should go
    through. """

  def __init__(self, *args, **kwargs) -> None:
    ChessMove.__init__(self, *args, **kwargs)

  def applyMove(self, boardState: BoardState, *args, **kwargs) -> NoReturn:
    """Implementation of the method applying the move"""
    self.state.cancelMove()
