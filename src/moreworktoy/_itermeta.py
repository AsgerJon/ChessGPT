"""IterMeta enables classes to be iterable over their instances"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any, Iterable


class InstanceIterationMeta(type):
  """IterMeta enables classes to be iterable over their instances
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @classmethod
  def __prepare__(mcls, name: str, bases: tuple[type]) -> dict:
    """Places the __meta__ identifier"""
    return {'__meta__': mcls}

  def __init__(cls, *args, **kwargs) -> None:
    """Class initialisation"""
    super().__init__(*args, **kwargs)
    cls._instances = []

  def __call__(cls, *args, **kwargs) -> Any:
    """Instance Creation"""
    instance = super().__call__(*args, **kwargs)
    cls._instances.append(instance)
    setattr(instance, '__cls__', cls)
    return instance

  def __iter__(cls) -> Iterable:
    """Implementation of iteration"""
    yield from cls._instances


class InstanceIteration(metaclass=InstanceIterationMeta):
  """Intermediary class"""
  pass
