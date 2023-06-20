"""Flag is a class decorator"""
#  Copyright (c) 2023 Asger Jon Vistisen
#  MIT Licence
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QEvent
from PySide6.QtGui import QEnterEvent, QPainterPath
from icecream import ic
from worktoy.typetools import CallMeMaybe
from worktoy.waitaminute import ProceduralError

ic.configureOutput(includeContext=True)


def flag(flagName: str) -> CallMeMaybe:
  """Factory for decorator functions"""

  def decorator(cls: type) -> type:
    """The actual decorator returned by the factory"""
    _name = '_%s' % flagName
    Name = '%s%s' % (flagName[0].upper(), flagName[1:])
    _setName = '_set%s' % (Name)
    _getName = '_get%s' % (Name)
    _deactivatorName = 'deactivate%s' % Name
    _activatorName = 'activate%s' % Name

    init = getattr(cls, '__init__', None)
    if init is None:
      raise KeyError('__init__')

    def getFlag(self) -> bool:
      """Get the value of the flag."""
      return True if getattr(self, _name, ) else False

    def setFlag(self, value) -> NoReturn:
      """Set the value of the flag."""
      setattr(self, _name, value)

    def activateFlag(self) -> NoReturn:
      """Activate the flag."""
      setattr(self, _name, True)

    def deactivateFlag(self) -> NoReturn:
      """Deactivate the flag."""
      setattr(self, _name, False)

    def _postInit(self, ) -> NoReturn:
      """Extra __init__"""
      setattr(self, _name, False)
      pointF = getattr(self, 'getViewPort')().center().toPointF()
      enterEvent = QEnterEvent(pointF, pointF, self.mapToGlobal(pointF), )
      getattr(self, 'enterEvent')(enterEvent)
      getattr(self, 'leaveEvent')(QEvent(QEvent.Leave))

    def newInit(self, *args, **kwargs) -> NoReturn:
      """New init function"""
      init(self, *args, **kwargs)
      _postInit(self)

    setattr(cls, '__init__', newInit)

    setattr(cls, flagName, property(getFlag, setFlag))
    setattr(cls, _deactivatorName, activateFlag)
    setattr(cls, _activatorName, deactivateFlag)
    setattr(cls, _getName, getFlag)
    setattr(cls, _setName, setFlag)

    flagGetters = getattr(cls, 'flagGetters', [])
    flagNames = getattr(cls, 'flagNames', [])
    if getFlag in flagGetters:
      raise ProceduralError('Same flag applied a second time')
    flagGetters.append(getFlag)
    flagNames.append(flagName)
    setattr(cls, 'flagGetters', flagGetters)
    setattr(cls, 'flagNames', flagNames)

    return cls

  return decorator
