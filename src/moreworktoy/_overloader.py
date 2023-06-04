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
  from typing import Any
else:
  from worktoy.typetools import Any

Bases = tuple[type, ...]

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

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases) -> dict:
    """Prepares namespace"""
    baseNames = []
    for base in bases:
      baseNames.append(base.__name__)
    baseNames.append(name)
    nameSpace = {
      '__meta__'     : mcls,
      '__name__'     : name,
      '__qualname__' : '.'.join(baseNames),
      '__overloads__': []
    }
    return nameSpace

  def __new__(mcls, name: str, bases: tuple[type], nameSpace: dict) -> type:
    """OverLoad is a metaclass enabling overloading
    #  MIT Licence
    #  Copyright (c) 2023 Asger Jon Vistisen"""
    overloads = {}
    for (key, val) in nameSpace.items():
      typeKey = getattr(val, '__overloaded__', None)
      if typeKey is not None:
        setattr(val, '__recursion_flag__', False)
        funcName = val.__name__
        if overloads.get(funcName, None) is None:
          overloads |= {funcName: {}}
        overloads[funcName] |= {typeKey: val}
    nameSpace['__overloads__'] = overloads
    return super().__new__(mcls, name, bases, nameSpace)

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
        if typeFunc.__recursion_flag__:
          raise RecursionError
        setattr(typeFunc, '__recursion_flag__', True)
        out = typeFunc(*args, *kwargs)
        return

      setattr(cls, funcName, func)


class OverLoad:
  """Callable decorator"""

  def __init__(self, *types) -> None:
    self._key = TypeKey(*types)
    self._out = None
    self._func = None

  def __rshift__(self, other: TypeKey | Bases) -> OverLoad:
    """Sets the output to other explicitly"""
    if isinstance(other, TypeKey):
      self._out = other
      return self
    if isinstance(other, tuple):
      if all([isinstance(type_, type) for type_ in other]):
        return self >> TypeKey(*other)
      msg = 'Found object of type other than type in other!'
      raise TypeError(msg)
    if isinstance(other, list):
      return self >> TypeKey(*other)

  def __call__(self, *args, **kwargs) -> OverLoad:
    """If private variable '_func_ is None, then assumes that a single
    positional argument containing a function to be decorated. Otherwise,
    assumes a function call to wrapped function."""
    if self._func is None:
      self._func = args[0]
      return self
    if self._out is None:
      return self._invokeFunction(*args, **kwargs)

  def _invokeFunction(self, *args, **kwargs) -> Any:
    """Invokes function"""
    return self._func(*args, **kwargs)


OverLoad()


def overload(*types) -> CallMeMaybe:  # Factory
  """Quick overloading"""
  typeKey = TypeKey(*types)

  def decorator(func: CallMeMaybe) -> CallMeMaybe:
    """Applies decorations to target function"""
    setattr(func, '__overloaded__', typeKey)
    return func

  return decorator


class OverLoadify(metaclass=OverloadMeta):
  """OverLoadify"""
  pass


class OverLoad:
  """Referred to be overloaded classes"""

  def __init__(self, className: str) -> None:
    self._className = className
    self._functions = {}

  def __call__(self, *args, **kwargs) -> Any:
    """Either assigns the class or invokes the function"""

  def _assignClass(self, cls: type) -> OverLoad:
    """Assigns the class"""


class OuterLoaded:
  """Outer replacement. The overloaded class calls an instance of this
  class in replacement of an overloaded function."""

  def __init__(self, className: str, funcName: str) -> None:
    self._innerLoaded = []

  def __call__(self, *args, **kwargs) -> Any:
    """Invokes the function appropriate to the keys"""
    for func in self._innerLoaded:
      res = func(*args, **kwargs)
      if res[0]:
        return res[1]
    key = TypeKey.keyLike()
    msg = """No support found for given type signature: %s""" % key
    raise TypeError(msg)


class InnerLoaded:
  """The inner replacement"""

  def __init__(self, key: TypeKey, func: CallMeMaybe) -> None:
    self._key = key
    self._func = func

  def getKey(self) -> TypeKey:
    """Getter-function for key"""
    return self._key

  def _invokeFunction(self, *args, **kwargs) -> Any:
    """Invokes the function"""
    return self._func(*args, **kwargs)

  def _compareKey(self, *args, **kwargs) -> bool:
    """Compares arguments to keys"""
    if len(args) != len(self.getKey()):
      return False
    for (arg, type_) in zip(args, self.getKey()):
      if not isinstance(arg, type_):
        return False
    return True

  def __call__(self, *args, **kwargs) -> Any:
    """Compares arguments to keys and invokes function if match"""
    if self._compareKey(*args, **kwargs):
      return (True, self._invokeFunction(*args, **kwargs))
    return (False, None)


def decorate(*types) -> CallMeMaybe:
  """This is the function written by the user. """
  key = TypeKey(*types)


def outerFactory(func: CallMeMaybe) -> typing.NoReturn:
  """This collects the function"""


def innerFactory(key: TypeKey, funcName: str) -> CallMeMaybe:
  """This factory returns the function matching the typeKey and function
  name"""


def innerOverload(func: CallMeMaybe, *args, **kwargs) -> Any:
  """This function is what should be invoked"""
  return func(*args, **kwargs)
