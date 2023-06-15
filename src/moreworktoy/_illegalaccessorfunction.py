"""The illegalAccessorFunction creates an illegal accessor function"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Never

from icecream import ic
from worktoy.typetools import CallMeMaybe
from worktoy.waitaminute import ReadOnlyError

ic.configureOutput(includeContext=True)


def illegalAccessorFactory(name: str) -> CallMeMaybe:
  """Factory creating illegal accessor factory. This method is coming to
  WorkToy in the future!"""

  def func(__, *_) -> Never:
    """Illegal accessor function"""
    raise ReadOnlyError(name)

  return func


noAcc = illegalAccessorFactory
