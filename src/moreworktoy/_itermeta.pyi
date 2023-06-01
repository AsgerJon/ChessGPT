#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen

from typing import Any, Iterable, NoReturn


class InstanceIterationMeta(type):
  @classmethod
  def __prepare__(mcls, name: str, bases: tuple[type]) -> dict: ...

  def __init__(cls, *args, **kwargs) -> None: ...

  def __call__(cls, *args, **kwargs) -> Any: ...

  def __iter__(cls) -> Iterable: ...

  def _appendInstance(self, newInstance) -> NoReturn:
    pass

  def __old__(self, param, param1) -> object:
    pass


class InstanceIteration(metaclass=InstanceIterationMeta): ...
