"""The illegalAccessorFunction creates an illegal accessor function"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from enum import Enum, IntEnum
from typing import Never

from icecream import ic
from worktoy.core import maybe
from worktoy.parsing import extractArg, maybeType
from worktoy.stringtools import stringList, monoSpace
from worktoy.typetools import CallMeMaybe
from worktoy.waitaminute import ReadOnlyError, UnexpectedStateError

from moreworktoy import ArgumentError

ic.configureOutput(includeContext=True)


class Accessor(IntEnum):
  """Accessor types"""

  @staticmethod
  def illegalAnnotations() -> dict:
    """Annotations for illegal accessor function"""
    return {'return': 'Never'}

  @staticmethod
  def parseArguments(*args, **kwargs) -> tuple[str, str]:
    """Parses arguments to variable and owner name"""
    nameKeys = stringList('name, varName, variable, variableName')
    nameDefault = 'variable'
    ownerKeys = stringList('owner, ownerName, parent, class_, cls')
    ownerDefault = 'owner'
    name, args, kwargs = extractArg(str, nameKeys, *args, **kwargs)
    owner, args, kwargs = extractArg(str, ownerKeys, *args, **kwargs)
    name, owner = maybe(name, nameDefault), maybe(owner, ownerDefault)
    if isinstance(name, str) and isinstance(owner, str):
      return (name, owner)

  DEL = 0
  GET = 1
  SET = 2

  @classmethod
  def fromValue(cls, value: int) -> Accessor:
    """Finds the instance having given value"""
    if not isinstance(value, int):
      msg = monoSpace("""Expected given value to be of type '%s', 
      but received '%s' of type '%s'!""")
      valueString = value.__str__()
      valueType = type(value)
      raise TypeError(msg % (int, valueString, valueType))
    for instance in cls:
      if instance.value == value:
        return instance
    msg = monoSpace(
      """Unable to find instance of '%s' having value: '%s'!""")
    clsName = getattr(cls, '__qualname__', None)
    clsName = maybe(clsName, getattr(cls, '__name__', None))
    valueName = '%s' % (value)
    raise ValueError(msg % (valueName, clsName))

  @classmethod
  def fromString(cls, name: str) -> Accessor:
    """Finds the instance having given name. Please note that this method
    is case-insensitive."""
    if not isinstance(name, str):
      msg = monoSpace("""Expected given name to be of type '%s', 
      but received '%s' of type '%s'!""")
      nameString = name.__str__()
      nameClass = getattr(name, '__class__', None)
      nameType = maybe(nameClass, type(name))
      nameTypeString = getattr(nameType, '__qualname__', None)
      nameTypeString = maybe(
        nameTypeString, getattr(nameType, '__name__', None))
      nameTypeString = maybe(nameTypeString, '%s' % nameType)
      raise TypeError(msg % (str, nameString, nameTypeString))
    for instance in cls:
      if instance.name.lower() == name.lower():
        return instance
    msg = """Failed to find instance named '%s' in the instances of '%s'."""
    className = getattr(cls, '__qualname__', None)
    className = maybe(className, getattr(cls, '__name__', None))
    className = maybe(className, '%s' % cls)
    raise NameError(msg % (name, className))

  def __str__(self) -> str:
    """String Representation"""
    base = None
    if self is Accessor.DEL:
      return 'Deleter-function'
    if self is Accessor.GET:
      return 'Getter-function'
    if self is Accessor.SET:
      return 'Setter-function'
    if base is None:
      msg = monoSpace("""Instance %s was not recognized as instance of 
      indicated parent: %s!""")
      raise UnexpectedStateError(msg % self, self.__class__.__qualname__)

  def docFactory(self, *args, **kwargs) -> str:
    """Docstring factory"""
    varName, ownerName = self.parseArguments(*args, **kwargs)
    return '%s for %s on %s' % (self, varName, ownerName)

  def illegalDocFactory(self, *args, **kwargs) -> str:
    """Docstring for illegal accessors"""
    varName, ownerName = self.parseArguments(*args, **kwargs)
    base = 'Illegal %s' % (self)
    msg = """'%s' for '%s' on '%s'"""
    return msg % (base.lower(), varName, ownerName)


def illegalAccessorFactory(name: str, op: str) -> CallMeMaybe:
  """Factory creating illegal accessor factory. This method is coming to
  WorkToy in the future!"""

  def func(__, *_) -> Never:
    """Docstring"""
    raise ReadOnlyError(name)

  return func


def noAcc(*args, **kwargs) -> CallMeMaybe:
  """Decorator on illegal accessors. This sets a relevant docstring and
  annotations"""
  if not args:
    raise ArgumentError('The function to be decorated')
  if not isinstance(args[0], CallMeMaybe):
    msg = """Expected first positional argument to be a function to be 
    decorated, but found: %s of type %s"""
    raise TypeError(monoSpace(msg) % (args[0], type(args[0])))
  target = args[0]
  accKeys = stringList('operation, accessor, accessorType, acc')
  acc, args, kwargs = extractArg(Accessor, accKeys, *args, **kwargs)
  if acc is None:
    accInt, args, kwargs = extractArg(int, accKeys, *args, **kwargs)
    acc = Accessor.fromValue(accInt)
