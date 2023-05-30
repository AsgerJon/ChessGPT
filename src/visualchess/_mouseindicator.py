"""MouseIndicator"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QPoint, Slot
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList


class MouseIndicator(QWidget):
  """MouseIndicator
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, parent=None, *args, **kwargs) -> None:
    parentKeys = stringList('parent, main, mainWindow, window')
    parent: QWidget
    parent, args, kwargs = extractArg(QWidget, parentKeys, *args, **kwargs)
    QWidget.__init__(self, parent)
    self._baseWidget = None
    self._xLabel = None
    self._yLabel = None
    self._layout = None

  @Slot(QPoint)
  def indicate(self) -> NoReturn:
    """Indicator slot"""
    self._xLabel.setText

  def setupWidgets(self) -> NoReturn:
    """Sets up the widgets"""
    self._baseWidget = QWidget()
    self._xLabel = QWidget()
    self._yLabel = QWidget()
    self._layout = QHBoxLayout()
    self._layout.addWidget(self._xLabel)
    self._layout.addWidget(self._yLabel)
    self._baseWidget.setLayout(self._layout)

  def updateCoordinateLabel(self, mouse_pos):
    self.coordinate_label.setText(
      f"Mouse Coordinate: ({mouse_pos.x()}, {mouse_pos.y()})")
