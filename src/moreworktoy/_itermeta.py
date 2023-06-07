"""IterMeta is a metaclass providing classes with iteration over their
instances."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from worktoy.core import maybe
from worktoy.typetools import CallMeMaybe
from icecream import ic
from worktoy.waitaminute import ProceduralError

Bases = tuple[type, ...]
ic.configureOutput(includeContext=True)


class IterMeta(type):
  """Implementation of instance awareness enabling classes using this
  metaclass to iterate over their instances."""

  @staticmethod
  def _getterFunc(cls: type, key: str, **kwargs) -> object:
    """General getter-function for class"""
    obj = getattr(cls, key, None)
    if obj is None and not kwargs.get('allowNone', False):
      raise AttributeError
    return obj

  @staticmethod
  def _setterFunc(cls: type, key: str, obj: object) -> type:
    """General setter-function for class"""
    setattr(cls, key, obj)
    return cls

  @staticmethod
  def _getInstances(cls: type, ) -> list:
    """Getter-function for class"""
    __instances__ = IterMeta._getterFunc(cls, '__instances__')
    if isinstance(__instances__, list):
      return __instances__
    raise TypeError

  @staticmethod
  def _appendInstance(cls: type, instance: object) -> type:
    """Appends instance to type"""
    __instances__ = [*IterMeta._getInstances(cls, ), instance]
    IterMeta._setterFunc(cls, '__instances__', __instances__)
    return cls

  @staticmethod
  def _getIndex(cls: type, ) -> int:
    """Getter-function for class"""
    __index__ = IterMeta._getterFunc(cls, '__index__', )
    if isinstance(__index__, int):
      return __index__
    raise TypeError

  @staticmethod
  def _setIndex(cls: type, value: int = None) -> type:
    """Getter-function for class"""
    value = maybe(value, 0)
    IterMeta._setterFunc(cls, '__index__', value)
    return cls

  @staticmethod
  def _incIndex(cls, ) -> type:
    """Increments index"""
    value = getattr(cls, '__index__', None)
    if value is None:
      raise AttributeError
    if isinstance(value, int):
      return IterMeta._setIndex(cls, value + 1)
    raise TypeError

  @staticmethod
  def _decIndex(cls, ) -> type:
    """Increments index"""
    value = getattr(cls, '__index__', None)
    if value is None:
      raise AttributeError
    if isinstance(value, int):
      return IterMeta._setIndex(cls, value - 1)
    raise TypeError

  @staticmethod
  def _instanceAtIndex(cls, index: int = None) -> object:
    """Getter-function for the instance at given index or current index"""
    index = maybe(index, IterMeta._getIndex(cls))
    if index is None:
      raise AttributeError
    if isinstance(index, int):
      __instances__ = IterMeta._getInstances(cls)
      n = len(__instances__)
      if isinstance(__instances__, list):
        while index < 0:
          index += n
        if index < n:
          return __instances__[index]
        raise StopIteration
      raise TypeError
    raise TypeError

  @classmethod
  def __prepare__(mcls, name: str, bases: Bases):
    """Introduces __instances__ and __index__ to the namespace"""
    nameSpace = {}
    for base in bases:
      baseDict = IterMeta._getterFunc(base, '__dict__')
      if hasattr(baseDict, 'items'):
        for (key, val) in baseDict.items():
          nameSpace |= {key: val}
      else:
        raise TypeError
    nameSpace |= {'__instances__': [], '__index__': 0}
    nameSpace |= dict(__instance__=[],
                      __index__=0,
                      __createAll__=False,
                      __old__=False,
                      __root__=False,
                      __ready__=False,
                      _recursionFlag=False)
    return nameSpace

  def __new__(mcls, name: str, bases: Bases, attrs: dict, **kwargs) -> type:
    """Creates the new class"""
    newClass = super().__new__(mcls, name, bases, attrs, **kwargs)
    createAll = attrs.get('createAll', None)
    old = attrs.get('__old__', None)
    if createAll is not None:
      if not isinstance(createAll, CallMeMaybe):
        raise TypeError
      newClass.__createAll__ = createAll
    if old is not None:
      if not isinstance(createAll, CallMeMaybe):
        raise TypeError
      newClass.__old__ = old

    # setattr(newClass, '__new__', _new_)

    return newClass

  def __init__(cls, *args, **kwargs) -> None:
    """Initialisation of class"""
    super().__init__(*args, **kwargs)
    createAll = getattr(cls, '__createAll__', None)
    if createAll:
      createAll(cls)
    cls.__ready__ = True
    print('%s reporting ready' % cls)

  def __call__(cls, *args, **kwargs) -> object:
    """Instance creation"""
    out = None
    if cls.__old__:
      out = cls.__old__(*args, **kwargs)
    if out is None:
      out = super().__call__(cls, *args, **kwargs, lol=True)
      cls.__instances__.append(out)
      return out
    return out

  #
  #   _instance = super().__call__(cls, *args, **kwargs, lol=True)
  #   if _instance is not None:
  #     IterMeta._appendInstance(cls, _instance)
  #   return _instance

  def __len__(cls) -> int:
    """Length is the number of instances"""
    if not cls.__ready__:
      raise ProceduralError
    __instances__ = getattr(cls, '__instances__', None)
    if __instances__ is None:
      raise AttributeError
    return len(__instances__)

  def __iter__(cls) -> type:
    """Iterates over instances"""
    if not cls.__ready__:
      raise ProceduralError
    IterMeta._setIndex(cls, 0)
    return cls

  def __next__(cls) -> object:
    """Iterates over instances"""
    if not cls.__ready__:
      raise ProceduralError
    IterMeta._incIndex(cls)
    return IterMeta._instanceAtIndex(cls, cls._getIndex(cls) - 1)


class Iterify(metaclass=IterMeta):
  """Iterify is a parent class implementing instance aware class iteration
  on subclasses. Example:

  class Color(Iterify):
    def __init__(self, r: int, g: int, b: int) -> None:
      self.r, self.g, self.b = r, g, b

  red, green, blue = [Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255)]
  for color in Color:
    print(color)
  produces:
    Color(255, 0, 0)
    Color(0, 255, 0)
    Color(0, 0, 255)"""

  @classmethod
  def createAll(cls, *args, **kwargs) -> NoReturn:
    """Class method which should creates instances. It is invoked at class
    creation time."""

  @classmethod
  def __old__(cls, *args, **kwargs) -> NoReturn:
    """Implement this method to retrieve an existing instance matching
    arguments instead of creating a new one. Have this method return None
    in case no existing instance matching the arguments were found. In
    this case the class will return the return value from the __new__
    method. """
