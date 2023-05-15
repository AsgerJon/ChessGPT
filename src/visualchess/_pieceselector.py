"""PieceSelector is a subclass of QWidget showing each of the 12 chess
pieces."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtGui import QPixmap
from icecream import ic
from PySide6.QtCore import QSize, QSizeF, Qt
from PySide6.QtWidgets import QLabel, QGridLayout, QWidget
from worktoy import maybeTypes, maybeType, searchKeys, maybe

from visualchess import showPiece
from worktoyside import geometriesF2Int

ic.configureOutput(includeContext=True)


class ChessPiecesWidget(QWidget):
  """PieceSelector is a subclass of QWidget showing each of the 12 chess
  pieces.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @staticmethod
  def pieceFrozenSet(*args) -> frozenset[str, str]:
    """Collects a frozen set of a color and a piece name from positional
    arguments"""
    strArgs = ' '.join(maybeTypes(str, *args))
    pieceName, pieceColor = None, None
    pieceNames = ["king", "queen", "rook", "bishop", "knight", "pawn"]
    for i, color in enumerate(["white", "black"]):
      if color in strArgs and pieceColor is None:
        pieceColor = color
        break
    for name in pieceNames:
      if name in strArgs and pieceName is None:
        pieceName = name
        break
    if pieceColor is None or pieceName is None:
      if pieceColor is None and pieceName is None:
        raise ValueError('Unable to find pieceColor as well as pieceName!')
      if pieceColor is None:
        raise ValueError('Unable to find pieceColor')
      if pieceColor is None:
        raise ValueError('Unable to find pieceName')
    return frozenset([pieceColor, pieceName])

  def __init__(self, parent=None) -> None:
    QWidget.__init__(self, parent)
    # self.setFixedSize(256, 128)
    self.piece_size = QSize(32, 32)
    self.grid_layout = QGridLayout()
    self.setLayout(self.grid_layout)
    self._pixMaps = None

  def createPixmaps(self) -> NoReturn:
    """Creator-function for pixmaps"""
    self._pixMaps = {}
    piece_names = ["king", "queen", "rook", "bishop", "knight", "pawn"]
    for i, color in enumerate(["white", "black"]):
      for j, name in enumerate(piece_names):
        key = frozenset([color, name])
        self._pixMaps |= {key: showPiece(color, name)}

  def getPixmap(self, *args, **kwargs) -> QPixmap:
    """Getter-function for the QPixmap at name, color and size (optional)"""
    pieceId = self.pieceFrozenSet(*args, )
    pix = self._pixMaps.get(pieceId, None)
    if pix is None:
      raise ValueError('Could not find pixmap on: %s' % (pieceId))
    sizeKwarg = searchKeys('size', ) @ QSize >> kwargs
    sizeFKwarg = searchKeys('size', ) @ QSizeF >> kwargs
    sizeArg = maybeType(QSize, *args)
    sizeFArg = maybeType(QSizeF, *args)
    sizeDefault = None
    size = maybe(sizeKwarg, sizeFKwarg, sizeArg, sizeFArg, sizeDefault)
    if size is None:
      return pix
    size = geometriesF2Int(size)
    return pix.scaled(size, Qt.AspectRatioMode.KeepAspectRatio)

  def setupWidgets(self) -> NoReturn:
    """Sets up the widgets"""

  def minimumSizeHint(self) -> QSize:
    """Minimum size required to show 12 pix maps """

  def setPixmaps(self) -> NoReturn:
    """Setter-function for the pix map"""
    piece_names = ["king", "queen", "rook", "bishop", "knight", "pawn"]
    for i, color in enumerate(["white", "black"]):
      for j, name in enumerate(piece_names):
        pixmap = showPiece(color, name, request=QPixmap)
        label = QLabel(self)
        label.setPixmap(pixmap)
        self.grid_layout.addWidget(label, i, j)
