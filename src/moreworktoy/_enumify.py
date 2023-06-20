"""Enumify provides for a more flexible implementation of enums"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic
from worktoy.waitaminute import InstantiationError

ic.configureOutput(includeContext=True)

Bases = tuple[type, ...]


class EnumifyMeta(type):
  """Enumify provides for a more flexible implementation of enums
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @staticmethod
  def _isDunder(name: str) -> bool:
    """Checks if a name is a dunder type name"""
    return True if name.startswith('__') and name.endswith('__') else False

  @classmethod
  def __prepare__(mcls, name: str, bases=Bases, ) -> dict:
    """Prepares the dictionary"""
    __instances__ = []
    __meta__ = mcls
    __bases__ = bases
    __name__ = name
    nameSpace = dict(
      __instances__=__instances__,
      __meta__=__meta__,
      __bases__=__bases__,
      __name__=__name__,
    )

    for base in [*bases, ]:
      baseDict = getattr(base, '__dict__', None)
      if baseDict is None:
        raise TypeError
      nameSpace |= baseDict
    return nameSpace

  def __new__(mcls, name: str, _, nameSpace: dict, **kwargs) -> type:
    """Creates the new class. Baseclasses have their bases placed in the
    nameSpace to avoid meta conflicts. Please note, that this is not
    generally a recommendable practice.

    In the new method, items in the name space are seperated into
    callables, dunder-methods and variables. Dunder-methods are ignored,
    callables are decorated with the name of the class being created and
    remaining variables are used at a later state to create instances."""

    for (key, val) in nameSpace.items():
      if not mcls._isDunder(key):
        if callable(val):
          setattr(val, '__class__', name)
    cls = type.__new__(mcls, name, (), nameSpace, **kwargs)
    setattr(cls, 'iterable', lambda *_: getattr(cls, '__instances__'))

  def __init__(cls, name, bases, nameSpace) -> None:
    """Initializes the new class"""
    type.__init__(cls, name, (), nameSpace)

  def __call__(cls, name: str, ) -> object:
    """Instance creation"""
    for (key, val) in cls.__dict__.items():
      if val == '__instance__':
        setattr(cls, key, cls(key))
    out = getattr(cls, name, None)
    if out is None:
      raise InstantiationError()
    return out


class Enumify(metaclass=EnumifyMeta):
  """Intermediary class bringing the metaclass functionality"""
  pass
