"""The backgroundStyle is an instance of BaseStyle"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QFont
from icecream import ic

from workside.styles import BaseStyle, Family

ic.configureOutput(includeContext=True)
_baseData = dict(
  fillColor=QColor(0, 0, 0, 0),
  fillStyle=Qt.BrushStyle.SolidPattern,
  lineColor=QColor(0, 0, 0, 0),
  lineStyle=Qt.PenStyle.SolidLine,
  lineWidth=1,
  fontFamily=Family.courierNew,
  fontWeight=QFont.Weight.Normal,
  fontSize=12,
)
_darkSquareData = dict(
  fillColor=QColor(181, 136, 99),  # Light gray background color
  fillStyle=Qt.BrushStyle.SolidPattern,
  lineColor=QColor(0, 0, 0, 0),
  lineStyle=Qt.PenStyle.SolidLine,
  lineWidth=1,
  fontFamily=Family.courierNew,
  fontWeight=QFont.Weight.Normal,
  fontSize=12,
)
_lightSquareData = dict(
  fillColor=QColor(240, 217, 181),  # Light gray background color
  fillStyle=Qt.BrushStyle.SolidPattern,
  lineColor=QColor(0, 0, 0, 0),
  lineStyle=Qt.PenStyle.SolidLine,
  lineWidth=1,
  fontFamily=Family.courierNew,
  fontWeight=QFont.Weight.Normal,
  fontSize=12,
)
_bezelData = dict(
  fillColor=QColor(120, 98, 77, 255),  # Transparent fill color
  fillStyle=Qt.BrushStyle.SolidPattern,
  lineColor=QColor(255, 255, 255, 255),  # Black line color
  lineStyle=Qt.PenStyle.SolidLine,
  lineWidth=1,  # Increased line width for borders
  fontFamily=Family.courierNew,  # Courier New font family
  fontWeight=QFont.Weight.Bold,  # Bold font weight for visibility
  fontSize=14,  # Increased font size for better readability
)
_backgroundData = dict(
  fillColor=QColor(240, 240, 240),  # Light gray background color
  fillStyle=Qt.BrushStyle.SolidPattern,
  lineColor=QColor(200, 200, 200),  # Light gray line color
  lineStyle=Qt.PenStyle.SolidLine,
  lineWidth=1,
  fontFamily=Family.courierNew,
  fontWeight=QFont.Weight.Normal,
  fontSize=12,
)
_hoveredSquareData = dict(
  fillColor=QColor(173, 216, 230, 100),
  # Light blue fill color with alpha value of 100
  fillStyle=Qt.BrushStyle.SolidPattern,
  lineColor=QColor(0, 0, 0, 100),
  # Black line color with alpha value of 100
  lineStyle=Qt.PenStyle.SolidLine,
  lineWidth=2,
  # Increased line width for borders of hovered squares
  fontFamily=Family.courierNew,
  fontWeight=QFont.Weight.Normal,
  fontSize=12,
)
_outlineData = dict(
  fillColor=QColor(0, 0, 0, 0),
  fillStyle=Qt.BrushStyle.SolidPattern,
  lineColor=QColor(0, 0, 31, 255),
  lineStyle=Qt.PenStyle.SolidLine,
  lineWidth=2,
  fontFamily=Family.courierNew,
  fontWeight=QFont.Weight.Normal,
  fontSize=12,
)
_gridStyleData = dict(
  fillColor=QColor(223, 223, 255, 255),
  fillStyle=Qt.BrushStyle.SolidPattern,
  lineColor=QColor(0, 0, 0, 0),
  lineStyle=Qt.PenStyle.SolidLine,
  lineWidth=1,
  fontFamily=Family.courierNew,
  fontWeight=QFont.Weight.Normal,
  fontSize=12,
)
_labelData = dict(
  fillColor=QColor(0, 0, 0, 0, ),
  fillStyle=Qt.BrushStyle.NoBrush,
  lineColor=QColor(223, 223, 255, 255),
  lineStyle=Qt.PenStyle.SolidLine,
  lineWidth=1,
  fontFamily=Family.cambria,
  fontWeight=QFont.Weight.Bold,
  fontSize=16,
)
_headerData = dict(
  fillColor=QColor(0, 0, 0, 0, ),
  fillStyle=Qt.BrushStyle.NoBrush,
  lineColor=QColor(0, 0, 91, 255),
  lineStyle=Qt.PenStyle.SolidLine,
  lineWidth=1,
  fontFamily=Family.modern,
  fontWeight=QFont.Weight.Bold,
  fontSize=32,
)
_debugData = dict(
  fillColor=QColor(223, 255, 223, 255, ),
  fillStyle=Qt.BrushStyle.SolidPattern,
  lineColor=QColor(255, 0, 0, 255),
  lineStyle=Qt.PenStyle.SolidLine,
  lineWidth=1,
  fontFamily=Family.courierNew,
  fontWeight=QFont.Weight.Normal,
  fontSize=12,
)
_baseButton = dict(
  fillColor=QColor(0, 0, 63, 255, ),
  fillStyle=Qt.BrushStyle.SolidPattern,
  lineColor=QColor(255, 255, 255, 255),
  lineStyle=Qt.PenStyle.NoPen,
  lineWidth=1,
  fontFamily=Family.courierNew,
  fontWeight=QFont.Weight.Normal,
  fontSize=12,
)
_hoverButton = dict(
  fillColor=QColor(0, 0, 127, 255, ),
  fillStyle=Qt.BrushStyle.SolidPattern,
  lineColor=QColor(255, 255, 255, 255),
  lineStyle=Qt.PenStyle.NoPen,
  lineWidth=2,
  fontFamily=Family.courierNew,
  fontWeight=QFont.Weight.Normal,
  fontSize=12,
)
_textButton = dict(
  fillColor=QColor(0, 0, 127, 255, ),
  fillStyle=Qt.BrushStyle.NoBrush,
  lineColor=QColor(255, 255, 0, 255),
  lineStyle=Qt.PenStyle.SolidLine,
  lineWidth=1,
  fontFamily=Family.modern,
  fontWeight=QFont.Weight.Normal,
  fontSize=14
  ,
)
backgroundStyle = BaseStyle('Background', _backgroundData)
bezelStyle = BaseStyle('Bezels', _bezelData)
darkSquareStyle = BaseStyle('Dark Square', _darkSquareData)
lightSquareStyle = BaseStyle('Light Square', _lightSquareData)
hoveredSquareStyle = BaseStyle('Hover', _hoveredSquareData)
outlineStyle = BaseStyle('Outline', _outlineData)
gridStyle = BaseStyle('Grid', _gridStyleData)
labelStyle = BaseStyle('Label', _labelData)
headerStyle = BaseStyle('Label', _headerData)
debugStyle = BaseStyle('debug', _debugData)
baseButtonStyle = BaseStyle('Base Button', _baseButton)
hoverButtonStyle = BaseStyle('Hover Button', _hoverButton)
textButtonStyle = BaseStyle('Text Button', _textButton)
