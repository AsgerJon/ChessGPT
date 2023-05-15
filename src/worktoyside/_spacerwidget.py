"""SpacerWidget provides filler around content widgets"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Qt
from PySide6.QtGui import QPaintEvent, QPainter, QBrush, QColor, QPen
from PySide6.QtWidgets import QWidget, QSizePolicy
from worktoy import searchKeys, maybe, maybeType


class SpacerWidget(QWidget):
  """SpacerWidget provides filler around content widgets
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @staticmethod
  def expandPolicy() -> QSizePolicy.Policy:
    """Getter-function for expander policy"""
    return QSizePolicy.Policy.MinimumExpanding

  @staticmethod
  def maximumPolicy() -> QSizePolicy.Policy:
    """Getter-function for expander policy"""
    return QSizePolicy.Policy.Maximum

  def __init__(self, *args, **kwargs) -> None:
    parentKwarg = searchKeys('parent', 'main') @ QWidget >> kwargs
    parentArg = maybeType(QWidget, *args)
    parentDefault = None
    parent = maybe(parentKwarg, parentArg, parentDefault)
    QWidget.__init__(self, parent)
    vPol = self.expandPolicy()
    hPol = self.expandPolicy()
    pol = QSizePolicy()
    pol.setHorizontalPolicy(hPol)
    pol.setVerticalPolicy(vPol)
    self.setSizePolicy(pol)

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """PaintEvent """
    p = QPainter()
    p.begin(self)
    viewRect = p.viewport()
    brush = QBrush()
    brush.setColor(QColor(223, 255, 223))
    brush.setStyle(Qt.BrushStyle.SolidPattern)
    pen = QPen()
    pen.setColor(QColor(0, 0, 0, ))
    pen.setStyle(Qt.PenStyle.SolidLine)
    pen.setWidget(1)
    p.setPen(pen)
    p.setBrush(brush)
    p.drawRect(viewRect, )
    p.end()


class HorizontalSpacer(SpacerWidget):
  """Horizontal spacer expands in horizontally"""

  def __init__(self, *args, **kwargs) -> None:
    SpacerWidget.__init__(self, *args, **kwargs)
    vPol = self.maximumPolicy()
    hPol = self.expandPolicy()
    pol = QSizePolicy()
    pol.setHorizontalPolicy(hPol)
    pol.setVerticalPolicy(vPol)
    self.setSizePolicy(pol)


class VerticalSpacer(SpacerWidget):
  """Horizontal spacer expands in horizontally"""

  def __init__(self, *args, **kwargs) -> None:
    SpacerWidget.__init__(self, *args, **kwargs)
    vPol = self.expandPolicy()
    hPol = self.maximumPolicy()
    pol = QSizePolicy()
    pol.setHorizontalPolicy(hPol)
    pol.setVerticalPolicy(vPol)
    self.setSizePolicy(pol)
