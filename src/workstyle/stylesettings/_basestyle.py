"""BaseStyle"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QBrush, QFont, QPen, QColor, QPainter
from icecream import ic
from worktoy.waitaminute import ProceduralError

from workstyle.styles import Family

ic.configureOutput(includeContext=True)


class BaseStyle:
  """Instances must contain settings applied to QPainters"""

  _baseValues = dict(
    fillColor=QColor(0, 0, 0, 0),
    fillStyle=Qt.BrushStyle.SolidPattern,
    lineColor=QColor(0, 0, 0, 0),
    lineStyle=Qt.PenStyle.SolidLine,
    lineWidth=1,
    fontFamily=Family.courierNew,
    fontWeight=QFont.Weight.Normal,
    fontSize=12,
  )

  def __init__(self, name: str, data: dict) -> None:
    self._viewPort = None
    self._name = name
    self._data = data | BaseStyle._baseValues
    self._data = {}
    for (key, val) in BaseStyle._baseValues.items():
      self._data |= {key: data.get(key, val)}

  def getViewPort(self) -> QRect:
    """Getter-function for viewport"""
    if self._viewPort is None:
      raise ProceduralError('viewPort')
    return self._viewPort

  def setViewPort(self, viewPort: QRect) -> NoReturn:
    """Setter-function for viewport"""
    self._viewPort = viewPort

  def getFont(self, ) -> QFont:
    """Getter-function for QFont"""
    font = self._data.get('fontFamily').asQFont()
    weight = self._data.get('fontWeight')
    font.setWeight(weight)
    viewSize = min(self.getViewPort().width(), self.getViewPort().height())
    fontSize = int(self._data.get('fontSize') * viewSize / 400)
    font.setPointSize(fontSize)
    return font

  def getBrush(self) -> QBrush:
    """Getter-function for QBrush"""
    brush = QBrush()
    brush.setStyle(self._data.get('fillStyle'))
    brush.setColor(self._data.get('fillColor'))
    return brush

  def getPen(self) -> QPen:
    """Getter-function for QPen"""
    pen = QPen()
    pen.setStyle(self._data.get('lineStyle'))
    pen.setColor(self._data.get('lineColor'))
    pen.setWidth(self._data.get('lineWidth'))
    return pen

  def __matmul__(self, other: QPainter) -> QPainter:
    """Applies these settings to the given painter"""
    self.setViewPort(other.viewport())
    other.setPen(self.getPen())
    other.setFont(self.getFont())
    other.setBrush(self.getBrush())
    return other

  def __str__(self) -> str:
    """String representation"""
    out = 'BaseStyle instance: %s' % (self._name)
    return out

  def __repr__(self, ) -> str:
    """Code Representation"""
    out = 'BaseStyle: %s\n' % self._name
    for (key, val) in self._data.items():
      entry = '  %s: %s\n' % (key, val)
      out += entry
    return out
