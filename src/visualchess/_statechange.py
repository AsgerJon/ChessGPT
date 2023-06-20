"""StateChange instances represent changes to the state of the game. They
are characterized by the requirement of being reversible. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never, TYPE_CHECKING

from icecream import ic
from worktoy.core import plenty, maybe
from worktoy.parsing import extractArg, maybeType, maybeTypes
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError

from moreworktoy import ArgumentError
from visualchess import Square, ChessPiece, File, Rank, \
  ChessColor, PieceType

if TYPE_CHECKING:
  from visualchess import BoardState

ic.configureOutput(includeContext=True)


class StateChange:
  """StateChange instances represent changes to the state of the game. They
  are characterized by the requirement of being reversible.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @classmethod
  def fromUpdate(cls, *args) -> StateChange:
    """Creates a new instance"""
    square = maybeType(Square, *args)
    pieces = maybeTypes(ChessPiece, *args, padLen=2, padChar=None)
    if not plenty(*pieces):
      raise ArgumentError('ChessPiece')
    return cls(square, *pieces)

  @staticmethod
  def _parseArguments(*args, **kwargs) -> tuple:
    """Parses arguments"""
    squareKeys = stringList('square, position, coordinates')
    square, a, k = extractArg(Square, squareKeys, *args, **kwargs)
    fileKeys = stringList('file, x, column, col, vertical')
    file, a, k = extractArg(File, fileKeys, *a, **k)
    rankKeys = stringList('rank, y, row, horizontal')
    rank, a, k = extractArg(Rank, rankKeys, *a, **k)
    preKeys = stringList('pre, before, old')
    postKeys = stringList('post, after, new')
    prePiece, a, k = extractArg(ChessPiece, preKeys, *a, *k)
    postPiece, a, k = extractArg(ChessPiece, postKeys, *a, *k)
    preColor, a, k = extractArg(ChessColor, preKeys, *a, *k)
    postColor, a, k = extractArg(ChessColor, postKeys, *a, *k)
    preType, a, k = extractArg(PieceType, preKeys, *a, *k)
    postType, a, k = extractArg(PieceType, postKeys, *a, *k)
    squareAlt, prePieceAlt, postPieceAlt = None, None, None
    squareDefault = Square.NULL
    prePieceDefault = ChessPiece.EMPTY
    postPieceDefault = ChessPiece.EMPTY
    if plenty(file, rank):
      if isinstance(file, File) and isinstance(rank, Rank):
        squareAlt = Square.fromFileRank(file, rank)
    if plenty(preType, preColor, postType, postColor):
      if isinstance(preType, PieceType):
        if isinstance(preColor, ChessColor):
          prePieceAlt = ChessPiece.fromColorPiece(preColor, preType)
      if isinstance(postType, PieceType):
        if isinstance(postColor, ChessColor):
          postPieceAlt = ChessPiece.fromColorPiece(postColor, postType)
    square = maybe(square, squareAlt, squareDefault)
    prePiece = maybe(prePiece, prePieceAlt, prePieceDefault)
    postPiece = maybe(postPiece, postPieceAlt, postPieceDefault)
    return (square, prePiece, postPiece)

  def __init__(self, *args, **kwargs) -> None:
    _data = self._parseArguments(*args, **kwargs)
    self._square = _data[0]
    self._prePiece = _data[1]
    self._postPiece = _data[2]

  def _getSquare(self, ) -> Square:
    """Getter-function for square"""
    if isinstance(self._square, Square):
      return self._square
    raise TypeError

  def _getPrePiece(self) -> ChessPiece:
    """Getter-function for chess piece"""
    if isinstance(self._prePiece, ChessPiece):
      return self._prePiece
    raise TypeError

  def _getPostPiece(self) -> ChessPiece:
    """Getter-function for chess piece"""
    if isinstance(self._postPiece, ChessPiece):
      return self._postPiece
    raise TypeError

  def _apply(self, boardState: BoardState) -> BoardState:
    """Applies this statechange"""
    boardState.setPiece(self.square, self.postPiece)
    return boardState

  def _reverse(self, boardState: BoardState) -> BoardState:
    """Reverses this statechange"""
    boardState.setPiece(self.square, self.prePiece)
    return boardState

  def __rshift__(self, other: BoardState) -> BoardState:
    """Alias for _apply"""
    return self._apply(other)

  def __rlshift__(self, other: BoardState) -> BoardState:
    """Alias for _apply"""
    return self._apply(other)

  def __rrshift__(self, other: BoardState) -> BoardState:
    """Alias for _reverse"""
    return self._reverse(other)

  def __lshift__(self, other: BoardState) -> BoardState:
    """Alias for _reverse"""
    return self._reverse(other)

  def _noAcc(self, *_) -> Never:
    """Illegal Accessor Function"""
    raise ReadOnlyError('General illegal accessor')

  square = property(_getSquare, _noAcc, _noAcc)
  prePiece = property(_getPrePiece, _noAcc, _noAcc)
  postPiece = property(_getPostPiece, _noAcc, _noAcc)
