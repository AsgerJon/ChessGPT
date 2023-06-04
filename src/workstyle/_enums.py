"""Enums relating to PySide6"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import IntEnum

from PySide6.QtCore import Qt

from typing import TYPE_CHECKING

from worktoy.core import maybe
from worktoy.stringtools import stringList

if TYPE_CHECKING:
  from typing import Any
else:
  from worktoy.typetools import Any


class Click(IntEnum):
  """Click Type"""

  NULL = 0
  SINGLE = 1
  DOUBLE = 2


class Button(IntEnum):
  """Mouse buttons"""

  @classmethod
  def buttonNames(cls, ) -> dict[str, int]:
    """Named button"""
    names = stringList('left, right, middle, forward, back, NULL')
    return {k: v for (v, k) in enumerate(names)}

  @classmethod
  def fromName(cls, name: str) -> Button:
    """Returns the instance matching name"""
    num = cls.buttonNames().get(name, 5)
    return cls.fromValue(num)

  @classmethod
  def fromFlag(cls, qt: Qt.MouseButton) -> Any:
    """Returns the instance matching given Qt Enum"""
    for btn in cls:
      if btn.flag() == qt:
        return btn
    return cls.NULL

  @classmethod
  def fromValue(cls, num: int) -> Button:
    """Returns the instance matching given value"""
    for btn in cls:
      if btn.value == num:
        return btn
    return cls.NULL

  LEFT = 0
  RIGHT = 1
  MIDDLE = 2
  FORWARD = 3
  BACK = 4
  NULL = 5

  def flag(self, num: int = None) -> Qt.MouseButton:
    """As Qt Enum"""
    num = maybe(num, self)
    if isinstance(num, int):
      return [
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.RightButton,
        Qt.MouseButton.MiddleButton,
        Qt.MouseButton.ForwardButton,
        Qt.MouseButton.BackButton,
        Qt.MouseButton.NoButton,
      ][num]
    return Qt.MouseButton.NoButton

  def __eq__(self, other: Any) -> bool:
    """Matching"""
    if isinstance(other, Qt.MouseButton):
      return True if self.flag() == other else False
    if isinstance(other, int):
      return False if self - other else True
    if isinstance(other, str):
      return False if self - Button.fromName(other) else True
