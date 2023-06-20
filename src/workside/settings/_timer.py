"""The timer function decorates classes with a QTimer"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QTimer, Qt, Slot
from icecream import ic
from worktoy.core import maybe
from worktoy.typetools import CallMeMaybe

ic.configureOutput(includeContext=True)


def timer(timerName: str, interval: int, signal: str = None) -> CallMeMaybe:
  """Factory for decorator functions"""

  def decorator(cls: type) -> type:
    """The actual decorator returned by the factory"""
    _name = '_%sTimer' % timerName
    Name = '%s%s' % (timerName[0].upper(), timerName[1:])
    signalName = maybe(signal, timerName)
    _creatorName = '_create%sTimer' % Name
    _getterName = '_get%sTimer' % Name
    _resetName = '_reset%sTimer' % Name

    init = getattr(cls, '__init__', None)
    if init is None:
      raise KeyError('__init__')

    def _postInit(self, ) -> NoReturn:
      """Extra __init__"""
      setattr(self, _name, None)

    def newInit(self, *args, **kwargs) -> NoReturn:
      """New Init function"""
      init(self, *args, **kwargs)
      _postInit(self, )

    setattr(cls, '__init__', newInit)

    def createTimer(self, ) -> NoReturn:
      """Creator function for the timer"""
      _timer = QTimer()
      _timer.setTimerType(Qt.TimerType.PreciseTimer)
      _timer.setInterval(interval)
      _timer.setSingleShot(True)
      if isinstance(signalName, str):
        _signal = getattr(self, signalName)
      else:
        msg = """Expected signalName to be of type %s, but received %s!"""
        raise TypeError(msg % (str, type(signalName)))
      _timer.timeout.connect(_signal.emit)
      setattr(self, _name, _timer)

    def getTimer(self, ) -> QTimer:
      """Getter-function for the timer"""
      _timer = getattr(self, _name, None)
      if _timer is None:
        _createTimer = getattr(self, _creatorName, )
        _getTimer = getattr(self, _getterName, )
        _createTimer()
        return _getTimer()
      if isinstance(_timer, QTimer):
        return _timer
      eMsg = """Expected a QTimer, but received: %s!""" % (type(_timer))
      raise TypeError(eMsg)

    def resetTimer(self, ) -> QTimer:
      """Resetter-function for the timer"""
      _timer = getattr(self, _name)
      if not isinstance(_timer, QTimer):
        msg = """Expected _timer to be of type %s, but received %s"""
        raise TypeError(msg % (QTimer, type(_timer)))
      _timer.stop()
      _timer.start()
      return _timer

    setattr(cls, _creatorName, createTimer)
    setattr(cls, _getterName, getTimer)

    setattr(cls, _resetName, resetTimer)

    return cls

  return decorator
