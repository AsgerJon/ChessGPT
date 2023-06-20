"""PaintMeLike instances decorates paintEvent methods. The class is
abstract meaning that it should be subclassed. Instances of the subclasses
can then be further specialised at instantiation time. The logic flows in
the following order:

  0 - Creation the abstract base class PaintMeLike. In the future,
  this may include inheriting from custom metaclasses.
  1 - Creation of subclass. Limit responsibilities of each subclass as the
  required coding seems to increase exponentially with the amount of
  responsibilities place on each subclass.
  2 - Instantiation of decorator. This step occurs when decorating the
  paintEvent method directly or decorating the class whose paintEvent is
  to be decorated. The baseclass handles both cases automatically.
  Decorating the class itself rather than the paintEvent directly is
  recommended for reasons described below.
  3a - Decorating the paintEvent directly. During this step, the instance
  of the subclass receives the paintEvent, but does not automatically
  become aware of the class to which this paintEvent belongs.

"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from icecream import ic

ic.configureOutput(includeContext=True)


class PaintMeLike:
  """"""
