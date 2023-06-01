"""MouseButton handles mouse click events on a button by button basis"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QObject, Qt, QTimer, Signal
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QWidget
from worktoy.core import maybe
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList
from worktoy.waitaminute import ProceduralError


class MouseButton(QObject):
  """MouseButton handles mouse click events on a button by button basis
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  click = Signal()
  doubleClick = Signal()
  pressHold = Signal()

  def __init__(self, *args, **kwargs) -> None:
    parent: QWidget
    _btn: Qt.MouseButton
    buttonKeys = stringList('button, buttonEnum, mouseButton')
    _btn, a, k = extractArg(Qt.MouseButton, buttonKeys, *args, **kwargs)
    if _btn is None:
      raise ProceduralError('_btn')
    self._button = _btn
    parentKeys = stringList('main, parent')
    parent, args, kwargs = extractArg(QWidget, parentKeys, *a, **k)
    self._parent = parent
    QObject.__init__(self, self._parent)
    pressTime: int
    dblTime: int
    releaseTime: int
    pressKeys = stringList('press, pressTime, pressTimeLimit')
    pressTime, args, kwargs = extractArg(int, pressKeys, *args, **kwargs)
    releaseKeys = stringList('release, releaseTime, releaseTimeLimit')
    releaseTime, args, kwargs = extractArg(int, releaseKeys, *args, **kwargs)
    dblKeys = stringList('dblClick, dblClickTime, dblClickTimeLimit')
    dblTime, args, kwargs = extractArg(int, dblKeys, *args, **kwargs)
    pressTimeDefault: int = 500
    releaseTimeDefault: int = 100
    dblTimeDefault: int = 200
    self._pressTime: int
    self._releaseTime: int
    self._dblTime: int
    if pressTime is None:
      self._pressLimit = pressTimeDefault
    else:
      self._pressLimit = pressTime
    if releaseTime is None:
      self._releaseLimit = releaseTimeDefault
    else:
      self._releaseLimit = releaseTime
    if dblTime is None:
      self._dblLimit = dblTimeDefault
    else:
      self._dblLimit = dblTime

    self._pressTimer = QTimer(self)
    self._pressTimer.setSingleShot(True)
    self._pressTimer.setInterval(self._pressLimit)
    self._pressTimer.timeout.connect(self._handlePressTimeout)

    self._pressHoldTimer = QTimer(self)
    self._pressHoldTimer.setSingleShot(True)
    self._pressHoldTimer.setInterval(self._pressLimit * 2)
    self._pressHoldTimer.timeout.connect(self._handlePressHoldTimeout)

    self._doubleClickBanTimer = QTimer(self)
    self._doubleClickBanTimer.setSingleShot(True)
    self._doubleClickBanTimer.setInterval(self._dblLimit)
    self._doubleClickBanTimer.timeout.connect(self.click.emit)

    self._releaseTimer = QTimer(self)
    self._releaseTimer.setSingleShot(True)
    self._releaseTimer.setInterval(self._releaseLimit)
    self._releaseTimer.timeout.connect(self.click.emit)
    self._releaseTimer.timeout.connect(self._doubleClickBanTimer.start)

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

  def _handlePressHoldTimeout(self) -> NoReturn:
    """Press hold time out handling"""
    self.pressHold.emit()

  def __eq__(self, event: QMouseEvent) -> bool:
    """Checks if button in matches this button"""
    return True if event.button() == self._button else False

  def mousePressEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation"""
    if self == event:
      self._pressTimer.start(self._pressLimit)

  def mouseReleaseEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation"""
    if self == event:
      if self._pressTimer.isActive():
        self._pressTimer.stop()
        self._releaseTimer.start(self._releaseLimit)
      self._pressHoldTimer.stop()

  def mouseDoubleClickEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation"""
    if self == event:
      if self._doubleClickBanTimer.isActive():
        return
      self._pressTimer.stop()
      self._pressHoldTimer.stop()
      self._releaseTimer.stop()
      self.doubleClick.emit()
