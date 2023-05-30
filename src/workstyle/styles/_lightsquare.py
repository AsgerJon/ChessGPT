"""LightSquareStyle defines the look of the dark squares"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from workstyle.styles import BaseStyle


class LightSquareStyle(BaseStyle):
  """DarkSquareStyle defines the look of the dark squares
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  context = 'lightSquare'
  fillColor = QColor(15 * 16 + 1, 12 * 16 + 15, 10 * 16 + 7, 255)
  lineStyle = Qt.PenStyle.NoPen
