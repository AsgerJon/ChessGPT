"""IterMeta enables classes to be iterable over their instances"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Iterable, NoReturn

Types = tuple[type]


class InstanceIterationMeta(type):
  """IterMeta enables classes to be iterable over their instances
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
  def __prepare__(mcls, name: str, bases: Types) -> dict:
    """Places the __meta__ identifier"""
    nameSpace = {'__meta__': mcls, '__index__': 0, '__instances__': []}
    for base in bases:
      nameSpace |= base.__dict__
    return nameSpace

  @classmethod
  def __new__(mcls, name: str, bases: Types, nameSpace: dict, **kws) -> type:
    """Creates the new class"""
    cls = super().__new__(mcls, name, bases, nameSpace)
    for (key, val) in nameSpace.items():
      if not (mcls._isDunder(key) or mcls._checkType(val)):
        setattr(val, '__cls__', cls)
        setattr(cls, key, val)
    return cls

  def __init__(cls, *args, **kwargs) -> None:
    """Class initialisation"""
    super().__init__(*args, **kwargs)

  def __call__(cls, *args, **kwargs) -> object:
    """Instance Creation"""
    if kwargs.get('_root', False):
      newInstance = super().__call__(*args, **kwargs)
      cls._appendInstance(newInstance)
      return newInstance
    return cls.__old__(*args, **kwargs)

  def __old__(cls, *args, **kwargs) -> object:
    """Abstract method responsible for returning an existing instances.
    Classes must implement this method."""

  def _appendInstance(cls, instance: object) -> NoReturn:
    """Appends given instance to the list of instances"""
    if not isinstance(instance, cls):
      raise TypeError
    __instances__ = getattr(cls, '__instances__', None)
    if not isinstance(__instances__, list):
      raise TypeError
    setattr(cls, '__instances__', [*__instances__, instance])

  def _getIndex(cls) -> int:
    """Getter-function for the current index"""
    index = getattr(cls, '__index__', None)
    if isinstance(index, int):
      return index
    raise TypeError

  def _setIndex(cls, index: int) -> NoReturn:
    """Setter-function for the current index"""
    setattr(cls, '__index__', index)

  def _incIndex(cls) -> NoReturn:
    """Incrementor-function for the current index"""
    cls._setIndex(cls._getIndex() + 1)

  def _decIndex(cls) -> NoReturn:
    """Decrement-function for the current index"""
    cls._setIndex(cls._getIndex() - 1)

  def __len__(cls) -> int:
    """Length is the number of instances"""
    __instances__ = getattr(cls, '__instances__', None)
    return len(__instances__)

  def __iter__(cls) -> type:
    """Implementation of iteration"""
    setattr(cls, '__index__', 0)
    return cls

  def __next__(cls) -> object:
    """Implementation of iteration"""
    cls._incIndex()
    index = cls._getIndex()
    __instances__ = getattr(cls, '__instances__', None)
    if index > len(cls):
      raise StopIteration
    return __instances__[index - 1]


class InstanceIteration(metaclass=InstanceIterationMeta):
  """Intermediary class"""
  pass
