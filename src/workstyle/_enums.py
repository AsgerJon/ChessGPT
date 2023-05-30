"""Enums relating to PySide6"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum

from PySide6.QtCore import Qt

from typing import TYPE_CHECKING

if TYPE_CHECKING:
  from typing import Any
else:
  from worktoy.typetools import Any


class Button(IntEnum):
  """Mouse buttons"""

  LEFT = 0
  RIGHT = 1
  MIDDLE = 2
  FORWARD = 3
  BACK = 4

  def flag(self) -> Any:
    """As Qt Enum"""
    return [
      Qt.MouseButton.LeftButton,
      Qt.MouseButton.RightButton,
      Qt.MouseButton.MiddleButton,
      Qt.MouseButton.ForwardButton,
      Qt.MouseButton.BackButton,
    ][self]

  def __eq__(self, other: Any) -> bool:
    """Matching"""
    if isinstance(other, Qt.MouseButton):
      return True if self.flag() == other else False
