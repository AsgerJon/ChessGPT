"""PaintOperation instances provides logic for paint event. This way,
subclasses of QWidget need not reimplement paint event, but instead invoke
a subclass of PaintOperation"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

ic.configureOutput(includeContext=True)


class PaintOperation:
  """PaintOperation instances provides logic for paint event. This way,
  subclasses of QWidget need not reimplement paint event, but instead invoke
  a subclass of PaintOperation"""

  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen

  def __init__(self, *args, **kwargs) -> None:
    pass
