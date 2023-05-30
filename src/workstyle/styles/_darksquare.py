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

  fillColor = QColor(0, 0, 31, 255)
  lineStyle = Qt.PenStyle.NoPen
