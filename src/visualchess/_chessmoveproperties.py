"""_ChessMoveProperties provides the properties used by the ChessMove
class."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn, Never, TYPE_CHECKING

from icecream import ic
from worktoy.core import maybe
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError

from visualchess import Square, ChessPiece, Move, ChessColor, File, Rank

if TYPE_CHECKING:
  from visualchess import BoardState

ic.configureOutput(includeContext=True)


class _ChessMoveProperties:
  """_ChessMoveProperties provides the properties used by the ChessMove
  class.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @staticmethod
  def _parseArguments(*args, **kwargs) -> tuple[str, BoardState]:
    """Parses given arguments to instance name"""
    nameKey = stringList('name, title, moveName')
    stateKey = stringList('state, boardState, game, current')
    name, args, kwargs = extractArg(str, nameKey, *args, **kwargs)
    boardState, a, k = extractArg(BoardState, stateKey, *args, *kwargs)
    boardState = maybe(boardState, None)
    if not isinstance(name, str):
      msg = """Expected argument name 'name' to be of type '%s', 
      but received '%s' of type '%s'!"""
      raise TypeError(msg % (str, name, type(name)))
    if boardState is not None:
      if not isinstance(boardState, BoardState):
        msg = """Expected argument name 'boardState' to be of type '%s', 
        but received '%s' of type '%s'!"""
        raise TypeError(msg % (BoardState, name, type(BoardState)))
    return name, boardState

  def __init__(self, *args, **kwargs) -> None:
    _name, _state = self._parseArguments(*args, **kwargs)
    self._name = _name
    self._boardState = _state
    self._move = None
    self.updateMove(*args, **kwargs)

  def _getName(self, ) -> str:
    """Getter-function for name"""
    if isinstance(self._name, str):
      return self._name
    msg = """Expected private variable '_name' to be of type '%s', 
    but received '%s' of type '%s'!"""
    raise TypeError(msg % (str, self._name, type(self._name)))

  def _getBoardState(self, ) -> BoardState:
    """Getter-function for board state"""
    if isinstance(self._boardState, BoardState):
      return self._boardState

  def _setMove(self, move: Move) -> NoReturn:
    """Setter-function for the move variable"""
    if isinstance(move, Move):
      self._move = move

  def _delMove(self) -> NoReturn:
    """Deleter function for the move. """
    self._move = None

  def _getMove(self, ) -> Move:
    """Getter-function for the move variable"""
    if self._move is None:
      return self.state.move
    if isinstance(self._move, Move):
      return self._move
    raise TypeError

  def _updateMove(self, *args, **kwargs) -> NoReturn:
    """Creates an instance of 'Move' from the given argument. Then this
    instance is set as the private variable '_move' on the 'ChessMove'
    instance. """
    self._move = Move(*args, **kwargs)

  def _getSourceSquare(self) -> Square:
    """Getter-function for the source square"""
    if self.move is not None:
      if isinstance(self.move, Move):
        sourceSquare = self.move.sourceSquare
        if sourceSquare is not None:
          if isinstance(sourceSquare, Square):
            return sourceSquare
    if isinstance(self.state.grabbedSquare, Square):
      return self.state.grabbedSquare

  def _getSourceFile(self) -> File:
    """Getter-function for the source file"""
    return self._getSourceSquare().file

  def _getSourceRank(self) -> Rank:
    """Getter-function for the source rank"""
    return self._getSourceSquare().rank

  def _getSourceX(self) -> int:
    """Getter-function for integer value of source file"""
    return self._getSourceFile().value

  def _getSourceY(self) -> int:
    """Getter-function for integer value of source rank"""
    return self._getSourceSquare().value

  def _getTargetSquare(self) -> Square:
    """Getter-function for the target square"""
    if self.move is not None:
      if isinstance(self.move, Move):
        targetSquare = self.move.targetSquare
        if targetSquare is not None:
          if isinstance(targetSquare, Square):
            return targetSquare
    if isinstance(self.state.hoverSquare, Square):
      return self.state.hoverSquare

  def _getTargetFile(self) -> File:
    """Getter-function for the target file"""
    return self._getTargetSquare().file

  def _getTargetRank(self) -> Rank:
    """Getter-function for the target rank"""
    return self._getTargetSquare().rank

  def _getTargetX(self) -> int:
    """Getter-function for integer value of target file"""
    return self._getTargetFile().value

  def _getTargetY(self) -> int:
    """Getter-function for integer value of target rank"""
    return self._getTargetRank().value

  def _getSourcePiece(self) -> ChessPiece:
    """Getter-function for the source piece"""
    if self.move is not None:
      if isinstance(self.move, Move):
        sourcePiece = self.move.sourcePiece
        if sourcePiece is not None:
          if isinstance(sourcePiece, ChessPiece):
            return sourcePiece
    if isinstance(self.state.grabbedPiece, ChessPiece):
      return self.state.grabbedPiece

  def _getTargetPiece(self) -> ChessPiece:
    """Getter-function for the source square"""
    if self.move is not None:
      if isinstance(self.move, Move):
        targetPiece = self.move.targetPiece
        if targetPiece is not None:
          if isinstance(targetPiece, ChessPiece):
            return targetPiece
    if isinstance(self.state.hoverPiece, ChessPiece):
      return self.state.hoverPiece

  def _getSourceColor(self) -> ChessColor:
    """Getter-function for source color"""
    if self.move is not None:
      if isinstance(self.move, Move):
        sourcePiece = self.move.sourcePiece
        if sourcePiece is not None:
          if isinstance(sourcePiece, ChessPiece):
            if isinstance(sourcePiece.color, ChessColor):
              return sourcePiece.color
    if isinstance(self.state.grabbedColor, ChessColor):
      return self.state.grabbedColor
    raise TypeError

  def _getTargetColor(self) -> ChessColor:
    """Getter-function for target color"""
    if self.move is not None:
      if isinstance(self.move, Move):
        targetPiece = self.move.targetPiece
        if targetPiece is not None:
          if isinstance(targetPiece, ChessPiece):
            if isinstance(targetPiece.color, ChessColor):
              return targetPiece.color
    if isinstance(self.state.hoverColor, ChessColor):
      return self.state.hoverColor
    raise TypeError

  def _noAcc(self, *_) -> Never:
    """General Illegal Accessor Function"""
    raise ReadOnlyError('Attempted to access general illegal accessor!')

  name = property(_getName, _noAcc, _noAcc)
  state = property(_getBoardState, _noAcc, _noAcc)
  move = property(_getMove, _setMove, _noAcc)
  sourceSquare = property(_getSourceSquare, _noAcc, _noAcc)
  sourceFile = property(_getSourceFile, _noAcc, _noAcc)
  sourceX = property(_getSourceX, _noAcc, _noAcc)
  sourceY = property(_getSourceY, _noAcc, _noAcc)
  sourceRank = property(_getSourceRank, _noAcc, _noAcc)
  sourcePiece = property(_getSourcePiece, _noAcc, _noAcc)
  sourceColor = property(_getSourceColor, _noAcc, _noAcc)
  targetSquare = property(_getTargetSquare, _noAcc, _noAcc)
  targetFile = property(_getTargetFile, _noAcc, _noAcc)
  targetRank = property(_getTargetRank, _noAcc, _noAcc)
  targetX = property(_getTargetX, _noAcc, _noAcc)
  targetY = property(_getTargetY, _noAcc, _noAcc)
  targetPiece = property(_getTargetPiece, _noAcc, _noAcc)
  targetColor = property(_getTargetColor, _noAcc, _noAcc)
