"""ArgumentError should be invoked where required arguments are missing."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic
from worktoy.parsing import maybeTypes
from worktoy.waitaminute import ExceptionCore

ic.configureOutput(includeContext=True)


class ArgumentError(ExceptionCore):
  """ArgumentError should be invoked where required arguments are missing.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  def _createMsg(self, *args, **kwargs) -> str:
    """Implementation"""
    strArgs = [*maybeTypes(str, *args), ]
    argNames = ', '.join(strArgs)
    _msg = """Missing the following required arguments: %s""" % argNames
    self._msg = _msg
    return _msg
