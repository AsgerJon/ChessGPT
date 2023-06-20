"""Spacer is a subclass of CoreWidget which pushes other widgets around"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtGui import QPaintEvent, QPainter
from PySide6.QtWidgets import QSizePolicy
from icecream import ic
from worktoy.stringtools import stringList

from workside.settings import Settings
from workside.styles import debugStyle
from workside.widgets import CoreWidget

ic.configureOutput(includeContext=True)


class Spacer(CoreWidget):
  """Spacer is a subclass of CoreWidget which pushes other widgets around
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)
    self.setMouseTracking(True)
    _policy = self.createSizePolicy(*args, **kwargs)
    if isinstance(_policy, QSizePolicy):
      self.setSizePolicy(_policy)
    else:
      raise TypeError
    # debugStyle @ self

  def paintEvent(self, event: QPaintEvent) -> NoReturn:
    """Implementation of paint event"""
    if not Settings.DEBUGGING:
      return
    painter = QPainter()
    painter.begin(self)
    self.getStyle() @ painter
    viewRect = painter.viewport()
    painter.drawRoundedRect(viewRect, 8, 8)
    painter.end()

  def __str__(self) -> str:
    """String Representation"""
    r = self.getViewPortF()
    names = stringList('left, top, right, bottom')
    localDims = [r.left(), r.top(), r.right(), r.bottom()]
    corners = [r.topLeft(), r.bottomRight()]
    corners = [self.mapToGlobal(c) for c in corners]
    corners = [[c.x(), c.y()] for c in corners]
    globalDims = [*corners[0], *corners[1], ]
    msg = """Spacer item with rectangle:\n\n    Local Coordinates:"""
    for (i, (name, dim)) in enumerate(zip(names, localDims)):
      msg = '%s\n  %s: %s' % (msg, name.capitalize(), dim)
    msg = """%s\n\n    Global Coordinates:""" % (msg)
    for (i, (name, dim)) in enumerate(zip(names, globalDims)):
      msg = '%s\n  %s: %s' % (msg, name.capitalize(), dim)

    return msg


class VSpacer(Spacer):
  """Vertical spacer"""

  def __init__(self, *__, **_) -> None:
    Spacer.__init__(self, horizontal=False, vertical=True)


class HSpacer(Spacer):
  """Vertical spacer"""

  def __init__(self, *__, **_) -> None:
    Spacer.__init__(self, horizontal=True, vertical=False)


class DoubleSpacer(Spacer):
  """Double directed spacer"""

  def __init__(self, *__, **_) -> None:
    Spacer.__init__(self, horizontal=True, vertical=True)
