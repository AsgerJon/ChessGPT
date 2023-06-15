"""StateStyle subclasses BaseStyle and provides style values that are
dependent on the state of the widget. Rather than instantiating
StateStyle, it should be subclassed further to tailor itself to a subclass
of CoreWidget. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6.QtGui import QBrush
from icecream import ic
from worktoy.typetools import CallMeMaybe

from workside.styles import BaseStyle

ic.configureOutput(includeContext=True)


class StateStyle(BaseStyle):
  """StateStyle subclasses BaseStyle and provides style values that are
  dependent on the state of the widget.
  #  Copyright (c) 2023 Asger Jon Vistisen
  #  MIT Licence"""
