"""BackgroundStyle defines the background"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from workstyle.styles import BaseStyle


class BackgroundStyle(BaseStyle):
  """BackgroundStyle"""

  context = 'background'
  fillColor = QColor(247, 247, 255, 255)
  lineStyle = Qt.PenStyle.NoPen
