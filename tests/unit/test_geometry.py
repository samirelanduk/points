from unittest import TestCase
from math import pi
from points.geometry import degree_angle

class AngleDecoratorTests(TestCase):

    def test_decorator_can_convert_to_degrees(self):
        def angle():
            return pi
        angle = degree_angle(angle)
        self.assertEqual(angle(), pi)
        self.assertEqual(angle(degrees=False), pi)
        self.assertEqual(angle(degrees=True), 180)
