"""LongCastle subclasses ChessMove"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import NoReturn

from icecream import ic

from visualchess import ChessMove, File, Rank, Square, ChessColor, \
  ChessPiece, PieceType

ic.configureOutput(includeContext=True)


class Castle(ChessMove):
  """LongCastle subclasses ChessMove
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    ChessMove.__init__(self, *args, **kwargs)

  @abstractmethod
  def getRookSquare(self) -> Square:
    """Getter-function for the square holding the rook"""

  def pieceCompatibility(self, *args, **kwargs) -> bool:
    """This abstract method determines if the source piece is of a piece
    type supported by the subclass"""
    rookPiece = self.state.getPiece(self.getRookSquare())
    if rookPiece.piece == PieceType.ROOK:
      if rookPiece.color == self.sourceColor:
        if self.sourcePiece.isKing:
          return True
    return False

  def isMovePossible(self, *args, **kwargs) -> bool:
    """All moves that are no longer than 1 square away from source are
    possible."""
    if not self.sourceRank == self.targetRank:
      return False
    if abs(self.sourceX - self.targetX) in [2, 3]:
      return True
    return False

  def obstructSquares(self, *args, **kwargs) -> list[Square]:
    """Reimplementation support special castling behaviour"""
    r = 1 if self.getRookSquare().file.value > self.sourceX else 1
    fileInts = [self.sourceX + r * i for i in [1, 2]]
    squares = [Square.fromInts(x, self.sourceY) for x in fileInts]
    return squares

  def baseValidation(self, *args, **kwargs) -> bool:
    """Reimplementation support special castling behaviour"""
    if self.state.getColorRookMoved(
        self.getRookSquare().file, self.sourceColor):
      return False
    if self.state.getColorKingMoved(self.sourceColor):
      return False
    if self.state.colorKingCheck(self.sourceColor):
      return False
    stepSquares = self.obstructSquares(*args, **kwargs)
    otherReach = self.state.getColorReach(~self.sourceColor)
    for square in stepSquares:
      if self.state.getPiece(square) or square in otherReach:
        return False
    return True

  @abstractmethod
  def updateBoardState(self, *args, **kwargs) -> NoReturn:
    """Unusual implementation involving the moving of two pieces"""


class QueenSideCastle(Castle):
  """Subclass for long castle"""

  def getRookSquare(self) -> Square:
    """Getter-function for the square holding the rook"""
    rank = Rank.rank1 if self.sourceColor is ChessColor.WHITE else Rank.rank8
    return Square.fromFileRank(File.A, rank)

  def obstructSquares(self, *args, **kwargs) -> list[Square]:
    """Reimplementation support special castling behaviour"""
    rank = Rank.rank1 if self.sourceColor is ChessColor.WHITE else Rank.rank8
    return [Square.fromInts(f, rank.value) for f in [File.D, File.C]]

  def updateBoardState(self, *args, **kwargs) -> NoReturn:
    """Unusual implementation involving the moving of two pieces"""
    rank = Rank.rank1 if self.sourceColor is ChessColor.WHITE else Rank.rank8
    self.state.setPiece(self.targetSquare, self.sourcePiece)
    self.state.setPiece(self.sourceSquare, ChessPiece.EMPTY)
    rookSource = Square.fromFileRank(File.A, rank)
    rookTarget = Square.fromFileRank(File.D, rank)
    rookPiece = ChessPiece.fromColorPiece(self.sourceColor, PieceType.ROOK)
    self.state.setPiece(rookSource, ChessPiece.EMPTY)
    self.state.setPiece(rookTarget, rookPiece)
    self.state.setColorKingMoved(self.sourceColor)
    self.state.setColorRookMoved(self.sourceColor, self.getRookSquare().file)


class KingSideCastle(Castle):
  """Subclass for short castle"""

  def getRookSquare(self) -> Square:
    """Getter-function for the square holding the rook"""
    rank = Rank.rank1 if self.sourceColor is ChessColor.WHITE else Rank.rank8
    return Square.fromFileRank(File.H, rank)

  def obstructSquares(self, *args, **kwargs) -> list[Square]:
    """Reimplementation support special castling behaviour"""
    rank = Rank.rank1 if self.sourceColor is ChessColor.WHITE else Rank.rank8
    return [Square.fromInts(f, rank.value) for f in [File.F, File.G]]

  def updateBoardState(self, *args, **kwargs) -> NoReturn:
    """Unusual implementation involving the moving of two pieces"""
    rank = Rank.rank1 if self.sourceColor is ChessColor.WHITE else Rank.rank8
    self.state.setPiece(self.targetSquare, self.sourcePiece)
    self.state.setPiece(self.sourceSquare, ChessPiece.EMPTY)
    rookSource = Square.fromFileRank(File.H, rank)
    rookTarget = Square.fromFileRank(File.F, rank)
    rookPiece = ChessPiece.fromColorPiece(self.sourceColor, PieceType.ROOK)
    self.state.setPiece(rookSource, ChessPiece.EMPTY)
    self.state.setPiece(rookTarget, rookPiece)
    self.state.setColorKingMoved(self.sourceColor)
    self.state.setColorRookMoved(self.sourceColor, self.getRookSquare().file)
