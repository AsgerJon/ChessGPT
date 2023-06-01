"""MouseWidget is a subclass of CoreWidget providing mouse related
signals. It does not implement the __init__."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Qt, Signal, QObject, QTimer, QPointF, QEvent
from PySide6.QtGui import QMouseEvent, QEnterEvent
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
  move = Signal(QPointF)
  leave = Signal()
  enter = Signal(QPointF)

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)
    self._pressTimer = QTimer(self)
    self._pressTimer.setSingleShot(True)
    self._pressTimer.timeout.connect(self._handlePressTimeout)

    self._doubleClickBanTimer = QTimer(self)
    self._doubleClickBanTimer.setSingleShot(True)
    self._doubleClickBanTimer.timeout.connect(self.click.emit)

    self._releaseTimer = QTimer(self)
    self._releaseTimer.setSingleShot(True)
    self._releaseTimer.timeout.connect(self.click.emit)
    self._releaseTimer.timeout.connect(self._doubleClickBanTimer.start)

    self._activeButton = Qt.MouseButton.NoButton
    self._clickTimeLimit = 500
    self._releaseTimerDelay = 100
    self._doubleClickBanPeriod = 200

    self._point = None

  def _handlePressTimeout(self) -> NoReturn:
    """If a button is held in for two long the click signal is cancelled."""
    self._pressTimer.stop()

  def _handleReleaseTimeout(self) -> NoReturn:
    """After button release, a delay allows for a double click to occur,
    which prevents the single click emission. If the single click does
    happen, it places a ban on the double click for a time."""
    self.click.emit()

  def _handleDoubleClickBanTimeout(self) -> NoReturn:
    """Double clicks are banned for a period after a single click emits."""

  def mousePressEvent(self, event) -> NoReturn:
    """Implementation"""
    if self == event:
      self._pressTimer.start(self._clickTimeLimit)

  def mouseReleaseEvent(self, event) -> NoReturn:
    """Implementation"""
    if self._pressTimer.isActive():
      self._pressTimer.stop()
      self._releaseTimer.start(self._releaseTimerDelay)

  def mouseDoubleClickEvent(self, event) -> NoReturn:
    """Implementation"""
    if self._doubleClickBanTimer.isActive():
      return
    if event.button() == Qt.LeftButton:
      self._pressTimer.stop()
      self._releaseTimer.stop()
      self.doubleClick.emit()

  def mouseMoveEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation"""
    self._point = event.position()
    self.move.emit(self._point)

  def enterEvent(self, event: QEnterEvent) -> NoReturn:
    """Implementation"""
    self.enter.emit(event.position())

  def leaveEvent(self, event: QEvent) -> NoReturn:
    """Implementation"""
    self.leave.emit()


class WhereMouse(_WhereMouse):
  """LOL"""
