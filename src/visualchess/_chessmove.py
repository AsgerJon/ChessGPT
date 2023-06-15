"""ChessMove instances represent a single chess move. It provides rule
logic and triggers relevant functions"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn
from warnings import warn

from icecream import ic
from worktoy.core import plenty
from worktoy.parsing import maybeTypes, maybeType

from moreworktoy import ArgumentError
from visualchess import Square, DebugState, BoardState, PieceType, ChessColor

ic.configureOutput(includeContext=True)


class ChessMove:
  """ChessMove instances represent a single chess move. It provides rule
  logic and triggers relevant functions
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args) -> None:
    squares = maybeTypes(Square, *args, padLen=2, padChar=None)
    if not plenty(squares):
      raise ArgumentError('squares')
    self._origin, self._target = squares
    self._pieceType = maybeType(PieceType, *args)
    self._chessColor = maybeType(ChessColor, *args)

  def validate(self) -> bool:
    """Validates the move. If the move fails to validate then no board
    state will allow the move. Validated moves are possible for certain
    board states. """
