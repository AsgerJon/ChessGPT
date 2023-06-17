"""The styles package provides centrally defined style settings."""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

from ._fontfamily import Family
from ._basestyle import BaseStyle
from ._styleinstances import backgroundStyle, labelStyle, headerStyle
from ._styleinstances import debugStyle, lightSquareStyle, darkSquareStyle
from ._styleinstances import outlineStyle, textButtonStyle, bezelStyle
from ._styleinstances import baseButtonStyle, hoverButtonStyle, gridStyle
from ._styleinstances import hoveredSquareStyle

ic.configureOutput(includeContext=True)
