"""The showPiece function loads up an image of the requested piece"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import os.path
from typing import Any

from PIL import ImageQt, Image
from PySide6.QtGui import QPixmap, QImage
from worktoy import maybeType, searchKeys, maybe

from moreworktoy import loadPIL
from visualchess import parsePiece


def showPiece(*args, **kwargs) -> Any:
  """The showPiece function loads up an image of the requested piece
  #  MIT License
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  pieceColor, pieceName = parsePiece(*args)
  imageName = None
  here = os.path.dirname(os.path.abspath(__file__))
  imageFolder = os.path.join(here, 'images')
  for imageName in os.listdir(imageFolder):
    if pieceColor in imageName and pieceName in imageName:
      imageName = os.path.basename(os.path.abspath(imageName))
      break
  imagePath = os.path.join(imageFolder, imageName)
  pilImg = loadPIL(imagePath)
  imageQt = ImageQt.ImageQt(pilImg)
  reqKwarg = searchKeys('requestType', 'request') @ type >> kwargs
  reqArg = maybeType(type, *args)
  reqDefault = QPixmap
  req = maybe(reqKwarg, reqArg, reqDefault)
  if req == Image.Image:
    return pilImg
  if req in [QImage, ImageQt.ImageQt]:
    return imageQt
  if req == QPixmap:
    return QPixmap(imageQt)
