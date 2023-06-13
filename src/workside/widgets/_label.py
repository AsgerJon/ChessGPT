"""Label provides an alternative to QLabel"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

import string
from typing import NoReturn, Never

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPaintEvent, QPainter, QFontMetrics, QFont
from PySide6.QtWidgets import QSizePolicy
from icecream import ic
from worktoy.core import maybe
from worktoy.waitaminute import ReadOnlyError

from workside.styles import labelStyle, BaseStyle, Family, headerStyle
from workside.widgets import CoreWidget
from workside.settings import Settings
from random import choices

ic.configureOutput(includeContext=True)


class Label(CoreWidget):
  """Label provides an alternative to QLabel
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  _maxLength = None

  @classmethod
  def _getMaxLength(cls) -> int:
    """Getter-function for the width in number of characters."""
    out = maybe(cls._maxLength, Settings.headerLabelWidth)
    if isinstance(out, int):
      return out
    raise TypeError

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)
    self._words = None
    self._styleSettings = None
    self._fontMetrics = None
    self._font = None
    _policy = self.createSizePolicy(
      vertical=QSizePolicy.Policy.Maximum,
      horizontal=QSizePolicy.Policy.Maximum,
    )
    self.setSizePolicy(_policy)
    self.setStyle(headerStyle)

  def setFont(self, font: QFont) -> NoReturn:
    """Setter-function for the font"""
    self._createFont(font)
    self._createFontMetrics()

  def _createFont(self, font: QFont = None) -> NoReturn:
    """Creator-function for font"""
    if font is None:
      self._font = Family.modern.asQFont()
    elif isinstance(font, QFont):
      self._font = font
    else:
      raise TypeError

  def _getFont(self) -> QFont:
    """Getter-function for the font"""
    if self._style is None:
      self._createStyle()
      return self._getFont()
    font = self.getStyle().getFont()
    self._createFontMetrics(font)
    return font

  def _createFontMetrics(self, font: QFont = None) -> NoReturn:
    """Creator-function for the font metrics"""
    if font is None:
      font = self._getFont()
    if isinstance(font, QFont):
      self._fontMetrics = QFontMetrics(font)

  def _getFontMetrics(self, ) -> QFontMetrics:
    """Getter-function for the font metrics"""
    if self._fontMetrics is None:
      self._createFontMetrics()
      return self._getFontMetrics()
    if isinstance(self._fontMetrics, QFontMetrics):
      return self._fontMetrics
    raise TypeError

  def _getBoundingRect(self, text: str = None) -> QRectF:
    """Getter-function for the QRectF that would be required to bound the
    given text by the given font."""
    letters = [*string.ascii_lowercase, *string.ascii_uppercase]
    text = maybe(text, ''.join(choices(letters, k=self._getMaxLength())))
    if isinstance(text, str):
      return self._getFontMetrics().boundingRect(text).toRectF()
    raise TypeError

  def setStyle(self, style: BaseStyle) -> NoReturn:
    """Reimplementation of the style setter such as to create the font
    metrics immediately"""
    style.setViewPort(self.getViewPortF())
    font = style.getFont()
    self._createFontMetrics(font)
    CoreWidget.setStyle(self, style)

  def setText(self, text: str) -> NoReturn:
    """Setter-function for the text"""
    for word in text.split(' '):
      self._getWords().append(word)
    self.setMinimumSize(self._getBoundingRect(text).size().toSize())
    self.update()

  def getText(self, ) -> str:
    """Getter-function for the text"""
    words = []
    for word in reversed(self._getWords()):
      if len(words) + len(word) + 1 > self._getMaxLength():
        words.append('...')
        break
      else:
        words.append(word)
    return ' '.join(reversed(words))

  def _getWords(self, ) -> list[str]:
    """Getter-function for the list of strings to be used construct the
    text."""
    if self._words is None:
      self._words = []
      return self._getWords()
    if isinstance(self._words, list):
      return self._words
    raise TypeError

  def show(self) -> NoReturn:
    """Reimplementation inserting a measure of the bounding rectangle
    setting the size"""
    CoreWidget.show(self)
    self.setMinimumSize(self._getBoundingRect().size())

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementation of paint event"""
    painter = QPainter()
    painter.begin(self)
    self.getStyle() @ painter
    viewRect = painter.viewport()
    alignFlag = Qt.AlignmentFlag.AlignCenter
    painter.drawText(viewRect, alignFlag, self.getText())
    painter.end()
