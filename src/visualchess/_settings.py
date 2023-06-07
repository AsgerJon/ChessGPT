"""Settings"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import QEnterEvent, QSinglePointEvent
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
  movingTimeLimit = 200


def convertToEnterEvent(event: QSinglePointEvent) -> QEnterEvent:
  """
  Converts a QSinglePointEvent to a QEnterEvent for the same widget.
  """
  # Retrieve the local and global positions from the QSinglePointEvent
  localPos = event.position().toPoint()
  widget = event.widget()

  if widget is None:
    raise AttributeError(
      "The QSinglePointEvent does not have an associated widget.")

  globalPos = widget.mapToGlobal(localPos)

  # Create a QEnterEvent with the same position as the QSinglePointEvent
  enterEvent = QEnterEvent(localPos, globalPos, localPos)

  return enterEvent
