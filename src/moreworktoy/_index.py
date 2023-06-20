"""Index is a subclass of field setting the index flag for use with
iteration"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import typing
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

  def __call__(self, cls: type) -> typing.Any:
    """Implements iteration if class implements the 'iterable' method."""
    cls = BaseField.__call__(self, cls)
    iterable = getattr(cls, 'iterable', None)
    if iterable is None:
      return cls
    if not isinstance(iterable, CallMeMaybe):
      return cls

    def newInit(instance, *args, **kwargs) -> None:
      """New init function"""
      setattr(instance, '__index__', 0)
      cls.__init__(instance, *args, **kwargs)

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

    if isinstance(iterable, classmethod):
      setattr(cls, '__index__', 0)
      setattr(cls, '__iter__', classmethod(newIter))
      setattr(cls, '__next__', classmethod(newNext))
      setattr(cls, '__len__', classmethod(newLen))
    else:
      setattr(cls, '__init__', newInit)
      setattr(cls, '__iter__', newIter)
      setattr(cls, '__next__', newNext)
      setattr(cls, '__len__', newLen)
    return cls
