"""TypeKey provides keys for the overloaded functions"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from worktoy.parsing import maybeTypes, maybeType, extractArg
from worktoy.stringtools import stringList

from moreworktoy import Index


@Index()
class TypeKey:
  """TypeKey provides keys for the overloaded functions
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @classmethod
  def keyLike(cls, *args, **kwargs) -> TypeKey:
    """Creates an instance of a TypeKey using the types of the positional
    arguments."""
    return cls([type(arg) for arg in args])

  def __init__(self, *args, **kwargs) -> None:
    typeKeyNames = stringList('typeKey, key')
    key, args, kwargs = extractArg(TypeKey, typeKeyNames, *args, **kwargs)
    if key is None:
      self._types = maybeTypes(type, *args)
    else:
      self._types = [type_ for type_ in key]

  def __hash__(self) -> int:
    """Returns the hash of the tuple"""
    return hash((*self._types,))

  def __eq__(self, other: TypeKey) -> bool:
    """Checks if types are the same"""
    if isinstance(other, (list, tuple)):
      return self == TypeKey(*other)
    if len(self) - len(other):
      return False
    for (selfType, otherType) in zip(self, other):
      if selfType != otherType:
        return False
    return True

  def __str__(self) -> str:
    """String representation"""
    words = [type_.__qualname__ for type_ in self]
    return """TypeKey: %s""" % (', '.join(words))

  def __repr__(self) -> str:
    """Code representation"""
    words = [type_.__qualname__ for type_ in self]
    return 'TypeKey(%s)' % ', '.join(words)

  def iterable(self) -> list:
    """Iterable implementation"""
    return [*self._types, ]

  def __instancecheck__(self, instance: tuple | list) -> bool:
    """Implementation of isinstance"""
    if len(instance) - len(self):
      return False
    for (ins, type_) in zip(instance, self):
      if not isinstance(ins, type_):
        return False
    return True
