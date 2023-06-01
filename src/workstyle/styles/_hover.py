"""HoverStyle"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from workstyle.styles import BaseStyle


class HoverStyle(BaseStyle):
  """HoverStyle defines the indication that a square is under the mouse
  #  MIT Licence #2F0703
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  context = 'hoverStyle'

  lineStyle = Qt.PenStyle.SolidLine
  lineColor = QColor(0, 0, 0, 255)
  lineWidth = 3
  fillStyle = Qt.BrushStyle.SolidPattern
  fillColor = QColor(255, 255, 255, 127)
