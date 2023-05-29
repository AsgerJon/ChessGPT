"""FileRankStyle defines the style of the letters and numbers indicate
files and ranks respectively"""
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from visualchess.styles import Family, BaseStyle


class FileRankStyle(BaseStyle):
  context = 'fileRankStyle'
  fontFamily = Family.helvetica
  fontSize = 20
