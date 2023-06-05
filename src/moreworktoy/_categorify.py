"""Categorify is an alternative to Enum"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

ic.configureOutput(includeContext=True)


class _CategorifyMeta(type):
  """Categorify is an alternative to Enum
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @staticmethod
  def _isDunder(name: str) -> bool:
    """Checks if a name is a dunder type name"""
    if not name.startswith('__'):
      return False
    if not name.endswith('__'):
      return False
    return True

  @classmethod
  def __prepare__(mcls, name, bases) -> dict:
    """Prepares the nameSpace."""
    return dict(__name__=name, __members__=[], __index__=0, __NULL__=None)

  def __new__(mcls, name: str, _, nameSpace: dict, **kwargs) -> type:
    """Creates the new type. All instances must be present in the
    nameSpace. All instances of the type are created at the same time at
    the class. All entries in the namespace are treated as instances,
    except for entries where the key is of dunder format or where the
    value is a callable."""
    instanceNames = []
    for (key, val) in nameSpace.items():
      if not (mcls._isDunder(key) or callable(val)):
        instanceNames.append(key)
    nameSpace |= {'__instance_names__': instanceNames}
    return super().__new__(mcls, name, (), nameSpace, **kwargs)

  def __init__(cls, name: str, _, nameSpace: dict, **kwargs) -> None:
    """Initializes the new class"""
    instances = {}
    for name in nameSpace['__instance_names__']:
      instances |= {name: cls()}
    setattr(cls, '__instances_names__', instances)
    super().__init__(name, (), nameSpace)

  def __call__(cls, *args, **kwargs) -> object:
    """Instead of creating a new instance, and attempt is made to
    recognize an existing instance"""


class Categorify(metaclass=_CategorifyMeta):
  """Categorify is an alternative to Enum
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""
  pass
