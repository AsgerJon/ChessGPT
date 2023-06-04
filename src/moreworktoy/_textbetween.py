"""The textBetween function finds text between given tags"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations
import re

from icecream import ic

ic.configureOutput(includeContext=True)


def textBetween(text, openTag, closeTag) -> list[str]:
  """The textBetween function finds text between given tags
  #  MIT Licence
  #  Copyright (c) 2023 Asger Jon Vistisen"""
  opened = re.escape(openTag)
  middle = r'([^' + re.escape(closeTag) + r']*)'
  closed = re.escape(closeTag)
  pattern = opened + middle + closed
  matches = re.findall(pattern, text)
  return matches
