"""BoardState describes a present state of a game"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import NoReturn

from PySide6.QtCore import QRect, QRectF
from icecream import ic
from worktoy.typetools import TypeBag
from worktoy.waitaminute import UnexpectedStateError, ProceduralError

from visualchess import ChessPiece, Square, Move
from visualchess.chesspieces import initialPosition

ic.configureOutput(includeContext=True)

Rect = TypeBag(QRectF, QRect)


class BoardState:
    """BoardState represents a chess board with each squared occupied by a
    member, possibly the empty one, of the Piece Enum."""

    @classmethod
    def InitialPosition(cls) -> BoardState:
        """Creates an instance with piece at the starting position"""
        instance = cls()
        for line in initialPosition:
            square = Square.fromStr(line[0])
            piece = ChessPiece.fromColorPiece(line[1], line[2])
            instance[square] = piece
        return instance

    def __init__(self, *args, **kwargs) -> None:
        self._contents = {s: ChessPiece.EMPTY for s in Square}
        self._activeColor = 7

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

    def pieceGuard(self, piece: ChessPiece | str, square: Square) -> bool:
        """This method checks if the given piece is on the given square.
        Please note that this method is color agnostic meaning that it returns
        true regardless of what color the piece is."""
        if isinstance(piece, str):
            raise NotImplementedError
        placedPiece = self.getPiece(square)
        if not placedPiece:
            return False
        return True if piece in [placedPiece, ~placedPiece] else False

    def pieceGuardStrict(self, piece: ChessPiece | str,
                         square: Square) -> bool:
        """This method raises an error if the piece guard fails"""
        if self.pieceGuard(piece, square):
            return True
        actualPiece = self.getPiece(square)
        msg = """Expected piece %s on square %s, but found %s!"""
        raise UnexpectedStateError(msg % (piece, square, actualPiece))

    def getKingSquares(self, square: Square, ) -> list[Square]:
        """Getter-function for the squares reachable by a king on the given
        square. This method raises an exception a king is not on the given
        square.

        Please note that this method will return moves that would put the king
        in check! Such moves a removed by a separate method which removes all
        moves which would put the king in check. This method does remove moves
        that would bring the piece out of bounds."""
        piece, out = self.getPiece(square), []
        self.pieceGuardStrict(ChessPiece.WHITE_KING, square)
        for move in Move.getKingMoves():
            out.append(square + move)
        return [move for move in out if move is not None]

    def getKnightSquares(self, square: Square, ) -> list[Square]:
        """Getter-function for the knight moves. See docstring for king moves."""
        piece, out = self.getPiece(square), []
        self.pieceGuardStrict(ChessPiece.WHITE_KNIGHT, square)
        for move in Move.getKnightMoves():
            out.append(square + move)
        return [move for move in out if move is not None]

    def getRookSquares(self, square: Square, ) -> list[Square]:
        """Getter-function for the squares reachable by a rook from the given
        square. """
        self.pieceGuardStrict(ChessPiece.WHITE_ROOK, square)
        piece, out = self.getPiece(square), []
        for move in Move.getRookMoves():
            movingSquare = square + move
            while not self.getPiece(movingSquare):
                out.append(movingSquare)
                movingSquare += move
            out.append(movingSquare)
        return out

    def getBishopSquares(self, square: Square) -> list[Square]:
        """Getter-function for the squares reachable by rook from the g iven
        square."""
        self.pieceGuardStrict(ChessPiece.WHITE_BISHOP, square)
        piece, out = self.getPiece(square), []
        for move in Move.getBishopMoves():
            movingSquare = square + move
            while not self.getPiece(movingSquare):
                out.append(movingSquare)
                movingSquare += move
            out.append(movingSquare)
        return out

    def getQueenSquares(self, square: Square) -> list[Square]:
        """Getter-function for the squares reachable by rook from the given
        square."""
        self.pieceGuardStrict(ChessPiece.WHITE_QUEEN, square)
        rookMoves = self.getRookSquares()
        bishopMoves = self.getBishopSquares()
        return [*rookMoves, *bishopMoves]

    def getPawnSquares(self, square: Square) -> list[Square]:
        """Getter-function for the squares reachable by a pawn from the given
        square."""
        return []

    def squareMoves(self, square: Square) -> list[Square]:
        """Getter-function for the moves available from the given square"""
        piece = self.getPiece(square)
        if not piece:
            return []
        if piece in ChessPiece.getKings():
            return self.getKingSquares(square)
        if piece in ChessPiece.getKnights():
            return self.getKnightSquares(square)
        if piece in ChessPiece.getBishops():
            return self.getBishopSquares()
        if piece in ChessPiece.getQueens():
            return self.getQueenSquares()
        if piece in ChessPiece.getRooks():
            return self.getRookSquares()
        if piece in ChessPiece.getPawns():
            return self.getPawnSquares()
        raise UnexpectedStateError
