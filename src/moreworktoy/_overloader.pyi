from moreworktoy import TypeKey as TypeKey
from worktoy.typetools import CallMeMaybe

class OverloadMeta(type):
    def __new__(mcls, name: str, bases: tuple[type], nameSpace: dict) -> type: ...
    def __init__(cls, name: str, bases: tuple[type], nameSpace: dict) -> None: ...

def overload(*types) -> CallMeMaybe: ...
