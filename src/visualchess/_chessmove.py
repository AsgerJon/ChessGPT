"""ChessMove instances represent a single chess move. It provides rule
logic and triggers relevant functions"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn
from warnings import warn

from icecream import ic

from visualchess import Square, DebugState, BoardState

ic.configureOutput(includeContext=True)


class ChessMove:
  """ChessMove instances represent a single chess move. It provides rule
  logic and triggers relevant functions
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    self._boardState = None

  def _createBoardState(self, ) -> NoReturn:
    """Creator function for the board state"""
    self._boardState = DebugState()

  def _getBoardState(self, ) -> BoardState:
    """Getter-function for the board state"""
    if self._boardState is None:
      self._createBoardState()
      return self._getBoardState()
    if isinstance(self._getBoardState(), (DebugState, BoardState)):
      return self._boardState
    msg = """Expected board state to be of type %s or %s, but received: %s"""
    raise TypeError(msg % (DebugState, BoardState, type(self._boardState)))

  def wouldBeCheck(self, source: Square, target: Square, ) -> NoReturn:
    """This method checks if the given move would leave the active King in
    check. """
    boardState = self._getBoardState()
    movedPiece = boardState.getPiece(source)
    targetPiece = boardState.getPiece(target)
    msg = """Functionality to determine if a move would leave the current 
    king in check is not yet implemented. The current developmental 
    behaviour will always return False such that no move is ever 
    disallowed because of the active king being in check. 
    
    Getting ready to move %s from %s to %s"""
    warn(msg % (movedPiece, source, target))
    return

  def geometryMove(self, source: Square, target: Square) -> NoReturn:
    """This method checks if the piece at square is capable of reach
    target square."""

  def allowMove(self, source: Square, target: Square) -> NoReturn:
    """Without executing the move this method checks if the suggest move
    would be available."""

  def executeMove(self, source: Square, target: Square) -> NoReturn:
    """Executes a move from source to square"""
