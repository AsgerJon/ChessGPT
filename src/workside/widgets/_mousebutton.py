"""MouseButton instances allow each button on a mouse to operate entirely
independently."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn, Any

from PySide6.QtCore import Signal, QTimer, Qt
from PySide6.QtGui import QMouseEvent
from icecream import ic
from worktoy.core import maybe
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList

from workside.settings import flag, Settings, timer
from workside.widgets import CoreWidget

ic.configureOutput(includeContext=True)


@timer('pressHold', Settings.pressHoldTime, 'pressHold')
@timer('releaseDeadLine', Settings.releaseDeadLineTime, 'clickCancel')
@timer('singleClickLockout',
       Settings.singleClickLockoutTime,
       'singleClickReady')
@timer('doubleClickLockout',
       Settings.doubleClickLockoutTime,
       'doubleClickReady')
@timer('releaseClickDelay', Settings.releaseClickDelayTime, 'singleClick')
class MouseButton(CoreWidget):
  """MouseButton instances allow each button on a mouse to operate entirely
  independently.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  clickCancel = Signal()
  singleClickReady = Signal()
  doubleClickReady = Signal()
  pressHold = Signal()
  singleClick = Signal()
  doubleClick = Signal()

  @staticmethod
  def parseArguments(*args, **kwargs) -> Any:
    """Parses arguments"""
    btnKeys = stringList('button, mouseButton, btn')
    mouseButton, a, k = extractArg(Qt.MouseButton, btnKeys, *args, **kwargs)
    mouseButton = maybe(mouseButton, None)
    if isinstance(mouseButton, Qt.MouseButton):
      return mouseButton
    raise TypeError

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)
    self._mouseButton = self.parseArguments(*args, **kwargs)
    # self._pressHoldTimer = None
    # self._releaseDeadLineTimer = None
    # self._releaseClickDelayTimer = None
    # self._singleClickLockoutTimer = None
    # self._doubleClickLockoutTimer = None
    # self.singleClick.connect(lambda: print('singleClick emitted'))
    self._first = True

  def mousePressEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation of mouse press event"""
    if self._first:
      self.singleClick.connect(self._getDoubleClickLockoutTimer().start)
      self._first = False
    if self._mouseButton == event.button():
      if self._getSingleClickLockoutTimer().isActive():
        return
      self._getReleaseClickDelayTimer().stop()
      self._getReleaseDeadLineTimer().stop()
      self._getPressHoldTimer().start()
      self._getReleaseDeadLineTimer().start()

  def mouseReleaseEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation of mouse release event"""
    if self._mouseButton == event.button():
      self._getPressHoldTimer().stop()
      if self._getSingleClickLockoutTimer().isActive():
        return
      if self._getReleaseDeadLineTimer().isActive():
        self._getReleaseDeadLineTimer().stop()
        self._getSingleClickLockoutTimer().start()
        return self._getReleaseClickDelayTimer().start()

  def mouseDoubleClickEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation of mouse doubleclick event"""
    if self._getDoubleClickLockoutTimer().isActive():
      return
    if self._mouseButton == event.button():
      self._getReleaseClickDelayTimer().stop()
      self._getReleaseDeadLineTimer().stop()
      self.doubleClick.emit()
      self._getSingleClickLockoutTimer().start()
