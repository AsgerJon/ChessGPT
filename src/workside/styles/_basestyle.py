"""BaseStyle"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import NoReturn, TYPE_CHECKING

from PySide6.QtCore import Qt, QRect, QRectF
from PySide6.QtGui import QBrush, QFont, QPen, QColor, QPainter, \
  QFontMetrics, QFontMetricsF
from icecream import ic
from worktoy.core import maybe
from worktoy.typetools import TypeBag
from worktoy.waitaminute import ProceduralError

from workside.settings import Settings
from workside.styles import Family

if TYPE_CHECKING:
  from workside.widgets import CoreWidget

  Graphic = TypeBag(QPainter, CoreWidget)

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

  def __init__(self, name: str, data: dict = None) -> None:
    data = maybe(data, {})
    if not isinstance(data, dict):
      raise TypeError
    self._viewPort = None
    self._name = name
    self._data = data | BaseStyle._baseValues
    self._data = {}
    for (key, val) in BaseStyle._baseValues.items():
      self._data |= {key: data.get(key, val)}
    self._fontMetrics = None

  def getData(self) -> dict:
    """Getter-function for data"""
    return self._data

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
    fontSize = self._data.get('fontSize')
    font.setPointSize(max(fontSize, Settings.minimumFontSize))
    return font

  def _createFontMetrics(self) -> NoReturn:
    """Creator-function for font metrics"""
    self._fontMetrics = QFontMetricsF(self.getFont())

  def getFontMetrics(self) -> QFontMetricsF:
    """Getter-function for font metrics"""
    if self._fontMetrics is None:
      self._createFontMetrics()
      return self._fontMetrics
    if isinstance(self._fontMetrics, QFontMetricsF):
      return self._fontMetrics
    msg = """Expected front metrics to be of type %s, but received: %s!"""
    raise TypeError(msg % (QFontMetricsF, type(self._fontMetrics)))

  def getBoundingRect(self, text: str) -> QRectF:
    """Getter-function for bounding rect"""
    return self.getFontMetrics().boundingRect(text)

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

  def __matmul__(self, other: Graphic) -> Graphic:
    """Applies these settings to the given painter"""
    if isinstance(other, QPainter):
      self.setViewPort(other.viewport())
      other.setPen(self.getPen())
      other.setFont(self.getFont())
      other.setBrush(self.getBrush())
      return other
    return NotImplemented

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
