from enum import IntEnum
from typing import Any

class Button(IntEnum):
    LEFT: int
    RIGHT: int
    MIDDLE: int
    FORWARD: int
    BACK: int
    def flag(self) -> Any: ...
    def __eq__(self, other: Any) -> bool: ...
