"""Settings"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from os import abort

from PySide6.QtCore import QPointF, Qt, QEvent
from PySide6.QtGui import QEnterEvent, QSinglePointEvent, QMouseEvent
from PySide6.QtWidgets import QWidget
from icecream import ic
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList

from workside.widgets import CoreWidget

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
  forbiddenCursor = Qt.CursorShape.ForbiddenCursor
  deviceName = 'Razer'
  movingTimeLimit = 200

  @staticmethod
  def convertToEnterEvent(*args, **kwargs) -> QEnterEvent:
    """Converts a QSinglePointEvent to a QEnterEvent for the same widget."""
    eventKey = stringList('event, mouseEvent, QMouseEvent, e')
    widgetKey = stringList('widget, parent, owner, device')
    event, a, k = extractArg(QMouseEvent, eventKey, *args, **kwargs)
    widget, a, k = extractArg(CoreWidget, widgetKey, *args, **kwargs)
    if not isinstance(widget, CoreWidget):
      ic(widget, type(widget))
      abort()
      raise TypeError
    if not isinstance(event, QEvent):
      raise TypeError
    if isinstance(event, QSinglePointEvent):
      localPosition = event.position()
      scenePosition = event.scenePosition()
      globalPosition = event.globalPosition()
      pointingDevice = event.pointingDevice()
    else:
      raise TypeError
    enterEvent = QEnterEvent(
      localPosition, scenePosition, globalPosition, device=pointingDevice)
    return enterEvent

  @staticmethod
  def mouseMoveEventFactory(*args, **kwargs) -> QMouseEvent:
    """Factory function for instances of QMouseEvent"""
    eventType = QEvent.Type.MouseMove
    widgetKeys = stringList('parent, widget, main, window, scope')
    widget, a, k = extractArg(CoreWidget, widgetKeys, *args, **kwargs)
    localPos = getattr(widget, '_position', None)
    if localPos is None:
      raise TypeError
    boardRect = getattr(widget, 'boardRect', None)
    if isinstance(widget, QWidget):
      viewPort = QWidget.visibleRegion(widget, ).boundingRect().toRectF()
    else:
      raise TypeError
    globalPos = QWidget.mapToGlobal(widget, localPos)
    button = Qt.MouseButton.NoButton
    buttons = Qt.MouseButton.NoButton | Qt.MouseButton.NoButton
    return QMouseEvent(eventType, localPos, globalPos, button, )
