#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen

from PIL import Image, ImageQt
from PySide6.QtGui import QPixmap
from visualchess import ChessColor as ChessColor, Piece as Piece


class Load:
  _imageRoot: str

  @classmethod
  def getImageFolder(cls) -> str: ...

  def __init__(self, piece: Piece, sideColor: ChessColor) -> None: ...

  def getImageFileName(self) -> str: ...

  def getImageFilePath(self) -> str: ...

  def loadPiecePIL(self) -> Image.Image: ...

  def loadPieceImageQt(self) -> ImageQt: ...

  def loadPieceQPixmap(self) -> QPixmap: ...
