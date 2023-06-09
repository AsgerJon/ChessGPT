"""ChessMoves is a class describes the moves available to different chess
pieces."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn, Never

from icecream import ic
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList
from worktoy.waitaminute import ReadOnlyError

from moreworktoy import Iterify
from visualchess import ChessPiece, BoardState

ic.configureOutput(includeContext=True)


class ChessMoves(Iterify):
  """ChessMoves is a class describes the moves available to different chess
  pieces.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @classmethod
  def createAll(cls, *args) -> NoReturn:
    """Creates an instance for each chess piece"""

  @classmethod
  def __old__(cls, *args, **kwargs) -> NoReturn:
    """Attempts to find an existing instance"""

  @staticmethod
  def parseArguments(*args, **kwargs) -> ChessPiece:
    """Parses the given arguments"""
    pieceKeys = stringList('piece, chessPiece, pieceType, type_, type')
    piece, a, k = extractArg(ChessPiece, pieceKeys, *args, **kwargs)
    if isinstance(piece, ChessPiece):
      return piece
    raise TypeError

  def __init__(self, *args, **kwargs) -> None:
    self._piece = ChessMoves.parseArguments(*args, **kwargs)

  def getPiece(self) -> ChessPiece:
    """Getter-function for the matching chess piece"""
    if isinstance(self._piece, ChessPiece):
      return self._piece
    raise TypeError

  def setPiece(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('piece')

  def delPiece(self, ) -> Never:
    """Illegal deleter function"""
    raise ReadOnlyError('piece')

  def getName(self) -> str:
    """Getter-function for the name of the name"""
    return self.piece.name

  def setName(self, *_) -> Never:
    """Illegal setter function"""
    raise ReadOnlyError('name')

  def delName(self, ) -> Never:
    """Illegal deleter function"""
    raise ReadOnlyError('name')

  def __str__(self) -> str:
    """String Representation"""
    return """Chess Moves for .%s""" % self.name

  def __repr__(self) -> str:
    """Code Representation"""
    return """ChessMoves(%s)""" % self.piece

  def __call__(self, boardState: BoardState) -> NoReturn:
    """Triggers the sound effect"""
    raise NotImplementedError('yolo!')

  piece = property(getPiece, setPiece, setPiece)
  name = property(getName, setName, delName)
