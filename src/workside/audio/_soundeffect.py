"""SoundEffect is a subclass of QSoundEffect"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import NoReturn

from PySide6.QtCore import QObject
from PySide6.QtMultimedia import QSoundEffect, QAudioDevice, QMediaDevices
from PySide6.QtWidgets import QApplication
from icecream import ic
from worktoy.core import maybe, plenty
from worktoy.parsing import searchKeys, maybeType
from worktoy.stringtools import stringList

from moreworktoy import ArgumentError
from workside.audio import Settings
from workside.widgets import CoreWidget

ic.configureOutput(includeContext=True)
Device = QAudioDevice


class _SoundEffectProperties(QSoundEffect):
  """This class provides the properties for the sound effect class
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  @staticmethod
  def getOutputDeviceByName(deviceName: str = None) -> QAudioDevice:
    """Returns the first instance of QAudioDevice having deviceName in its
    description."""
    deviceName = maybe(deviceName, Settings.deviceName)
    if not isinstance(deviceName, str):
      raise TypeError
    for device in QMediaDevices.audioOutputs():
      if deviceName.lower() in device.description().lower():
        return device
    msg = """Unable to find an output device named: %s!"""
    raise NameError(msg % deviceName)

  @classmethod
  def parseDevice(cls, *args, **kwargs) -> QAudioDevice:
    """Parses arguments to obtain audio device"""
    deviceKeys = stringList('device, target, output, speaker')
    deviceKwarg = searchKeys(*deviceKeys) >> kwargs
    if isinstance(deviceKwarg, str):
      deviceKwarg = cls.getOutputDeviceByName(deviceKwarg)
    deviceArg = maybeType(QAudioDevice, *args)
    deviceDefault = cls.getOutputDeviceByName()
    device = maybe(deviceKwarg, deviceArg, deviceDefault)
    if isinstance(device, QAudioDevice):
      return device
    raise TypeError

  @classmethod
  def parseArgs(cls, *args, **kwargs) -> tuple[Device, QObject]:
    """Parses arguments to QAudioDevice and QObject instances that are
    required for instances of this class. In particular, the parent
    QObject which ensures that instances do not get garbage collected."""
    device = cls.parseDevice(*args, **kwargs)
    parent = CoreWidget.parseParent(*args, **kwargs)
    parent = maybe(parent, QApplication.instance())
    if not plenty(device, parent):
      missingArgs = []
      if device is None:
        missingArgs.append(device)
      if parent is None:
        missingArgs.append(parent)
      raise ArgumentError(*missingArgs)
    if not isinstance(device, QAudioDevice):
      raise TypeError
    if not isinstance(parent, QObject):
      raise TypeError
    return (device, parent,)

  def __init__(self, *args, **kwargs) -> None:
    device, parent = self.parseArgs(*args, **kwargs)
    QSoundEffect.__init__(self, device, parent)
    self._device = device
    self._parent = parent


class _SoundEffectSignals(_SoundEffectProperties):
  """Class providing signals for the SoundEffect class"""

  def __init__(self, *args, **kwargs) -> None:
    _SoundEffectProperties.__init__(self, *args, **kwargs)


class SoundEffect(_SoundEffectSignals):
  """Subclass of QSoundEffect"""

  def __init__(self, *args, **kwargs) -> None:
    _SoundEffectSignals.__init__(self, *args, **kwargs)
    self._fileName = None
