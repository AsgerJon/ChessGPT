"""Index is a subclass of field setting the index flag for use with
iteration"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from worktoy.field import BaseField
from worktoy.typetools import CallMeMaybe


class Index(BaseField):
  """Index is a subclass of field setting the index flag for use with
  iteration
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __init__(self, ) -> None:
    BaseField.__init__(self, '__index__', 0, type_=int, readOnly=False)

  def __call__(self, cls: type) -> type:
    """Implements iteration if class implements the 'iterable' method."""
    cls = BaseField.__call__(self, cls)
    iterable = getattr(cls, 'iterable', None)
    if iterable is None:
      return cls
    if not isinstance(iterable, CallMeMaybe):
      return cls

    def newIter(instance, ) -> Any:
      """Implementation of __iter__"""
      instance.__index__ = 0
      return instance

    def newNext(instance, ) -> Any:
      """Implementation of __next__"""
      instance.__index__ += 1
      if instance.__index__ > len(instance):
        raise StopIteration
      return instance.iterable()[instance.__index__ - 1]

    def newLen(instance, ) -> int:
      """Implementation of __len__"""
      return len(instance.iterable())

    setattr(cls, '__iter__', newIter)
    setattr(cls, '__next__', newNext)
    setattr(cls, '__len__', newLen)

    return cls
