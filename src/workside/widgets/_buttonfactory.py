"""The button decorates the CoreWidget with a mouse button"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QMouseEvent
from icecream import ic
from worktoy.typetools import CallMeMaybe

from workside.widgets import MouseButton

ic.configureOutput(includeContext=True)

buttonDict = dict(
  left=Qt.MouseButton.LeftButton,
  right=Qt.MouseButton.RightButton,
  middle=Qt.MouseButton.MiddleButton,
  back=Qt.MouseButton.BackButton,
  forward=Qt.MouseButton.ForwardButton,
)


def buttonFactory(button: Qt.MouseButton | str) -> CallMeMaybe:
  """The button decorates the CoreWidget with a mouse button
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  if isinstance(button, str):
    try:
      return buttonFactory(buttonDict.get(button))
    except KeyError as e:
      print('Could not recognize %s as name of mouse button!' % button)
      raise e

  if not isinstance(button, Qt.MouseButton):
    msg = """Expected button to be of type %s, but received %s!"""
    raise TypeError(msg % (Qt.MouseButton, type(button)))

  def decorator(cls: type) -> type:
    """The actual decorator returned by the factory"""
    ButtonName = ('%s' % button).split('.')[-1]
    buttonName = '%s%s' % (ButtonName[0].lower(), ButtonName[1:])
    _buttonName = '_%s' % buttonName
    getButtonName = '_get%s' % ButtonName
    shortName = buttonName.replace('Button', '')
    pressHoldName = '%sPressHold' % shortName
    singleClickName = '%sClick' % shortName
    doubleClickName = '%sDoubleClick' % shortName

    setattr(cls, pressHoldName, Signal())
    setattr(cls, singleClickName, Signal())
    setattr(cls, doubleClickName, Signal())

    oldInit = getattr(cls, '__init__', None)

    def postInit(self, *args, **kwargs) -> NoReturn:
      """Extra initialization"""
      oldInit(self, *args, **kwargs)
      # setattr(cls, _buttonName, MouseButton(cls, button))
      setattr(cls, _buttonName, MouseButton(button))
      getattr(getattr(cls, _buttonName, ), 'pressHold').connect(
        getattr(self, pressHoldName).emit)
      getattr(getattr(cls, _buttonName, ), 'singleClick').connect(
        getattr(self, singleClickName).emit)
      getattr(getattr(cls, _buttonName, ), 'doubleClick').connect(
        getattr(self, doubleClickName).emit)

    setattr(cls, '__init__', postInit)

    setattr(cls, getButtonName, lambda self: getattr(self, _buttonName))

    oldPress = getattr(cls, 'mousePressEvent')
    oldRelease = getattr(cls, 'mouseReleaseEvent')
    oldDoubleClick = getattr(cls, 'mouseDoubleClickEvent')

    def newPressEvent(self, event: QMouseEvent) -> NoReturn:
      """New mouse press event"""
      getattr(cls, getButtonName)(self).mousePressEvent(event)
      return oldPress(self, event)

    def newReleaseEvent(self, event: QMouseEvent) -> NoReturn:
      """New mouse press event"""
      getattr(cls, getButtonName)(self).mouseReleaseEvent(event)
      oldRelease(self, event)
      return

    def newDoubleClick(self, event: QMouseEvent) -> NoReturn:
      """New mouse press event"""
      getattr(self, getButtonName, )().mouseDoubleClickEvent(event)
      oldDoubleClick(self, event)
      return

    setattr(cls, 'mousePressEvent', newPressEvent)
    setattr(cls, 'mouseReleaseEvent', newReleaseEvent)
    setattr(cls, 'mouseDoubleClickEvent', newDoubleClick)

    return cls

  return decorator
