"""AbstractButton implements toggling between two states"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from abc import abstractmethod
from typing import NoReturn

from PySide6.QtCore import QEvent, Signal
from PySide6.QtGui import QPaintEvent, QEnterEvent, QMouseEvent
from icecream import ic

from workside.settings import flag, timer, Settings
from workside.widgets import CoreWidget, buttonFactory

ic.configureOutput(includeContext=True)


@buttonFactory('left')
@buttonFactory('right')
@buttonFactory('middle')
@buttonFactory('back')
@buttonFactory('forward')
@flag('moving')
@flag('hover', )
@flag('state', )
@timer('movingDelay', Settings.movingDelayTime, 'movingDeactivated')
class AbstractButton(CoreWidget):
  """AbstractButton implements toggling between two states
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  stateActivated = Signal()
  stateDeactivated = Signal()
  stateChanged = Signal(bool)
  hoverActivated = Signal()
  hoverDeactivated = Signal()
  hoverChanged = Signal(bool)
  movingActivated = Signal()
  movingDeactivated = Signal()
  movingChanged = Signal(bool)

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)
    self.movingActivated.connect(self.activateMoving)
    self.movingActivated.connect(lambda: self.handleMovingChanged(True))
    self.movingDeactivated.connect(self.deactivateMoving)
    self.movingDeactivated.connect(lambda: self.handleMovingChanged(False))
    self.hoverActivated.connect(self.activateHover)
    self.hoverActivated.connect(lambda: self.handleHoverChanged(True))
    self.hoverDeactivated.connect(self.deactivateHover)
    self.hoverDeactivated.connect(lambda: self.handleHoverChanged(False))
    self.stateActivated.connect(self.activateState)
    self.stateActivated.connect(lambda: self.handleHoverChanged(True))
    self.stateDeactivated.connect(self.deactivateState)
    self.stateDeactivated.connect(lambda: self.handleHoverChanged(False))

  def handleStateChanged(self, newState: bool) -> NoReturn:
    """Handles state changed signals"""
    self.stateChanged.emit(newState)
    self._activateState() if newState else self._deactivateState()

  def handleMovingChanged(self, newState: bool) -> NoReturn:
    """Handles moving changed signals"""
    self.movingChanged.emit(newState)

  def handleHoverChanged(self, newState: bool) -> NoReturn:
    """Handles hover changed signals"""
    self.hoverChanged.emit(newState)

  def enterEvent(self, event: QEnterEvent) -> NoReturn:
    """Implementation of enter event"""
    self.movingActivated.emit()
    self.hoverActivated.emit()
    self._getMovingDelayTimer().start()
    self.update()
    CoreWidget.enterEvent(self, event)

  def leaveEvent(self, event: QEvent) -> NoReturn:
    """Implementation of leave event"""
    self.movingDeactivated.emit()
    self.hoverDeactivated.emit()
    self.update()
    CoreWidget.leaveEvent(self, event)

  def mouseMoveEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation of mouse move event"""
    self._getMovingDelayTimer().stop()
    self.movingActivated.emit()
    self._getMovingDelayTimer().start()
    self.update()
    CoreWidget.mouseMoveEvent(self, event)

  @abstractmethod
  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Subclasses must implement paint event handling"""
