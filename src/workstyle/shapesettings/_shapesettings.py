"""ShapeSettings. This class provides the static shape settings."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QRectF, QSizeF, QPointF
from icecream import ic

ic.configureOutput(includeContext=True)


class ShapeSettings:
  """ShapeSettings. This class provides the static shape settings.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  _viewPort = QRectF(QPointF(0, 0), QSizeF(400, 400))
  _squareGap = 2
  _boardOutline = 2

  @classmethod
  def setViewPort(cls, viewPort: QRectF) -> NoReturn:
    """Setter function for the view port"""
    cls._viewPort = viewPort

  @classmethod
  def getViewPort(cls, ) -> QRectF:
    """Getter-function for the view port"""
    return cls._viewPort

  @classmethod
  def getSideLength(cls) -> int:
    """Getter-function for the shortest side length"""
    viewPort = cls.getViewPort()
    return int(min(viewPort.width(), viewPort.height()))

  @classmethod
  def squareGap(cls) -> int:
    """Getter-function for square gap. """
    return cls._squareGap

  @classmethod
  def borderOutline(cls) -> int:
    """Getter-function for the outline around the board."""
    return cls._boardOutline

  @classmethod
  def bezelWidth(cls) -> int:
    """Getter-function for the width of the bezels as proportion of the
    board dimensions. For example, 5 % means that a board of size 400 by
    400 pixels will have a bezel of 0.05 * 400 = 20.
    Please note, that it is 20 in the top, bottom and left, right. So with
    5%, 10% of the side-length will be used for bezels."""
    return int(cls.getSideLength() * 0.06)

  @classmethod
  def getCornerRadius(cls, ) -> tuple[int, int]:
    """This option specifies the degree to which the corners on the outer
    square outside the bezels, should be rounded."""
    viewPort = cls.getViewPort()
    return (0.02 * viewPort.width(), 0.02 * viewPort.height())

  @classmethod
  def adjustFontSize(cls, fontSize: float | int) -> int:
    """Adjusts the font size to current dimensions"""
    return int(cls.getSideLength() / 600 * fontSize)
