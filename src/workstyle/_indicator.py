"""Indicator"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Slot, Qt, QRect, QEvent
from PySide6.QtGui import QPainter, QColor
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList

from workstyle import CoreWidget


class MyLabel(CoreWidget):
  """Custom QLabel with overridden paintEvent for background coloring."""

  def __init__(self, *args, **kwargs) -> None:
    """Initialize MyLabel with parent widget and default state."""
    CoreWidget.__init__(self, *args, **kwargs)
    textKeys = stringList('label, text, labelText, note, msg')
    self._text, a, k = extractArg(str, textKeys, *args, **kwargs)
    self.isOn = False
    self.setMinimumSize(32, 32)
    self.setSizePolicy(QSizePolicy.Policy.Preferred,
                       QSizePolicy.Policy.Maximum)

  def getText(self) -> str:
    """Getter-function for the text"""
    if self._text is None:
      self._text = 'NoText'
      return self.getText()
    if isinstance(self._text, str):
      return self._text
    raise TypeError

  def setText(self, text: str) -> NoReturn:
    """Setter-function for the text"""
    if isinstance(text, str):
      self._text = text
    else:
      raise TypeError

  def paintEvent(self, event: QEvent) -> NoReturn:
    """Handle paint events with custom backgrounds and text."""
    painter = QPainter(self)
    color = QColor('limegreen') if self.isOn else QColor('lightcoral')
    painter.fillRect(QRect(0, 0, self.width(), self.height()), color)
    painter.setPen(QColor('black'))
    painter.drawText(event.rect(), Qt.AlignCenter, self.getText())


class Indicator(CoreWidget):
  """Custom QWidget containing three state indicators."""

  def __init__(self, *args, **kwargs) -> None:
    """Initialize Indicator with three state indicators."""
    CoreWidget.__init__(self, *args, **kwargs)
    self.setSizePolicy(QSizePolicy.Policy.Preferred,
                       QSizePolicy.Policy.Maximum)
    self.label1 = MyLabel("State 1: OFF", self)
    self.label2 = MyLabel("State 2: OFF", self)
    self.label3 = MyLabel("State 3: OFF", self)
    layout = QHBoxLayout()
    layout.addWidget(self.label1)
    layout.addWidget(self.label2)
    layout.addWidget(self.label3)
    self.setLayout(layout)

  @Slot(bool)
  def setState1(self, isOn: bool) -> NoReturn:
    """Set state of first indicator and trigger repaint."""
    self.label1.isOn = isOn
    self.label1.setText("State 1: ON" if isOn else "State 1: OFF")
    self.label1.update()

  @Slot(bool)
  def setState2(self, isOn: bool) -> NoReturn:
    """Set state of second indicator and trigger repaint."""
    self.label2.isOn = isOn
    self.label2.setText("State 2: ON" if isOn else "State 2: OFF")
    self.label2.update()

  @Slot(bool)
  def setState3(self, isOn: bool) -> NoReturn:
    """Set state of third indicator and trigger repaint."""
    self.label3.isOn = isOn
    self.label3.setText("State 3: ON" if isOn else "State 3: OFF")
    self.label3.update()
