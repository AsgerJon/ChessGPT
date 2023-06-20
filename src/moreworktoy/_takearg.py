"""The takeArg function removes from a series of positional arguments the
first of a particular type. This is intended to be used with general
parsers allowing them to consume a positional argument, such that it will
not be reused."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

ic.configureOutput(includeContext=True)


def takeArg(type_: type, *args, ) -> dict:
  """The takeArg function removes from a series of positional arguments the
  first of a particular type. This is intended to be used with general
  parsers allowing them to consume a positional argument, such that it will
  not be reused. The return value is a dictionary of the following schema:
  {
    'removed'  : <REMOVED VALUE>   ,
    'remaining': <REMAINING VALUES>,
  }
  In cases where no such type is found, the value associated with
  'removed' will be 'None' and the remaining values will remain intact.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""
  out = []
  removed = None

  for arg in args:
    if isinstance(arg, type_):
      if removed is None:
        removed = arg
      else:
        out.append(arg)
  return dict(removed=removed, remaining=out)
