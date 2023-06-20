"""The Settings class provides all of the Settings used by the audio
package. Other packages in WorkSide looks for these settings as class
variables. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from icecream import ic

ic.configureOutput(includeContext=True)


class Settings:
  """The Settings class provides all of the Settings used by the audio
  package. Other packages in WorkSide looks for these settings as class
  variables.
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""

  deviceName = 'razer'
