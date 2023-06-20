"""The ClassAware method uses a custom metaclass that sets a __cls__
attribute on each attribute in subclasses to the class to which the method
belongs. The following entries in the namespace are exempted: entries
where the key is in dunder format, such as __...__ or where the value is
of an immutable type."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from icecream import ic

ic.configureOutput(includeContext=True)


class _ClassAwareMeta(type):
  """This private class is the actual custom metaclass"""

  _immutableTypes = [
    int,
    float,
    complex,
    bool,
    str,
    bytes,
    frozenset,
    type(None)
  ]

  @classmethod
  def _getImmutableTypes(mcls) -> list[type]:
    """Getter-function for list of immutable types"""
    return mcls._immutableTypes

  @classmethod
  def _isImmutable(mcls, obj: object) -> bool:
    """Checks if given object is of an immutable type"""
    for type_ in mcls._getImmutableTypes():
      if isinstance(obj, type_):
        return True
    return False

  @staticmethod
  def _isDunder(key: str) -> bool:
    """Checks if given key is in dunder format"""
    return True if key.startswith('__') and key.endswith('__') else False

  @classmethod
  def _isExempt(mcls, *args, **kwargs) -> bool | dict[str, object]:
    """Checks if given obj is exempt from getting the __cls__ attribute.
    If positional arguments are given, the first such of string-type is
    assumed to be the key and the first positional argument other than the
    key is assumed to be the object. If using keyword arguments,
    this takes precedence over positional arguments. In this case a
    dictionary will be returned which containing the entries found in the
    keyword arguments which are NOT exempt from receiving the attribute.
    Please note, that in early development, support for keyword arguments
    may not be fully implemented."""
    if kwargs:
      msg = """Support for keyword arguments is not yet implemented!"""
      raise NotImplementedError(msg)
