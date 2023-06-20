"""ChessMove is a class specifying the type of move about to be applied"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

import chess
from chess import Move
from icecream import ic
from worktoy.parsing import maybeTypes

from visualchess import Square, ChessPiece

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class ChessMove:
  """ChessMove is a class specifying the type of move about to be applied
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    squares = maybeTypes(Square, *args, padLen=2, padChar=None)
    pieces = maybeTypes(ChessPiece, *args, padLen=2, padChar=None)
    self._sourceSquare, self._targetSquare = squares
    self._sourcePiece, self._targetPiece = pieces
    self._kingSideCastling = None
    self._queenSideCastling = None

  def __str__(self) -> str:
    """String representation usable by chess python package"""

  def validate(self, validation: bool) -> NoReturn:
    """Validation setter"""
    # self._valid = True if validation else False
    # self._kingSideCastling = chess.Board.is_kingside_castling(board, move)
    # self._queenSideCastling = chess.Board.is_queenside_castling(board,
    # move)
