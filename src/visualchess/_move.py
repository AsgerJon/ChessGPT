"""The Move is a convenience dataclass providing square and piece for
source and target of move. Importantly, this class includes a flexible
parser which may be used directly, but more conveniently by simply
instantiating the class and using the properties of the instance."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from icecream import ic
from worktoy.parsing import extractArg, maybeType
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError

from visualchess import ChessPiece, Square, ChessColor

ic.configureOutput(includeContext=True)


class Move:
  """Dataclass defining square and piece for source and target"""

  @staticmethod
  def parseArguments(*args, **kwargs) -> dict:
    """Parses arguments to square and piece for source and target"""
    baseMove = maybeType(Move, *args, *[v for (k, v) in kwargs.items()])
    if isinstance(baseMove, Move):
      return dict(source=dict(square=baseMove.sourceSquare,
                              piece=baseMove.sourcePiece),
                  target=dict(square=baseMove.targetSquare,
                              piece=baseMove.targetPiece))
    sourceKeys = stringList('origin, source, start')
    targetKeys = stringList('target, capture, goal')
    sourceSquare, a, k = extractArg(Square, sourceKeys, *args, **kwargs)
    sourcePiece, a, k = extractArg(ChessPiece, sourceKeys, *a, **k)
    targetSquare, a, k = extractArg(Square, targetKeys, *a, **k)
    targetPiece, a, k = extractArg(ChessPiece, targetKeys, *a, **k)
    return dict(source=dict(square=sourceSquare, piece=sourcePiece),
                target=dict(square=targetSquare, piece=targetPiece))

  def __init__(self, *args, **kwargs) -> None:
    _data = Move.parseArguments(*args, **kwargs)
    self._sourceSquare = _data['source']['square']
    self._sourcePiece = _data['source']['piece']
    self._targetSquare = _data['target']['square']
    self._targetPiece = _data['target']['piece']

  def _getSourceSquare(self) -> Square:
    """Getter-function for the source square"""
    if isinstance(self._sourceSquare, Square):
      return self._sourceSquare
    return Square.NULL

  def _getTargetSquare(self) -> Square:
    """Getter-function for the target square"""
    if isinstance(self._targetSquare, Square):
      return self._targetSquare
    return Square.NULL

  def _getSourcePiece(self) -> ChessPiece:
    """Getter-function for the source piece"""
    if isinstance(self._sourcePiece, ChessPiece):
      return self._sourcePiece
    return ChessPiece.EMPTY

  def _getTargetPiece(self) -> ChessPiece:
    """Getter-function for the target piece"""
    if isinstance(self._targetPiece, ChessPiece):
      return self._targetPiece
    return ChessPiece.EMPTY

  def _getSourceColor(self) -> ChessColor:
    """Getter-function for the source color"""
    sourcePiece = self._getSourcePiece()
    if not sourcePiece:
      return ChessColor.NULL
    if isinstance(sourcePiece.color, ChessColor):
      return sourcePiece.color
    raise TypeError

  def _getTargetColor(self) -> ChessColor:
    """Getter-function for the target color"""
    targetPiece = self._getTargetPiece()
    if not targetPiece:
      return ChessColor.NULL
    if isinstance(targetPiece.color, ChessColor):
      return targetPiece.color
    raise TypeError

  def __str__(self, ) -> str:
    """String Representation"""
    srcPiece, srcSqr = self.sourcePiece, self.sourceSquare
    tarPiece, tarSqr = self.targetPiece, self.targetSquare
    if self.targetPiece:
      out = 'Moving %s from %s to %s capturing %s'
      return out % (srcPiece, srcSqr, tarSqr, tarPiece)
    out = 'Moving %s from %s to %s'
    return out % (srcPiece, srcSqr, tarSqr)

  def __repr__(self, ) -> str:
    """Code Representation"""
    srcPiece, srcSqr = self.sourcePiece, self.sourceSquare
    tarPiece, tarSqr = self.targetPiece, self.targetSquare
    data = [srcPiece, srcSqr, tarPiece, tarSqr]
    out = 'Move(%s)' % ', '.join(['%s' for i in data if i is not None])
    return out % (*data,)

  def _noAcc(self, *_) -> Never:
    """General Illegal Accessor Function"""
    raise ReadOnlyError('Attempted to access general illegal accessor!')

  sourceSquare = property(_getSourceSquare, _noAcc, _noAcc, )
  targetSquare = property(_getTargetSquare, _noAcc, _noAcc, )
  sourcePiece = property(_getSourcePiece, _noAcc, _noAcc, )
  targetPiece = property(_getTargetPiece, _noAcc, _noAcc, )
  sourceColor = property(_getSourceColor, _noAcc, _noAcc)
  targetColor = property(_getTargetColor, _noAcc, _noAcc)
