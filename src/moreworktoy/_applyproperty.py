"""ApplyProperty class that creates decorators to apply a
    property to the decorated class."""
#  MIT License
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Type


class ApplyProperty:
  """ApplyProperty class that creates decorators to apply a
  property to the decorated class.

  Args:
      propName (str): The name of the property.
  #  MIT License
  #  Copyright (c) 2023 Asger Jon Vistisen
    """

  def __init__(self, propName: str):
    self._propName = propName

  def __call__(self_, cls: Type) -> Type:
    """Decorates a class with a property.

    Args:
        cls (Type): The class to decorate.

    Returns:
        Type: The decorated class.
    """
    original_cls_setattr = cls.__setattr__

    def new_cls_setattr(self, name, value):
      if name == self._propName:
        # Custom logic for setting the property value
        print(f"Setting property '{self._propName}' to: {value}")
      else:
        # Call the original setattr for other attributes
        original_cls_setattr(self, name, value)

    def prop_getter(self):
      # Custom logic for getting the property value
      print(f"Getting property '{self._propName}'")
      return getattr(self, f"_{self._propName}")

    def prop_setter(self, value):
      # Custom logic for setting the property value
      print(f"Setting property '{self._propName}' to: {value}")
      setattr(self, f"_{self._propName}", value)

    setattr(cls, self_._propName, property(prop_getter, prop_setter))
    cls.__setattr__ = new_cls_setattr

    return cls
