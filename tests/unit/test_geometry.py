from unittest import TestCase
from unittest.mock import Mock, patch
from points.geometry import *
from points.vectors import Vector

class GeometryTests(TestCase):

    def setUp(self):
        self.v1, self.v2, self.v3 = Mock(Vector), Mock(Vector), Mock(Vector)
        self.v1._values, self.v2._values, self.v3._values = [1, 2, 3], [4, 5, 6], [7, 8, 9]



class TranslationTests(GeometryTests):

    def test_can_translate(self):
        translate_vectors((10, -20, 5), self.v1, self.v2)
        self.assertEqual(self.v1._values, [11, -18, 8])
        self.assertEqual(self.v2._values, [14, -15, 11])


    def test_translation_needs_vectors(self):
        with self.assertRaises(TypeError):
            translate_vectors((10, -20, 5), self.v1, self.v2, "vector")


    def test_translation_needs_correct_dimension(self):
        with self.assertRaises(ValueError):
            translate_vectors((10, -20), self.v1, self.v2)
        self.v3._values = [7, 8]
        with self.assertRaises(ValueError):
            translate_vectors((10, -20, 5), self.v1, self.v2, self.v3)


'''
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
'''
