"""Shade is an Enum for dark and light squares"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum

from icecream import ic
from worktoy.typetools import TypeBag

from workstyle.styles import DarkSquareStyle, LightSquareStyle

ic.configureOutput(includeContext=True)


class Shade(Enum):
  """Enum for light and dark squares"""
  DARK = 0
  LIGHT = 1

  def __bool__(self) -> bool:
    """Light is True, and Dark is False"""
    return True if '%s' % self.name.lower() == 'light' else False

  def __eq__(self, other: Shade) -> bool:
    """Equality operator implementation"""
    return True if self is other else False

  def __str__(self) -> str:
    """String Representation"""
    return 'Light' if self else 'Dark'

  def __repr__(self) -> str:
    """Code Representation"""
    return 'Shade.%s' % ('%s' % self).upper()

  def getStyle(self) -> TypeBag(LightSquareStyle, DarkSquareStyle):
    """Style getter function"""
    return LightSquareStyle if self else DarkSquareStyle
