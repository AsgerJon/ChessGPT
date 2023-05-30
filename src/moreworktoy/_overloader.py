"""OverLoad is a metaclass enabling overloading"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from icecream import ic
from worktoy.parsing import maybeTypes, searchKeys
from worktoy.stringtools import stringList
from worktoy.typetools import CallMeMaybe

if TYPE_CHECKING:
  from typing import Any
else:
  from worktoy.typetools import Any

ic.configureOutput(includeContext=True)


class OverloadMeta(type):
  """OverLoad is a metaclass enabling overloading
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def __new__(mcls, name, bases, attrs) -> type:
    """OverLoad is a metaclass enabling overloading
    #  MIT Licence
    #  Copyright (c) 2023 Asger Jon Vistisen"""
    overloads = {}
    for attr_name, attr_value in attrs.items():
      if hasattr(attr_value, '__overload__'):
        for arg_types in attr_value.__overload__:
          if overloads.get(attr_name, None) is None:
            overloads |= {attr_name: {}}
          overloads[attr_name] |= {(*arg_types,): attr_value}
    attrs['__overload__'] = overloads
    return super().__new__(mcls, name, bases, attrs)

  def __init__(cls, name, bases, attrs) -> None:
    super().__init__(name, bases, attrs)
    for attr_name, attr_value in attrs.items():
      if hasattr(attr_value, '__overload__'):
        setattr(cls, attr_name, cls.overLoadFactory(attr_name))

  @classmethod
  def overLoadFactory(cls, method_name) -> CallMeMaybe:
    """Creates the overload replacement"""

    def overloaded_method(self, *args, **kwargs) -> Any:
      """Finds the type appropriate overloading method"""
      typeKey = tuple(type(arg) for arg in args)
      overloads = self.__class__.__overload__[method_name][typeKey]
      return overloads(self, *args, **kwargs)

    return overloaded_method


class _ClassNames(list):
  """Without Append"""
  __content_class__ = int  # Specify the desired content class

  def __new__(cls, *args, **kwargs):
    filtered_args = [item for item in args[0] if
                     isinstance(item, cls.__content_class__)]
    return super().__new__(cls, filtered_args)

  def append(self, item):
    raise AttributeError("Appending to _AppendNot is not allowed.")

  def extend(self, iterable):
    raise AttributeError("Extending _AppendNot is not allowed.")


class _FuncOverLoad:
  """Overloaded functions become members of this class"""

  @staticmethod
  def _whatClass(func: CallMeMaybe) -> str:
    """Identifies the name of the class to which a method belongs"""
    return func.__qualname__.split('.')[0]

  _functions = []
  _functionNames = []
  _instances = {}

  _classes = {}

  @classmethod
  def _getClassNames(cls) -> _ClassNames:
    """Getter-function for list of named classes"""
    return _ClassNames([k for (k, v) in cls._classes.items()])

  @classmethod
  def _takeFactory(cls, *types) -> CallMeMaybe:
    """Invoked by overload"""

    def take(*args, **kwargs) -> Any:
      """Takes the overloaded function"""

    return take

  def __init__(self, *args, **kwargs) -> None:
    self._types = maybeTypes(type, *args)
    scopeKeys = stringList('scope, class, class_, type, type_')
    self._scopeClass = searchKeys(*scopeKeys) @ type >> kwargs
    funcKeys = stringList('func, function, method')
    self._function = searchKeys(*funcKeys) @ CallMeMaybe >> kwargs

  def __call__(self, *args, **kwargs) -> type:
    """Calling the function..."""

  @classmethod
  def _createFunctionEntry(cls, func: CallMeMaybe) -> bool:
    """Creates an entry in dictionary for given function"""
    if not cls._appendFunction(func):
      return False

  @classmethod
  def _appendFunction(cls, func: CallMeMaybe) -> bool:
    """Appends function to list of functions if it is not already"""
    if func.__name__ in cls._functionNames or func in cls._functions:
      return False
    cls._getFunctionNames().append(func.__name__)
    cls._getFunctions().append(func)
    return True

  @classmethod
  def _getFunctionNames(cls) -> list[str]:
    """Getter-function for function names"""
    return cls._functionNames

  @classmethod
  def _getFunctions(cls) -> list[CallMeMaybe]:
    """Getter-function for functions"""
    return cls._functions

  @classmethod
  def _getInstances(cls) -> dict[str, _FuncOverLoad]:
    """Returns list of instances"""
    return cls._instances

  @classmethod
  def _isFuncLoaded(cls, func: CallMeMaybe) -> bool:
    """Checks if given function is already loaded."""
    return True if func.__name__ in cls._getFunctionNames() else False

  @classmethod
  def overLoad(cls, *types, **kwargs) -> Any:
    """This function applies the overloading."""


class OverLoad(metaclass=OverloadMeta):
  """Subclasses of OverLoad support function overloading. """
