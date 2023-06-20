"""CheckButton is a custom checkbox like widget"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Qt, QRect, Signal
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtWidgets import QWidget


class CheckButton(QWidget):
  """CheckButton is a custom checkbox like widget
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  clicked = Signal()

  def __init__(self, parent=None):
    super().__init__(parent)
    self.setChecked(False)

  def isChecked(self):
    return self._checked

  def setChecked(self, checked):
    self._checked = checked
    self.update()

  def paintEvent(self, event):
    painter = QPainter(self)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setRenderHint(QPainter.TextAntialiasing)

    # Calculate the size of the checkbox
    checkbox_size = min(self.width(), self.height())
    checkbox_rect = QRect(0, 0, checkbox_size, checkbox_size)
    checkbox_rect.moveCenter(self.rect().center())

    # Draw the checkbox frame
    frame_color = QColor(127, 127, 127) if self.isEnabled() else QColor(200,
                                                                        200,
                                                                        200)
    frame_pen = QPen(frame_color)
    frame_pen.setWidth(2)
    painter.setPen(frame_pen)
    painter.drawRect(checkbox_rect)

    # Draw the checkmark if checked
    if self._checked:
      checkmark_color = QColor(0, 0, 0)
      checkmark_pen = QPen(checkmark_color)
      checkmark_pen.setWidth(2)
      painter.setPen(checkmark_pen)
      checkmark_rect = checkbox_rect.adjusted(4, 4, -4, -4)
      painter.drawLine(checkmark_rect.topLeft(),
                       checkmark_rect.bottomRight())
      painter.drawLine(checkmark_rect.topRight(),
                       checkmark_rect.bottomLeft())

  def mousePressEvent(self, event) -> NoReturn:
    """Implementation"""
    if event.button() == Qt.LeftButton:
      self.setChecked(not self._checked)
      event.accept()
      self.clicked.emit()
    else:
      super().mousePressEvent(event)
