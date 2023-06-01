"""The load function loads the images module like"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os
from typing import TYPE_CHECKING
from PIL import Image, ImageQt
from PySide6.QtGui import QPixmap
from icecream import ic

if TYPE_CHECKING:
  from visualchess import Piece, ChessColor

ic.configureOutput(includeContext=True)


class Load:
  """Load contains the images of a chess set the images module like"""

  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen
  _here = os.path.abspath(__file__)
  _imageRoot = os.path.join(_here, 'images')

  @classmethod
  def getImageFolder(cls) -> str:
    """Getter-function for image folder"""
    return cls._imageRoot

  def __init__(self, piece: Piece, sideColor: ChessColor) -> None:
    self._piece = piece
    self._sideColor = sideColor
    self._imageFid = piece + sideColor

  def getImageFileName(self) -> str:
    """Getter-function for image file name"""
    return self._imageFid

  def getImageFilePath(self) -> str:
    """Getter-function for full path to image file"""
    return os.path.join(self._imageRoot, self._imageFid)

  def loadPiecePIL(self, ) -> Image.Image:
    """The loadPiece function is responsible for loading images,
    in particular chess pieces, to instances of QPixmap which may then be
    inserted by the rest of the PySide6 widget framework"""
    #  MIT Licence
    #  Copyright (c) 2023 Asger Jon Vistisen
    with Image.open(self.getImageFilePath()) as image:
      return image

  def loadPieceImageQt(self, ) -> ImageQt:
    """As ImageQt"""
    return ImageQt.ImageQt(self.loadPiecePIL())

  def loadPieceQPixmap(self) -> QPixmap:
    """As QPixmap"""
    return QPixmap(self.loadPieceImageQt())
