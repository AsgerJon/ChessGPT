from PySide6.QtGui import QFont
from enum import Enum
from worktoy.field import BaseField

class Family(Enum):
    arial: str
    timesNewRoman: str
    courierNew: str
    verdana: str
    tahoma: str
    calibri: str
    comicSansMs: str
    helvetica: str
    geneva: str
    lucidaGrande: str
    dejavuSans: str
    dejavuSerif: str
    dejavuSansMono: str
    liberationSans: str
    liberationSerif: str
    liberationMono: str
    ubuntu: str
    cantarell: str
    droidSans: str
    droidSerif: str
    roboto: str
    robotoCondensed: str
    robotoMono: str
    notoSans: str
    notoSerif: str
    notoSansMono: str
    sourceSansPro: str
    sourceSerifPro: str
    sourceCodePro: str
    def asQFont(self, size: int = ...) -> QFont: ...

class BrushField(BaseField):
    def __init__(self, *args) -> None: ...

class PenField(BaseField):
    def __init__(self, *args) -> None: ...

class FontField(BaseField):
    def __init__(self, *args) -> None: ...
