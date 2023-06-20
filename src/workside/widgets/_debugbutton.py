"""DebugButton is a subclass of AbstractButton allowing implementation of
various functionality for use in more specific subclasses"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from random import randint
from typing import NoReturn, Never

from PySide6.QtCore import Qt
from PySide6.QtGui import QPaintEvent, QPainter
from icecream import ic
from worktoy.waitaminute import ReadOnlyError

from workside.styles import baseButtonStyle, textButtonStyle, \
  hoverButtonStyle
from workside.widgets import CoreWidget, AbstractButton

ic.configureOutput(includeContext=True)


class DebugButton(AbstractButton):
  """DebugButton is a subclass of AbstractButton allowing implementation of
  various functionality for use in more specific subclasses
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __new__(cls, *args, **kwargs) -> DebugButton:
    """LOL"""
    out = super().__new__(cls)
    setattr(out, '__name__', 'LOL%d' % (randint(0, 255)))
    return out

  def __init__(self, *args, **kwargs) -> None:
    self._text = None
    AbstractButton.__init__(self, *args, **kwargs)
    _policy = self.contract()
    self.setSizePolicy(_policy)
    self.leftPressHold.connect(lambda: print(
      'AbstractButton: Left PressHold!'))
    self.leftClick.connect(lambda: print(
      'AbstractButton: Left SingleClick!'))
    self.leftDoubleClick.connect(lambda: print(
      'AbstractButton: Left DoubleClick!'))

    self.rightPressHold.connect(lambda: print(
      'AbstractButton: Right PressHold!'))
    self.rightClick.connect(lambda: print(
      'AbstractButton: Right SingleClick!'))
    self.rightDoubleClick.connect(lambda: print(
      'AbstractButton: Right DoubleClick!'))

    self.middlePressHold.connect(lambda: print(
      'AbstractButton: Middle PressHold!'))
    self.middleClick.connect(lambda: print(
      'AbstractButton: Middle SingleClick!'))
    self.middleDoubleClick.connect(lambda: print(
      'AbstractButton: Middle DoubleClick!'))

    self.backPressHold.connect(lambda: print(
      'AbstractButton: Back PressHold!'))
    self.backClick.connect(lambda: print(
      'AbstractButton: Back SingleClick!'))
    self.backDoubleClick.connect(lambda: print(
      'AbstractButton: Back DoubleClick!'))

    self.forwardPressHold.connect(lambda: print(
      'AbstractButton: Forward PressHold!'))
    self.forwardClick.connect(lambda: print(
      'AbstractButton: Forward SingleClick!'))
    self.forwardDoubleClick.connect(lambda: print(
      'AbstractButton: Forward DoubleClick!'))

  def _createText(self, ) -> NoReturn:
    """Creator-function for the text"""
    self._text = 'Hello there, I\'m the debug button!'

  def _getText(self, ) -> str:
    """Getter-function for the text"""
    if self._text is None:
      self._createText()
      return self._getText()
    if isinstance(self._text, str):
      return self._text
    msg = """Expected text to be of type %s, but received: %s!"""
    raise TypeError(msg % (str, type(self._text)))

  def _setText(self, text: str) -> NoReturn:
    """Setter-function for the text"""
    if isinstance(text, str):
      self._text = text
    else:
      msg = """Expected text to be of type %s, but received: %s!"""
      raise TypeError(msg % (str, type(text)))

  def update(self, ) -> NoReturn:
    """Brings a resize before the parent update"""
    boundingRect = self.getStyle().getBoundingRect(self._getText())
    self.setMinimumSize(boundingRect.size().toSize())
    return CoreWidget.update(self)

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementation of paint event"""
    painter = QPainter()
    painter.begin(self)
    style = baseButtonStyle if self.hover else hoverButtonStyle
    style @ painter
    viewRect = painter.viewport()
    painter.drawRect(viewRect)
    textButtonStyle @ painter
    painter.drawText(viewRect, Qt.AlignmentFlag.AlignCenter, self._getText())
    painter.end()

  def _noDel(self) -> Never:
    """Illegal deleter"""
    raise ReadOnlyError('text')

  text = property(_getText, _setText, _noDel)
