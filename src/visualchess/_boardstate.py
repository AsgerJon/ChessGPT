"""BoardState describes a present state of a game"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import NoReturn

from PySide6.QtCore import QRect, QRectF
from icecream import ic
from pygments.lexers import pawn
from worktoy.stringtools import stringList
from worktoy.typetools import TypeBag
from worktoy.waitaminute import UnexpectedStateError

from visualchess import ChessPiece, Square, ChessColor, PieceType
from visualchess._boardstateproperties import _BoardStateProperties
from visualchess.chesspieces import initialPosition

ic.configureOutput(includeContext=True)

Rect = TypeBag(QRectF, QRect)
PositionList = list[list[str]]

debugPosition = [
  stringList('E8, black, king'),
  stringList('E1, white, king'),
]


class BoardState(_BoardStateProperties):
  """BoardState represents a chess board with each squared occupied by a
  member, possibly the empty one, of the Piece Enum."""

  @classmethod
  def readList(cls, positionList: PositionList) -> BoardState:
    """Creates an instance with pieces as defined in the given list"""
    instance = cls()
    instance.updatePositionFromList(positionList)
    return instance

  @classmethod
  def InitialPosition(cls) -> BoardState:
    """Creates an instance with the starting position"""
    return cls.readList(initialPosition)

  def __init__(self, *args, **kwargs) -> None:
    _BoardStateProperties.__init__(self, *args, **kwargs)

  def getPiece(self, square: Square) -> ChessPiece:
    """Getter-function for the piece on the given square"""
    piece = self._contents.get(square, None)
    if piece is not None:
      if isinstance(piece, ChessPiece):
        return piece
      raise TypeError
    os.abort()
    raise UnexpectedStateError

  def setPiece(self, square: Square, piece: ChessPiece) -> NoReturn:
    """Setter-function for the piece on the given square"""
    if piece is not None:
      if isinstance(piece, ChessPiece):
        self._contents[square] = piece
      else:
        raise TypeError
    else:
      raise UnexpectedStateError

  def delPiece(self, square: Square) -> ChessPiece:
    """Deleter-function for the given square. This removes the piece from
    it. Invoking the deleter returns the chess piece"""
    piece = self.getPiece(square)
    self.setPiece(square, ChessPiece.EMPTY)
    return piece

  def clearPosition(self) -> NoReturn:
    """Clears the position by setting all squares to empty"""
    for square in Square:
      self.setPiece(square, ChessPiece.EMPTY)

  def updatePositionFromList(self, positionList: PositionList) -> NoReturn:
    """Updates the position from the list """
    self.clearPosition()
    for line in positionList:
      square = Square.fromStr(line[0])
      colorDict = dict(white=ChessColor.WHITE, black=ChessColor.BLACK)
      color = colorDict.get(line[1], None)
      pieceTypeDict = dict(pawn=PieceType.PAWN, knight=PieceType.KNIGHT,
                           bishop=PieceType.BISHOP, rook=PieceType.ROOK,
                           queen=PieceType.QUEEN, king=PieceType.KING)
      piece = pieceTypeDict.get(line[2], None)
      if color is None or piece is None:
        raise KeyError
      piece = ChessPiece.fromColorPiece(color, piece)
      self[square] = piece
