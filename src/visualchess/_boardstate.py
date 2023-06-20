"""BoardState describes a present state of a game"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import NoReturn

from PySide6.QtCore import QRect, QRectF
from chess import Move, parse_square
from icecream import ic
from worktoy.core import plenty, maybe
from worktoy.parsing import maybeType
from worktoy.stringtools import stringList
from worktoy.typetools import TypeBag
from worktoy.waitaminute import UnexpectedStateError

from visualchess import ChessPiece, Square, ChessColor, Rank, File, \
  PieceType, ChessMove
from visualchess._boardstateproperties import _BoardStateProperties
from visualchess.chesspieces import initialPosition

ic.configureOutput(includeContext=True)

Rect = TypeBag(QRectF, QRect)
PositionList = list[list[str]]
AllColor = list[tuple[Square, ChessPiece]]
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
    _BoardStateProperties.__init__(self)
    self._movedRooks = []
    self._movedKings = []

  def getPiece(self, *args) -> ChessPiece:
    """Getter-function for the piece on the given square"""
    square = maybeType(Square, *args)
    file = maybeType(File, *args)
    rank = maybeType(Rank, *args)
    if isinstance(file, File) and isinstance(rank, Rank):
      square = maybe(square, Square.fromFileRank(file, rank), Square.NULL)
    if not square:
      return ChessPiece.EMPTY
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
      piece = ChessPiece.fromColorPiece(line[1], line[2])
      self[square] = piece

  def resetInitialPosition(self) -> NoReturn:
    """Resets the board to initial position"""
    self.colorTurn = ChessColor.WHITE
    self.updatePositionFromList(initialPosition)
    print('reset!')
    self.board.reset()

  def leaveBoard(self, ) -> NoReturn:
    """Resets move properties"""
    self.hoverPiece = ChessPiece.EMPTY
    self.hoverSquare = Square.NULL
    self.cancelMove()

  def hover(self, square: Square) -> NoReturn:
    """Sets hoverSquare to square"""
    piece = self.getPiece(square)
    if self.hoverSquare != square:
      self.hoverSquare = square
    if self.hoverPiece != self.getPiece(square):
      self.hoverPiece = piece

  def grabPiece(self, ) -> NoReturn:
    """Grabs the hovered piece"""
    if not self.hoverPiece.color == self.colorTurn:
      self.soundIllegalMove.play()
    if self.hoverPiece.color == self.colorTurn:
      if self.hoverPiece and self.hoverSquare:
        self.grabbedPiece = self.hoverPiece
        self.grabbedSquare = self.hoverSquare
        self.delPiece(self.grabbedSquare)
        return True
    return False

  def cancelMove(self, **kwargs) -> NoReturn:
    """This method instead moves the grabbed piece back to grabbed square"""
    if self.grabbedPiece and self.grabbedSquare:
      self.setPiece(self.grabbedSquare, self.grabbedPiece)
      self.soundCancelMove.play()
    self.grabbedSquare, self.grabbedPiece = Square.NULL, ChessPiece.EMPTY
    if self.hoverSquare:
      self.widget.setHoverCursor()
    else:
      self.widget.setNormalCursor()
    self.widget.update()

  def completeMove(self, *args, **kwargs) -> NoReturn:
    """This method completes the move once it has been validated."""
    res = maybeType(int, *args)
    move = maybeType(Move, *args)
    if not isinstance(res, int):
      raise TypeError
    if not isinstance(move, Move):
      raise TypeError
    kingCastle = False if res % 2 else True
    queenCastle = False if res % 3 else True
    enPassant = False if res % 5 else True
    capturedPiece = self.getPiece(self.hoverSquare)
    self.setPiece(self.hoverSquare, self.grabbedPiece)
    self.setPiece(self.grabbedSquare, ChessPiece.EMPTY)
    rookOriginSquare, rookTargetSquare = None, None
    if kingCastle:
      rookOriginSquare = Square.fromFileRank(File.H, self.hoverSquare.rank)
      rookTargetSquare = Square.fromFileRank(File.F, self.hoverSquare.rank)
    if queenCastle:
      rookOriginSquare = Square.fromFileRank(File.A, self.hoverSquare.rank)
      rookTargetSquare = Square.fromFileRank(File.D, self.hoverSquare.rank)
    if kingCastle or queenCastle:
      rookPiece = self.getPiece(rookOriginSquare)
      self.setPiece(rookTargetSquare, rookPiece)
      self.setPiece(rookOriginSquare, ChessPiece.EMPTY)
    if enPassant:
      captureSquare = Square.fromFileRank(
        self.hoverSquare.file, self.grabbedSquare.rank, )
      self.setPiece(captureSquare, ChessPiece.EMPTY)
    self.hoverSquare = self.grabbedSquare
    self.hoverPiece = self.grabbedPiece
    self.grabbedPiece = ChessPiece.EMPTY
    self.grabbedSquare = Square.NULL
    self.toggleTurn()
    self.board.push(move)
    if capturedPiece:
      self.soundAllowedCapture.play()
    else:
      self.soundAllowedMove.play()
    self.widget.update()

  def applyMove(self, ) -> NoReturn:
    """Interfaces with chess package"""
    if self.grabbedSquare == self.hoverSquare:
      ic(self.grabbedSquare, self.hoverSquare)
      return self.cancelMove(sameSquare=True)
    move = self.exportMove()
    res = self.board.validateMove(move)
    if not res % 7:
      return self.completeMove(res, move)
    return self.cancelMove()

  def exportMove(self) -> Move:
    """Creates a move instance from this state. """
    sourceFile = self.grabbedSquare.file.name
    sourceRank = self.grabbedSquare.rank.name
    targetFile = self.hoverSquare.file.name
    targetRank = self.hoverSquare.rank.name
    sourceName = '%s%s' % (sourceFile[0], sourceRank[-1])
    targetName = '%s%s' % (targetFile[0], targetRank[-1])
    sourceSquare = parse_square(sourceName.lower())
    targetSquare = parse_square(targetName.lower())
    return Move(sourceSquare, targetSquare)
