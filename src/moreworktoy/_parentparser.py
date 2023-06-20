"""The parentParser function parses positional and keyword arguments to
find an instance of QWidget"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtWidgets import QWidget
from worktoy.parsing import extractArg
from worktoy.stringtools import stringList


def parentParser(*args, **kwargs) -> QWidget:
  """The parentParser function parses positional and keyword arguments to
  find an instance of QWidget
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  parentKeys = stringList('parent, main, mainWindow, window')
  parent, args, kwargs = extractArg(QWidget, parentKeys, *args, **kwargs)
  if isinstance(parent, QWidget):
    return parent
