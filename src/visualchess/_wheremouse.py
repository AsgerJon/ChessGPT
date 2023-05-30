"""WhereMouse is a widget displaying the location of the mouse.Mostly for
debugging purposes."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QLabel, QVBoxLayout, \
  QWidget


class WhereMouse(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Mouse Coordinate Widget")
    layout = QVBoxLayout(self)

    self.coordinate_label = QLabel()
    layout.addWidget(self.coordinate_label)

    self.setMouseTracking(True)

  def mouseMoveEvent(self, event):
    if event.buttons() == Qt.NoButton:
      mouse_pos = event.pos()
      self.coordinate_label.setText(
        f"Mouse coordinates: ({mouse_pos.x()}, {mouse_pos.y()})")

  def event(self, event):
    if event.type() == QEvent.ToolTip:
      # Update the tooltip to show the current mouse coordinates
      mouse_pos = event.pos()
      tooltip = f"Mouse coordinates: ({mouse_pos.x()}, {mouse_pos.y()})"
      QToolTip.showText(event.globalPos(), tooltip, self)
      return True

    return super().event(event)
