from moreworktoy import Index as Index
from worktoy.parsing import maybeType as maybeType

class TypeKey:
    @classmethod
    def keyLike(cls, *args, **kwargs) -> TypeKey: ...
    def __init__(self, *args, **kwargs) -> None: ...
    def __hash__(self) -> int: ...
    def __eq__(self, other: TypeKey) -> bool: ...
    def iterable(self) -> list: ...
    def __instancecheck__(self, instance: tuple | list) -> bool: ...
