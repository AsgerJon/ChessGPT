"""AbstractStyleStates is a class providing decorators for the getter
functions
used by subclasses of BaseStyle. These decorators are instances of
StyleStates subclasses."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from abc import abstractmethod
from typing import NoReturn, Any

from icecream import ic
from worktoy.stringtools import monoSpace
from worktoy.typetools import CallMeMaybe
from worktoy.waitaminute import UnexpectedStateError

from workside.widgets import CoreWidget

ic.configureOutput(includeContext=True)


class AbstractStyleStates:
  """AbstractStyleStates is a class providing decorators for the getter
  functions
  used by subclasses of BaseStyle. These decorators are instances of
  StyleStates subclasses.

  Each subclass should match one subclass of CoreWidgets. Each such
  subclass should be able to recognize the current states of the given
  widget class. Thus, the state analyzer must be a class method.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""

  _primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

  @classmethod
  def getPrimes(cls) -> list[int]:
    """Getter function for the list of primes"""
    return cls._primes

  @staticmethod
  def stateKey(*flags) -> int:
    """Returns the prime key representation of the given flags"""
    key = 1
    for (p, f) in zip(AbstractStyleStates._primes, flags):
      key *= p if f else 1
    return key

  @staticmethod
  def getInstanceFlags(self: object, ) -> list[int]:
    """Here 'self' is the instance of the button."""

    if not isinstance(self, CoreWidget):
      msg = """Expected instance to be an instance of CoreWidget or one of 
      its subclasses, but received: %s!""" % type(self)
      raise TypeError(monoSpace(msg))

    cls = getattr(self, '__class__', None)
    if cls is None:
      raise KeyError('Unable to find \'__class__\' on %s!' % self)

    flagGetters = getattr(cls, 'flagGetters', None)
    if flagGetters is None:
      return []

    return [f(self) for f in flagGetters]

  @staticmethod
  def namedFlagsKey(cls: type, *names) -> int:
    """Creates the number of """
    flagGetters = getattr(cls, 'flagGetters', None)
    flagNames = getattr(cls, 'flagNames', None)
    nameList = [name for name in names]
    key = 1
    primes = AbstractStyleStates.getPrimes()
    for (name, p) in zip(flagNames, primes):
      if name in nameList:
        key *= p
    return key

  def __init__(self, *args, **kwargs) -> None:
    self._func = None
    self._wrappers = {}

  def __call__(self, *args, **kwargs) -> Any:
    """Receives and absorbs the function and replaces it with itself."""
    if self._func is None:
      if isinstance(args[0], CallMeMaybe):
        return self._setFunction(args[0])
      raise TypeError
    return self._stateWrapper(*args, **kwargs)

  def _setFunction(self, func: CallMeMaybe) -> AbstractStyleStates:
    """Setter-function for the underlying function"""
    if self._func is not None:
      raise UnexpectedStateError()
    self._func = func
    return self

  def _wrapper(self, instance: object, *args, **kwargs) -> Any:
    """Wrapper function"""
    if self._func is None:
      raise UnexpectedStateError()
    key = AbstractStyleStates.getInstanceFlags(instance)
    wrapper = self._wrappers.get(key, self._func)
    return wrapper(instance, *args, **kwargs)

  @abstractmethod
  def _stateWrapper(self, instance: object, *args, **kwargs) -> Any:
    """This is the state sensitive wrapper. """


class AbstractButtonStyle(AbstractStyleStates):
  """Subclass relevant to abstract buttons"""
