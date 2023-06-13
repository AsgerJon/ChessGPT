"""CoreWidget subclasses QWidget providing common and general
functionality."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QRectF, QRect, QPointF, QSizeF, QSize
from PySide6.QtWidgets import QWidget, QSizePolicy
from icecream import ic
from worktoy.core import maybe
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList

from workside.settings import Settings
from workside.styles import BaseStyle

ic.configureOutput(includeContext=True)


class CoreWidget(QWidget):
  """CoreWidget subclasses QWidget providing common and general
  functionality.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @staticmethod
  def createSizePolicy(*args, **kwargs) -> QSizePolicy:
    """Creator function for a size policy according to specification given
    in arguments"""
    verticalKeys = stringList('vertical, v, verticalPolicy')
    verticalSizePolicy, args, kwargs = extractArg(
      QSizePolicy.Policy, verticalKeys, *args, **kwargs)
    horizontalKeys = stringList('horizontal, h, horizontalPolicy')
    horizontalSizePolicy, args, kwargs = extractArg(
      QSizePolicy.Policy, horizontalKeys, *args, **kwargs)
    policy = QSizePolicy()
    verticalDefault = QSizePolicy.Policy.Preferred
    horizontalDefault = QSizePolicy.Policy.Preferred
    verticalSizePolicy = maybe(verticalSizePolicy, verticalDefault)
    horizontalSizePolicy = maybe(horizontalSizePolicy, horizontalDefault)
    policy.setVerticalPolicy(verticalSizePolicy)
    policy.setHorizontalPolicy(horizontalSizePolicy)
    return policy

  @classmethod
  def contract(cls) -> QSizePolicy:
    """Creator function for a size policy contracting vertically,
    and expanding horizontally"""
    return cls.createSizePolicy(
      vertical=QSizePolicy.Policy.Maximum,
      horizontal=QSizePolicy.Policy.Maximum)

  @classmethod
  def expandHorizontalPolicy(cls) -> QSizePolicy:
    """Creator function for a size policy expanding vertically,
    and contracting horizontally"""
    return cls.createSizePolicy(
      vertical=QSizePolicy.Policy.MinimumExpanding,
      horizontal=QSizePolicy.Policy.Maximum)

  @classmethod
  def expandVerticalPolicy(cls) -> QSizePolicy:
    """Creator function for a size policy expanding vertically,
    and contracting horizontally"""
    return cls.createSizePolicy(
      horizontal=QSizePolicy.Policy.Maximum,
      vertical=QSizePolicy.Policy.MinimumExpanding, )

  @classmethod
  def doubleExpand(cls) -> QSizePolicy:
    """Creator function for a size policy contracting vertically,
    and expanding horizontally"""
    return cls.createSizePolicy(
      vertical=QSizePolicy.Policy.MinimumExpanding,
      horizontal=QSizePolicy.Policy.MinimumExpanding)

  @staticmethod
  def parseParent(*args, **kwargs) -> QWidget:
    """Parses arguments to parent"""
    parentKeys = stringList('parent, main, mainWindow, window')
    parent, args, kwargs = extractArg(QWidget, parentKeys, *args, **kwargs)
    if isinstance(parent, QWidget):
      return parent

  def __init__(self, *args, **kwargs) -> None:
    parent = self.parseParent(*args, **kwargs)
    QWidget.__init__(self, parent)
    self._parent = parent
    self._style = None
    self.setupWidgets()
    self.setupActions()

  def _setParent(self, parent: CoreWidget) -> NoReturn:
    """Setter-function for the parent widget. When using this method the
    parent argument is expected to be of type CoreWidget"""
    if isinstance(parent, CoreWidget):
      self._parent = parent
    else:
      raise TypeError

  def getParent(self) -> CoreWidget:
    """Getter-function for the parent. Using the explicit getter and
    setter for the parent widget requires them to be of type CoreWidget"""
    return self._parent

  def _createStyle(self) -> NoReturn:
    """Creator function for the default style"""
    self._style = BaseStyle('default', )
    self._style.setViewPort(self.getViewPortF())

  def getStyle(self) -> BaseStyle:
    """Getter-function for the style"""
    if self._style is None:
      self._createStyle()
      return self.getStyle()
    if isinstance(self._style, BaseStyle):
      self._style.setViewPort(self.getViewPort())
      return self._style
    raise TypeError

  def setStyle(self, style: BaseStyle) -> NoReturn:
    """Setter-function for the style"""
    self._style = style

  def setupWidgets(self) -> NoReturn:
    """Sets up the widgets"""

  def setupActions(self) -> NoReturn:
    """Sets up the actions"""

  def show(self) -> NoReturn:
    """Reimplementation"""
    self.setupWidgets()
    self.setupActions()
    return QWidget.show(self)

  def __rmatmul__(self, other: BaseStyle) -> CoreWidget:
    """Applies given base style to self"""
    return self.setStyle(other)

  def getViewPortF(self) -> QRectF:
    """Getter-function for viewport as floating points"""
    r = self.visibleRegion().boundingRect().toRectF()
    left, top, width, height = r.left(), r.top(), r.right(), r.bottom()
    width = max(width, Settings.minimumWidgetSize.width())
    height = max(height, Settings.minimumWidgetSize.height())
    leftTop, size = QPointF(left, top), QSizeF(width, height)
    return QRectF(leftTop, size)

  def getViewPort(self) -> QRect:
    """Getter-function for viewport as integers"""
    return self.getViewPortF().toRect()

  def minimumSizeHint(self) -> QSize:
    """Implementation of minimum size hint"""
    return Settings.minimumWidgetSize
