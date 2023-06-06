"""Settings"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QPointF, Qt
from icecream import ic

ic.configureOutput(includeContext=True)


class Settings:
  """Central Settings"""
  bezelRatio = 0.08
  squareGap = 2
  boardOutline = 2
  cornerRadius = 8
  adjustFontSize = 1 / 600
  origin = QPointF(0, 0)
  normalCursor = Qt.CursorShape.ArrowCursor
  hoverCursor = Qt.CursorShape.OpenHandCursor
  grabCursor = Qt.CursorShape.ClosedHandCursor
  deviceName = 'Razer'
