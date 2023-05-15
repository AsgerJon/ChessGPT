"""The savePIL and loadPIL saves and loads PIL images"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PIL import Image
from PySide6.QtGui import QPixmap


def savePIL(image: Image.Image, file_path: str) -> NoReturn:
  """Saves pil image to filePath"""
  image.save(file_path, "PNG")


def loadPIL(file_path: str) -> Image.Image:
  """Loads png file to pil image"""
  return Image.open(file_path)


def pixmapToPilImage(pix: QPixmap) -> Image.Image:
  """QPixmap to pil image"""
  image = pix.toImage()
  image.save("temp.png", "PNG")
  pil_image = Image.open("temp.png")
  return pil_image
