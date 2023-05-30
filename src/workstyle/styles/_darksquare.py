"""DarkSquareStyle defines the look of the dark squares"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from workstyle.styles import BaseStyle


class DarkSquareStyle(BaseStyle):
  """DarkSquareStyle defines the look of the dark squares
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  context = 'darkSquare'
  # #CD7741
  fillColor = QColor(12 * 16 + 13, 7 * 16 + 7, 4 * 16 + 1, 255)
  lineStyle = Qt.PenStyle.NoPen
