"""LayoutWidget wraps the 3 by 3 widget around the content widget"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QWidget
from worktoy import searchKeys, maybe, maybeType


class LayoutWidget(QWidget):
  """LayoutWidget wraps the 3 by 3 widget around the content widget.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, *args, **kwargs) -> None:
    parentKwarg = searchKeys('parent', 'main') @ QWidget >> kwargs
    parentArg = maybeType(QWidget, *args)
    parentDefault = None
    parent = maybe(parentKwarg, parentArg, parentDefault)
    QWidget.__init__(self, parent)
