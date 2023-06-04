"""PaintFactory is a class moving the painting operations from QWidget
paint event to a central class that can paint both dynamic QWidgets
and static QPixmap images. This will also be located centrally with the
central style settings. This separates graphics entirely from the QWidget
class chain."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

ic.configureOutput(includeContext=True)
