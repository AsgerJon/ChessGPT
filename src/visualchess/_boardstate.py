"""BoardState describes a present state of a game"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import NoReturn, Never

from PySide6.QtCore import QRect, QRectF
from icecream import ic
from worktoy.stringtools import stringList
from worktoy.typetools import TypeBag
from worktoy.waitaminute import UnexpectedStateError, ReadOnlyError

from visualchess import ChessPiece, Square, ChessColor, Sound
from visualchess.chesspieces import initialPosition

ic.configureOutput(includeContext=True)

Rect = TypeBag(QRectF, QRect)
PositionList = list[list[str]]

debugPosition = [
  stringList('E8, black, king'),
  stringList('E1, white, king'),
]


class BoardState:
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

  @classmethod
  def DebugPosition(cls) -> BoardState:
    """Creates an instance with the debug position"""
    return cls.readList([
      stringList('E1, white, king'),
      stringList('E8, black, king'),
    ])

  def __init__(self, *args, **kwargs) -> None:
    self._contents = {s: ChessPiece.EMPTY for s in Square}
    self._colorTurn = ChessColor.WHITE
    self._enPassant = Square.NULL
    self._grabbedPiece = ChessPiece.EMPTY
    self._grabbedSquare = Square.NULL
    self._hoverSquare = Square.NULL
    self._hoverPiece = ChessPiece.EMPTY

  def __getitem__(self, square: Square) -> ChessPiece:
    """Returns the piece at given square"""
    return self._contents.get(square)

  def __setitem__(self, square: Square, piece: ChessPiece) -> NoReturn:
    """Places given piece and given square"""
    self._contents |= {square: piece}

  def __delitem__(self, square: Square) -> NoReturn:
    """Deletes the item at given square. Deleting means placing the EMPTY
    piece."""
    self._contents |= {square: ChessPiece.EMPTY}

  def keys(self) -> list[Square]:
    """Implementation of keys method"""
    return [key for key in self._contents.keys()]

  def values(self) -> list[ChessPiece]:
    """Implementation of values"""
    return [piece for piece in self._contents.values()]

  def items(self) -> list[tuple[Square, ChessPiece]]:
    """Implementation of items method"""
    return [(k, v) for (k, v) in self._contents.items()]

  def _getGrabbedPiece(self) -> ChessPiece:
    """Getter-function for the grabbed piece"""
    return self._grabbedPiece

  def _setGrabbedPiece(self, chessPiece: ChessPiece) -> NoReturn:
    """Setter-function for the grabbed piece"""
    self._grabbedPiece = chessPiece

  def _getGrabbedSquare(self) -> Square:
    """Getter-function for the grabbed square"""
    return self._grabbedSquare

  def _setGrabbedSquare(self, square: Square) -> NoReturn:
    """Setter-function for the hovered square"""
    self._grabbedSquare = square

  def _getHoverSquare(self) -> Square:
    """Getter-function for the grabbed square"""
    return self._hoverSquare

  def _setHoverSquare(self, square: Square) -> NoReturn:
    """Setter-function for the hovered square"""
    self._hoverSquare = square

  def _getHoverPiece(self) -> ChessPiece:
    """Getter-function for the hovered piece"""
    return self._hoverPiece

  def _setHoverPiece(self, chessPiece: ChessPiece) -> NoReturn:
    """Setter-function for the hovered square"""
    self._hoverPiece = chessPiece

  def _getTurn(self) -> ChessColor:
    """Getter-function for the color whose turn it is."""
    return self._colorTurn

  def _setTurn(self, chessColor: ChessColor) -> NoReturn:
    """Setter-function for the color whose turn it is."""
    self._colorTurn = chessColor

  def toggleTurn(self) -> NoReturn:
    """Toggle-function switching the turn"""
    if self._colorTurn is ChessColor.BLACK:
      self._colorTurn = ChessColor.WHITE
    else:
      self._colorTurn = ChessColor.BLACK

  def _getHoverTurn(self, ) -> bool:
    """Getter-function for hover turn flag. True indicates that the piece
    currently hovered is of the color whose turn it is."""
    if not self.hoverPiece:
      return False
    if self.hoverPiece.color == self.colorTurn:
      return True
    return False

  def getPiece(self, square: Square) -> ChessPiece:
    """Getter-function for the piece on the given square"""
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
    self._enPassant = Square.NULL

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

  def _noAcc(self, *_) -> Never:
    """Illegal Accessor Function"""
    raise ReadOnlyError('General illegal accessor')

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
    if self.hoverPiece.color == self.colorTurn:
      if self.hoverPiece and self.hoverSquare:
        self.grabbedPiece = self.hoverPiece
        self.grabbedSquare = self.hoverSquare
        self.delPiece(self.grabbedSquare)
        return True
    return False

  def cancelMove(self, ) -> NoReturn:
    """This method instead moves the grabbed piece back to grabbed square"""
    if self.grabbedPiece and self.grabbedSquare:
      self.setPiece(self.grabbedSquare, self.grabbedPiece)
      Sound.whoosh.play()
    self.grabbedSquare, self.grabbedPiece = Square.NULL, ChessPiece.EMPTY

  def validateBase(self) -> tuple[int, int]:
    """Base validation"""
    if self.hoverPiece:
      if self.hoverPiece.color == self.grabbedPiece.color:
        Sound.meme_nope.play()
        return (0, 0)
    if self.hoverSquare == self.grabbedSquare:
      return (0, 0)
    if not self.grabbedPiece:
      return (0, 0)
    supremum = self.grabbedSquare - self.hoverSquare
    infimum = self.grabbedSquare * self.hoverSquare
    if isinstance(supremum, int) and isinstance(infimum, int):
      return (supremum, infimum)

  def validateKingMove(self) -> bool:
    """Validates a king move"""
    supremum, infimum = self.validateBase()
    if not supremum * infimum:
      return False
    if self.grabbedPiece.isKing:
      if supremum < 2:
        return True
      return False
    msg = """validator expected King, but received grabbed piece: %s!"""
    raise ValueError(msg % self.grabbedPiece.piece)

  def validateKnightMove(self) -> bool:
    """Validates a knight move"""
    supremum, infimum = self.validateBase()
    if not supremum * infimum:
      return False
    if self.grabbedPiece.isKnight:
      if supremum == 2 and infimum == 1:
        return True
      return False

  def validateBishopMove(self) -> bool:
    """Validates a bishop move"""
    supremum, infimum = self.validateBase()
    if self.grabbedPiece.isBishop:
      if abs(supremum) == abs(infimum):
        if abs(supremum) == 1:
          return True
        x0, y0 = self.grabbedSquare.file.value, self.grabbedSquare.rank.value
        x1, y1 = self.hoverSquare.file.value, self.hoverSquare.rank.value
        distX, distY = x1 - x0, y1 - y0
        dx = int(distX / max(abs(distX), 1))
        dy = int(distY / max(abs(distY), 1))
        for i in range(1, abs(supremum)):
          pathSquare = Square.fromInts(x0 + i * dx, y0 + i * dy)
          if self.getPiece(pathSquare):
            return False
      elif abs(supremum) - abs(infimum):
        return False

  def validateRookMove(self) -> bool:
    """Validates a rook move"""
    supremum, infimum = self.validateBase()
    if self.grabbedPiece.isQueen:
      return True

  def validateQueenMove(self) -> bool:
    """Validates a queen move"""
    return self.validateBishopMove() or self.validateRookMove()

  def validatePawnMove(self) -> bool:
    """Validates a pawn move"""
    supremum, infimum = self.validateBase()
    if self.grabbedPiece.isPawn:
      return True

  def validateMove(self) -> bool:
    """This method checks if moving grabbed Piece to hoverSquare is
    allowable."""
    supremum, infimum = self.validateBase()
    if not supremum * infimum:
      return False
    if self.grabbedPiece.isKing:
      return self.validateKingMove()
    if self.grabbedPiece.isKnight:
      return self.validateKnightMove()
    if self.grabbedPiece.isBishop:
      return self.validateBishopMove()
    if self.grabbedPiece.isRook:
      return self.validateRookMove()
    if self.grabbedPiece.isQueen:
      return self.validateQueenMove()
    if self.grabbedPiece.isPawn:
      return self.validatePawnMove()
    return True

  def applyMove(self, ) -> NoReturn:
    """Moves grabbed piece to the hovered square if validated."""
    if self.validateMove():
      if self.hoverPiece:
        Sound.gotcha.play()
      self.setPiece(self.hoverSquare, self.grabbedPiece)
      self.grabbedPiece = ChessPiece.EMPTY
      self.grabbedSquare = Square.NULL
      self.toggleTurn()
      Sound.move.play()
      return True
    self.cancelMove()
    return False

  def _getMoves(self) -> list:
    """Getter-function for all available moves. """

  grabbedPiece = property(_getGrabbedPiece, _setGrabbedPiece, _noAcc)
  grabbedSquare = property(_getGrabbedSquare, _setGrabbedSquare, _noAcc)
  hoverSquare = property(_getHoverSquare, _setHoverSquare, _noAcc)
  hoverPiece = property(_getHoverPiece, _setHoverPiece, _noAcc)
  colorTurn = property(_getTurn, _setTurn, _noAcc)
  hoverTurn = property(_getHoverTurn, _noAcc, _noAcc)
