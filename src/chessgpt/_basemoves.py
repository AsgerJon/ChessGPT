"""BaseMoves are the relative squares that would be available to a given
piece type without any restrictions."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import NoReturn, Never

from icecream import ic
from worktoy.core import maybe
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError

from visualchess import Square, BoardState, Move

ic.configureOutput(includeContext=True)


class BaseMoves:
  """BaseMoves are the relative squares that would be available to a given
  piece type without any restrictions. Please note that pawns are special
  and their subclass basically must reimplement every method."""

  @staticmethod
  def parseArguments(*args, **kwargs) -> BoardState:
    """Parses arguments to the board state"""
    keys = stringList('boardState, board, state, chessboard')
    boardState, args, kwargs = extractArg(BoardState, keys, *args, **kwargs)
    return boardState

  def __init__(self, *args, **kwargs) -> None:
    self._boardState = self.parseArguments(*args, **kwargs)

  def _createBoardState(self, boardState: BoardState = None) -> NoReturn:
    """Creator-function for the board state"""
    _boardState = maybe(boardState, BoardState())
    if isinstance(_boardState, BoardState):
      self._boardState = _boardState
    else:
      msg = """Expected board state to be of type %s, but received %s!"""
      raise TypeError(msg % (BoardState, type(_boardState)))

  def _getBoardState(self) -> BoardState:
    if self._boardState is None:
      self._createBoardState()
      return self._getBoardState()
    if isinstance(self._boardState, BoardState):
      return self._boardState
    msg = """Expected board state to be of type %s but received %s!"""
    raise TypeError(msg % (BoardState, type(self._boardState)))

  @abstractmethod
  def getBaseMoves(self) -> list[tuple[int, int]]:
    """Getter-function for the squares available without any restrictions.
    Subclasses must implement this method."""

  def pathRestrict(self, square: Square, move: Move) -> list[Square]:
    """Collects all the moves until a non empty square is reached."""

  def _noSet(self, *_) -> Never:
    """Illegal Accessor Function"""
    raise ReadOnlyError('boardState')

  board = property(_getBoardState, _noSet, _noSet)
