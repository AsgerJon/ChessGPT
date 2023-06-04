"""PieceView is responsible for painting pieces."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn, TYPE_CHECKING

from PySide6.QtCore import QRectF
from PySide6.QtGui import QPixmap, QPaintEvent, QPainter
from icecream import ic
from worktoy.core import plenty
from worktoy.parsing import maybeType

from visualchess import ChessColor, Rank, File, Piece, loadPiece, \
  BoardState, \
  Square, ChessPiece

from workstyle.shapesettings import ShapeSettings

if TYPE_CHECKING:
  from visualchess import BoardWidget

ic.configureOutput(includeContext=True)


class PieceView:
  """PieceView is responsible for painting pieces.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @staticmethod
  def getViewPort() -> QRectF:
    """Getter-function for the active viewport"""
    return ShapeSettings.getViewPort()

  @staticmethod
  def getPiecePixmap(*args) -> QPixmap:
    """Getter-function for QPixmap representation of chess piece"""
    chessColor = maybeType(ChessColor, *args)
    piece = maybeType(Piece, *args)
    if isinstance(piece, Piece) and isinstance(chessColor, ChessColor):
      return loadPiece(piece, chessColor)

  def __init__(self, parent: BoardWidget, *args, **kwargs) -> None:
    self._parent = parent

  def debug(self) -> NoReturn:
    """Debugger"""
    print('pieceView debug')
    # for (key, val) in self.getBoardState().getContents().items():
    #   print(key, val)
    #   print(type(key), type(val))
    #   break

  def getParent(self) -> BoardWidget:
    """Getter-function of the parent"""
    return self._parent

  def setParent(self, parent: BoardWidget) -> NoReturn:
    """Setter-function of the parent"""
    self._parent = parent

  def getBoardState(self) -> BoardState:
    """Getter-function for parent BoardState"""
    return self.getParent().getBoardState()

  def collectTargetRect(self, *args, ) -> QRectF:
    """Paints a defined piece at a given square"""
    square = maybeType(Square, *args)
    if square is None:
      file = maybeType(File, *args)
      rank = maybeType(Rank, *args)
    if isinstance(square, Square):
      file, rank = square.getFile(), square.getRank()
      if isinstance(file, File) and isinstance(rank, Rank):
        return self.getParent().getBoardView().getSquareRect(file, rank)

  def ready(self, *args) -> NoReturn:
    """Applies the pixmap to the rectangle"""
    chessColor = maybeType(ChessColor, *args)
    piece = maybeType(Piece, *args)
    file = maybeType(File, *args)
    rank = maybeType(Rank, *args)
    pix = self.getPiecePixmap(piece, chessColor)
    rect = self.collectTargetRect(file, rank)
    self.getParent().update(rect, )

  def __call__(self, painter: QPainter) -> NoReturn:
    """Receives the active painter and places pieces"""
    for (square, chessPiece) in self.getBoardState().getContents().items():
      pix, target = None, None
      if chessPiece:
        if isinstance(square, Square):
          target = self.collectTargetRect(square)
        if isinstance(chessPiece, ChessPiece):
          pix = chessPiece.getPixmap()
        if not plenty(target, pix):
          raise TypeError
        source = pix.rect().toRectF()
        if isinstance(target, QRectF):
          if isinstance(pix, QPixmap):
            if isinstance(source, QRectF):
              painter.drawPixmap(target, pix, source)
