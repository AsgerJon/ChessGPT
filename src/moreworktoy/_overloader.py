"""OverLoad is a metaclass enabling overloading"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

import typing
from typing import TYPE_CHECKING

from icecream import ic
from worktoy.stringtools import justify
from worktoy.typetools import CallMeMaybe
from worktoy.waitaminute import UnexpectedStateError, ProceduralError

from moreworktoy import TypeKey

if TYPE_CHECKING:
  pass
else:
  pass

ic.configureOutput(includeContext=True)


class OverloadMeta(type):
  """OverLoad is a metaclass enabling overloading
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @classmethod
  def _exemptTypes(mcls) -> list[type]:
    """Getter-function for list of types exempt from having set attribute."""
    return [bytes, str, int, float, complex, bool, tuple, list, dict, set, ]

  @classmethod
  def _checkType(mcls, obj: object) -> bool:
    """Checks if given object is of exempted type"""
    return True if isinstance(obj, (*mcls._exemptTypes(),)) else False

  @staticmethod
  def _isDunder(name: str) -> bool:
    """Checks if name is __dunder__"""
    return True if name.startswith('__') or name.endswith('__') else False

  def __new__(mcls, name: str, bases: tuple[type], nameSpace: dict) -> type:
    """OverLoad is a metaclass enabling overloading
    #  MIT Licence
    #  Copyright (c) 2023 Asger Jon Vistisen"""
    attrs = nameSpace
    overloads = {}
    for (key, val) in nameSpace.items():
      typeKey = getattr(val, '__overloaded__', None)
      if typeKey is not None:
        funcName = val.__name__
        if overloads.get(funcName, None) is None:
          overloads |= {funcName: {}}
        overloads[funcName] |= {typeKey: val}
    nameSpace['__overloads__'] = overloads
    nameSpace['__meta__'] = mcls
    return super().__new__(mcls, name, bases, attrs)

  def __init__(cls, name: str, bases: tuple[type], nameSpace: dict) -> None:
    super().__init__(name, bases, nameSpace)
    __meta__ = getattr(nameSpace, '__meta__', None)
    if __meta__ is None:
      msg = """Expected name space to define __meta__!"""
      raise ProceduralError(msg)
    setattr(cls, '__meta__', __meta__)
    for (key, val) in nameSpace.items():
      if OverloadMeta._isDunder(key) or OverloadMeta._checkType(val):
        pass
      else:
        setattr(val, '__class__', cls)
        setattr(val, '__class_name__', cls.__name__)
        setattr(val, '__class_qualname__', cls.__qualname__)
    overLoadedFunctions = nameSpace.get('__overloads__', None)
    if overLoadedFunctions is None:
      msg = """Expected name space to contain overloads!"""
      raise UnexpectedStateError(msg)
    for (funcName, overloads) in overLoadedFunctions.items():
      def func(*args, **kwargs) -> typing.Any:
        """Replacement function"""
        typeKey = TypeKey(*args)
        typeFunc = overloads.get(typeKey, None)
        if typeFunc is None:
          e = """No overloaded implementation available for given types: 
          %s""" % typeKey
          raise TypeError(justify(e))
        if not isinstance(typeFunc, CallMeMaybe):
          e = """Function associated with given types: %s is not a 
          function."""
          raise TypeError(e)
        return typeFunc(*args, **kwargs)

      setattr(cls, funcName, func)


def overload(*types) -> CallMeMaybe:  # Factory
  """Quick overloading"""
  typeKey = TypeKey(*types)

  def decorator(func: CallMeMaybe) -> CallMeMaybe:
    """Applies decorations to target function"""
    setattr(func, '__overloaded__', typeKey)
    return func

  return decorator
