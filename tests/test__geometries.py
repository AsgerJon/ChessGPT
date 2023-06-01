#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen

import unittest
from unittest import skip

from PySide6.QtCore import QPoint, QLine, QPointF, QLineF

geometriesF2Int = 'lol'


@skip
class TestGeometries(unittest.TestCase):
  def test_convert_qpointf_to_qpoint(self):
    pointf = QPointF(10.5, 20.7)
    point = geometriesF2Int(pointf)
    self.assertIsInstance(point, QPoint)
    self.assertEqual(point.x(), 10)
    self.assertEqual(point.y(), 20)

  def test_convert_qlinef_to_qline(self):
    linef = QLineF(0.5, 0.5, 10.5, 20.5)
    line = geometriesF2Int(linef)
    self.assertIsInstance(line, QLine)
    self.assertEqual(line.x1(), 0)
    self.assertEqual(line.y1(), 0)
    self.assertEqual(line.x2(), 10)
    self.assertEqual(line.y2(), 20)

  # Add more test cases for other conversions...


if __name__ == '__main__':
  unittest.main()
