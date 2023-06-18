"""ChessMove is a class specifying the type of move about to be applied"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import NoReturn, Never, TYPE_CHECKING

from icecream import ic
from worktoy.core import maybe, plenty
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError
from visualchess import BoardState, Square, ChessPiece, Move

if TYPE_CHECKING:
  pass

ic.configureOutput(includeContext=True)


class ChessMove:
  """ChessMove is a class specifying the type of move about to be applied
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @staticmethod
  def parseSquaresPieces(*args, **kwargs) -> dict:
    """Parses arguments to square and piece for source and target"""

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
    self._move = Move(*args, **kwargs)

  def __str__(self, ) -> str:
    """String Representation"""
    return 'ChessMove'

  def __repr__(self, ) -> str:
    """Code Representation"""
    return 'ChessMove(\'...\')'

  @abstractmethod
  def applyMove(self, *args, **kwargs) -> NoReturn:
    """This abstract method applies the move represented by the subclass.
    Subclasses must implement this method."""

  @abstractmethod
  def validateMove(self, *args, **kwargs) -> bool:
    """This abstract method determines if a move is valid. It must receive
    valid origin and target squares and pieces either directly from the
    arguments or from the present board state.

    This method validates moves without checking if the move would leave
    own king in check. It is used by the board state logic to determine if
    a move would leave a king in check. """

  def baseValidation(self, *args, **kwargs) -> bool:
    """This method validates that sufficient piece information is
    available and that the move is not capturing a piece of same color as
    the capturing piece. Subclasses must manually invoke this method to
    use it."""
    _data = Move(*args, **kwargs)
    sourcePiece = maybe(_data.sourcePiece, self.state.grabbedPiece)
    sourceSquare = maybe(_data.sourceSquare, self.state.grabbedSquare)
    targetPiece = maybe(_data.targetPiece, self.state.hoverPiece)
    targetSquare = maybe(_data.targetSquare, self.state.hoverSquare)
    if not plenty(sourcePiece, sourceSquare, targetSquare):
      return False
    if isinstance(sourcePiece, ChessPiece):
      if ~sourcePiece.color == self.state.colorTurn:
        return False  # It is the other sides turn
      if isinstance(targetPiece, ChessPiece):
        if sourcePiece.color == targetPiece.color:
          return False
    return True

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

  def _getSourcePiece(self) -> Square:
    """Getter-function for the source piece"""
    if self.move is not None:
      if isinstance(self.move, Move):
        targetSquare = self.move.targetSquare
        if targetSquare is not None:
          if isinstance(targetSquare, Square):
            return targetSquare
    if isinstance(self.state.hoverSquare, Square):
      return self.state.grabbedSquare

  def _getTargetPiece(self) -> Square:
    """Getter-function for the source square"""
    if isinstance(self.state.hoverPiece, ChessPiece):
      return self.state.grabbedSquare

  def _noAcc(self, *_) -> Never:
    """General Illegal Accessor Function"""
    raise ReadOnlyError('Attempted to access general illegal accessor!')

  name = property(_getName, _noAcc, _noAcc)
  state = property(_getBoardState, _noAcc, _noAcc)
  move = property(_getMove, _setMove, _noAcc)
  sourceSquare = property(_getSourceSquare, _noAcc, _noAcc)
  sourcePiece = property(_getSourcePiece, _noAcc, _noAcc)
  targetSquare = property(_getTargetSquare, _noAcc, _noAcc)
  targetPiece = property(_getTargetPiece, _noAcc, _noAcc)
