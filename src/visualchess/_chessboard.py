"""ChessBoard reimplements the Board class from python chess"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, TYPE_CHECKING

from chess import Board, Move
from icecream import ic
from worktoy.waitaminute import ReadOnlyError

if TYPE_CHECKING:
  from visualchess import BoardState

ic.configureOutput(includeContext=True)


class ChessBoard(Board):
  """ChessBoard reimplements the Board class from python chess
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, state: BoardState, *args, **kwargs) -> None:
    Board.__init__(self, *args, **kwargs)
    self._state = state
    self._legalMoves = None

  def _getLegalMoves(self) -> list[Move]:
    """Getter-function for list of legal moves"""
    for m in self.generate_legal_moves():
      print(m)
    return [m for m in self.generate_legal_moves()]

  def _getState(self) -> BoardState:
    """Getter-function for board state"""
    return self._state

  def validateMove(self, move: Move) -> int:
    """Validates the potential move from grabbed square to hovered square."""
    out = 1
    out *= (2 if self.is_kingside_castling(move) else 1)
    out *= (3 if self.is_queenside_castling(move) else 1)
    out *= (5 if self.is_en_passant(move) else 1)
    out *= (7 if move in self.legal_moves else 1)
    return out

  def _noAcc(self, *_) -> Never:
    """Illegal Accessor Function"""
    raise ReadOnlyError('General illegal accessor')

  state = property(_getState, _noAcc, _noAcc)
  legalMoves = property(_getLegalMoves, _noAcc, _noAcc)
