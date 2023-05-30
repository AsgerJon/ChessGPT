"""MouseWidget is a subclass of CoreWidget providing mouse related
signals. It does not implement the __init__."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QPoint, Signal, QEvent
from PySide6.QtGui import QMouseEvent, QEnterEvent

from workstyle import CoreWidget


class MouseWidget(CoreWidget):
  """MouseWidget is a subclass of CoreWidget providing mouse related
  signals. It does not implement the __init__.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  mouseMove = Signal(QPoint)
  mouseLeftSingle = Signal(QPoint)
  mouseRightSingle = Signal(QPoint)
  mouseLeftDouble = Signal(QPoint)
  mouseRightDouble = Signal(QPoint)
  hoverEnter = Signal()
  hoverLeave = Signal()
  hover = Signal(bool)

  def mouseMoveEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation of signals"""
    self.mouseMove.emit(event.position().toPoint())

  def enterEvent(self, event: QEnterEvent) -> NoReturn:
    """Implementation of signals"""
    self.hoverEnter.emit()
    self.hover.emit(True)

  def leaveEvent(self, event: QEvent) -> NoReturn:
    """Implementation of signals"""
    self.hoverLeave.emit()
    self.hover.emit(False)

  def mousePressEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation of signals"""

  def mouseReleaseEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation of signals"""
    event.buttons()
