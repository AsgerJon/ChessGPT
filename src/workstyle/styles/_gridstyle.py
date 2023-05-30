"""GridStyle defines the gridlines between the squares"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from workstyle.styles import BaseStyle


class GridStyle(BaseStyle):
  """GridStyle defines the gridlines between the squares
  #  MIT Licence #2F0703
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  context = 'gridStyle'

  lineStyle = Qt.PenStyle.NoPen
  fillStyle = Qt.BrushStyle.SolidPattern
  fillColor = QColor(32 + 15, 7, 3, 255)
