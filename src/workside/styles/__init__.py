"""The styles package provides centrally defined style settings."""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations
from icecream import ic
from worktoy.waitaminute import n00bError

ic.configureOutput(includeContext=True)

from ._fontfamily import Family
from ._basestyle import BaseStyle
from ._styleinstances import backgroundStyle, labelStyle, headerStyle
from ._styleinstances import debugStyle, lightSquareStyle, darkSquareStyle
from ._styleinstances import outlineStyle
