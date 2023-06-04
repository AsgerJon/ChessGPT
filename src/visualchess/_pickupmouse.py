"""NEW SCRIPT"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtGui import QMouseEvent
from icecream import ic

from workstyle import CoreWidget

ic.configureOutput(includeContext=True)


class PickUpMouse(CoreWidget):
  """PickUpMouse is an alternative to WhereMouse which instead of focusing
  on doubleclick and single click and distinguishing between them,
  PickUpMouse allows picking up and putting down items found on the widget
  in a dynamic fashion."""

  def __init__(self, *args, **kwargs) -> None:
    CoreWidget.__init__(self, *args, **kwargs)

  def mousePressEvent(self, event: QMouseEvent) -> NoReturn:
    """Implementation"""
