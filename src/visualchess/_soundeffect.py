"""SoundEffect is a subclass of QSoundEffect"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from PySide6 import QtMultimedia
from PySide6.QtMultimedia import QSoundEffect, QAudioDevice, QMediaDevices
from icecream import ic
from worktoy.core import maybe
from worktoy.parsing import searchKeys, maybeType
from worktoy.stringtools import stringList

from visualchess import Settings

ic.configureOutput(includeContext=True)

Device = QtMultimedia.QAudioDevice


class SoundEffect(QSoundEffect):
  """SoundEffect is a subclass of QSoundEffect
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
      if deviceName in device.description():
        return device
    msg = """Unable to find an output device named: %s!"""
    raise NameError(msg % deviceName)

  def __init__(self, *args, **kwargs) -> None:
    deviceKeys = stringList('device, target, output, speaker')
    deviceKwarg = searchKeys(*deviceKeys) >> kwargs
    if isinstance(deviceKwarg, str):
      deviceKwarg = self.getOutputDeviceByName(deviceKwarg)
    deviceArg = maybeType(Device, *args)
    deviceDefault = self.getOutputDeviceByName('Razer')
    device = maybe(deviceKwarg, deviceArg, deviceDefault)
