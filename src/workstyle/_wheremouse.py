"""MouseWidget is a subclass of CoreWidget providing mouse related
signals. It does not implement the __init__."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Qt, Signal, QObject, QTimer
from PySide6.QtWidgets import QWidget
from icecream import ic
from worktoy.field import BaseField

from workstyle import CoreWidget

ic.configureOutput(includeContext=True)


@BaseField('activeButton', Qt.MouseButton.NoButton, type_=Qt.MouseButton)
class _WhereMouse(CoreWidget):
  """LOL"""

  click = Signal()
  doubleClick = Signal()

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)
    self._pressTimer = QTimer(self)
    self._pressTimer.setSingleShot(True)
    self._pressTimer.timeout.connect(self._handlePressTimeout)

    self._releaseTimer = QTimer(self)
    self._releaseTimer.setSingleShot(True)
    self._releaseTimer.timeout.connect(self.click.emit)

    self._activeButton = Qt.MouseButton.NoButton
    self._clickTimeLimit = 500
    self._releaseTimerDelay = 75

  def _handlePressTimeout(self) -> NoReturn:
    self._pressTimer.stop()

  def _handleReleaseTimeout(self) -> NoReturn:
    self.click.emit()

  def mousePressEvent(self, event) -> NoReturn:
    """Implementation"""
    self._activeButton = event.button()
    self._pressTimer.start(self._clickTimeLimit)

  def mouseReleaseEvent(self, event) -> NoReturn:
    """Implementation"""
    if self._pressTimer.isActive():
      self._pressTimer.stop()
      self._releaseTimer.start(self._releaseTimerDelay)

  def mouseDoubleClickEvent(self, event) -> NoReturn:
    """Implementation"""
    if event.button() == Qt.LeftButton:
      self._pressTimer.stop()
      self._releaseTimer.stop()
      self.doubleClick.emit()


class WhereMouse(_WhereMouse):
  """LOL"""
