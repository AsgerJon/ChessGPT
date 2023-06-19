"""BoardState describes a present state of a game"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import NoReturn

from PySide6.QtCore import QRect, QRectF
from icecream import ic
from worktoy.core import plenty, maybe
from worktoy.parsing import maybeTypes, maybeType
from worktoy.stringtools import stringList, monoSpace
from worktoy.typetools import TypeBag
from worktoy.waitaminute import UnexpectedStateError

from visualchess import ChessPiece, Square, ChessColor, Rank, File, \
  PieceType, Castle, ChessMove, EmptyMove, PawnMove, BishopMove, \
  KnightMove, \
  RookMove, QueenMove, KingMove, EnPassantMove, QueenSideCastle, \
  KingSideCastle, ChessAudio, StateChange
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

  _whitePawnMoves = [(0, -1), (-1, -1), (1, -1), (0, -2)]
  _blackPawnMoves = [(0, 1), (-1, 1), (1, 1), (0, 2)]
  _typeMoves = {
    PieceType.EMPTY : [EmptyMove, ],
    PieceType.PAWN  : [PawnMove, EnPassantMove],
    PieceType.KNIGHT: [KnightMove, ],
    PieceType.BISHOP: [BishopMove, ],
    PieceType.ROOK  : [RookMove, ],
    PieceType.QUEEN : [QueenMove, ],
    PieceType.KING  : [KingMove, KingSideCastle, QueenSideCastle],
  }

  @classmethod
  def getTypeMoves(cls) -> dict[PieceType, list]:
    """Getter-function for type to move dictionary"""
    return cls._typeMoves

  @classmethod
  def getChessMoves(cls, *args) -> list[ChessMove]:
    """Getter-function for the chess move class appropriate for the given
    piece type"""
    pieceType = maybeType(PieceType, *args)
    chessPiece = maybeType(ChessPiece, *args)
    if pieceType is None:
      if chessPiece is not None:
        if isinstance(chessPiece, ChessPiece):
          return cls.getChessMoves(chessPiece.piece)
    if isinstance(pieceType, PieceType):
      out = cls.getTypeMoves().get(pieceType, EmptyMove)
      if isinstance(out, list):
        return out
      raise TypeError

  @staticmethod
  def sign(n: int) -> int:
    """Implementation of signum. 0 is returned for 0."""
    return 0 if not n else (1 if n > 0 else -1)

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
    _BoardStateProperties.__init__(self)
    self._movedRooks = []
    self._movedKings = []

  def setColorRookMoved(self, *args) -> NoReturn:
    """Setter-function for the moved flag of the rook with color and file as
    indicated"""
    file = maybeType(File, *args)
    color = maybeType(ChessColor, *args)
    if not plenty(file, color):
      raise ValueError('missing file or color!')
    if isinstance(file, File) and isinstance(color, ChessColor):
      self._movedRooks.append(frozenset([file, color]))

  def getColorRookMoved(self, *args) -> bool:
    """Getter-function for the moved flag of the rook with color and file
    as indicated"""
    file = maybeType(File, *args)
    color = maybeType(ChessColor, *args)
    if not plenty(file, color):
      raise ValueError('missing file or color!')
    if isinstance(file, File) and isinstance(color, ChessColor):
      return True if frozenset([file, color]) in self._movedRooks else False
    raise TypeError

  def setColorKingMoved(self, chessColor: ChessColor) -> NoReturn:
    """Adds the king of given color to the list of moved kings."""
    self._movedKings.append(chessColor)

  def getColorKingMoved(self, chessColor: ChessColor) -> NoReturn:
    """Gets the moved flag of the king of the color indicated"""
    return True if chessColor in self._movedKings else False

  def getColorKingSquare(self, chessColor: ChessColor) -> Square:
    """Getter-function for the square occupied by the king of the given
    color"""
    for square in Square:
      piece = self.getPiece(square)
      if piece.piece is PieceType.KING and piece.color is chessColor:
        return square
    return Square.NULL

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
    stateChange = StateChange(square, self.getPiece(square), piece)
    if piece is not None:
      if isinstance(piece, ChessPiece):
        self._contents[square] = piece
        return stateChange
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

  def cancelMove(self, ) -> NoReturn:
    """This method instead moves the grabbed piece back to grabbed square"""
    if self.grabbedPiece and self.grabbedSquare:
      self.setPiece(self.grabbedSquare, self.grabbedPiece)
      # self.soundCancelMove.play()
    self.grabbedSquare, self.grabbedPiece = Square.NULL, ChessPiece.EMPTY

  def squaresPiecesColor(self, chessColor: ChessColor) -> AllColor:
    """Returns a list of tuples with square and piece where the piece is
    of the color indicated."""
    out = []
    for square in Square:
      piece = self.getPiece(square)
      if piece:
        if piece.color is chessColor:
          out.append((square, piece))
    return out

  def getColorReach(self, chessColor: ChessColor) -> list[Square]:
    """Getter-function for all squares reachable by a piece of the given
    color"""
    out, sourceSquare, sourcePiece = [], None, None
    colorSquares = self.squaresPiecesColor(chessColor)
    for (sourceSquare, sourcePiece) in colorSquares:
      for targetSquare in Square:
        if sourceSquare is not targetSquare:
          targetPiece = self.getPiece(targetSquare)
          if self.validateMove(
              sourceSquare, targetSquare, sourcePiece, targetPiece):
            out.append(targetSquare)
    return out

  def validateMove(self, *args, ) -> bool:
    """Validates move"""
    squares = maybeTypes(Square, *args, padLen=2, padChar=None)
    pieces = maybeTypes(ChessPiece, *args, padLen=2, padChar=None)
    sourceSquare = self.grabbedSquare
    targetSquare = self.hoverSquare
    sourcePiece = self.grabbedPiece
    targetPiece = self.hoverPiece
    if plenty(*squares) and plenty(*pieces):
      sourceSquare, targetSquare = squares
      sourcePiece, targetPiece = pieces
    if not isinstance(sourceSquare, Square):
      return False
    if not isinstance(targetSquare, Square):
      return False
    if not isinstance(sourcePiece, ChessPiece):
      return False
    if not isinstance(targetPiece, ChessPiece):
      return False
    chessMoves = self.getChessMoves(self.grabbedPiece)
    for item in chessMoves:
      chessMove = item(self)
      if chessMove.applyMove():
        return True
    return False

  def colorKingCheck(self, *args) -> bool:
    """Getter-function for flag indicating that the king of the given
    color is in check"""
    chessColor = maybeType(ChessColor, *args)
    if not isinstance(chessColor, ChessColor):
      raise TypeError
    square = maybeType(Square, *args)
    square = maybe(square, self.getColorKingSquare(chessColor))
    if chessColor is ChessColor.NULL:
      raise ValueError('NULL color has no king!')
    otherColorReach = self.getColorReach(~chessColor)
    return True if square in otherColorReach else False

  def applyMove(self, ) -> NoReturn:
    """Moves grabbed piece to the hovered square if validated."""
    self.validateMove()

  def __str__(self) -> str:
    """String Representation"""
    out = ''
    for rank in Rank:
      for file in File:
        piece = self.getPiece(file, rank)
        if not piece:
          out += '__'
