import math
from unittest import TestCase
import points

class GeometryTests(TestCase):

    def test_geometry(self):
        # Translation - 2D
        v1 = points.Vector(5, -1)
        v2 = points.Vector(19, 1)
        v3 = points.Vector(-112, 0.4)
        points.translate_vectors((12, -0.4), v1, v2, v3)
        self.assertEqual(v1.values(), (17, -1.4))
        self.assertEqual(v2.values(), (31, 0.6))
        self.assertEqual(v3.values(), (-100, 0))

        # Translation - 3D
        v4 = points.Vector(1, -9, 5)
        v5 = points.Vector(14, 1.1, -9.01)
        v6 = points.Vector(108, 12, 0.75)
        v7 = points.Vector(-9, 1, 0.2)
        points.translate_vectors((0.3, 0.4, -1000), v4, v5, v6, v7)
        self.assertEqual(v4.values(), (1.3, -8.6, -995))
        self.assertEqual(v5.values(), (14.3, 1.5, -1009.01))
        self.assertEqual(v6.values(), (108.3, 12.4, -999.25))
        self.assertEqual(v7.values(), (-8.7, 1.4, -999.8))

        # Rotation 2D
        points.rotate_2d_vectors(math.pi / 4, v1, v2, v3)
        self.assertAlmostEqual(v1.values()[0], 13.011, delta=0.005)
        self.assertAlmostEqual(v1.values()[1], 11.031, delta=0.005)
        self.assertAlmostEqual(v2.values()[0], 21.496, delta=0.005)
        self.assertAlmostEqual(v2.values()[1], 22.345, delta=0.005)
        self.assertAlmostEqual(v3.values()[0], -70.711, delta=0.005)
        self.assertAlmostEqual(v3.values()[1], -70.711, delta=0.005)
        v1 = points.Vector(5, -1)
        v2 = points.Vector(19, 1)
        v3 = points.Vector(-112, 0.4)
        points.translate_vectors((12, -0.4), v1, v2, v3)
        points.rotate_2d_vectors(45, v1, v2, v3, trim=1, degrees=True)
        self.assertEqual(v1.values(), (13.0, 11.0))
        self.assertEqual(v2.values(), (21.5, 22.3))
        self.assertEqual(v3.values(), (-70.7, -70.7))

        # Rotate 3D
        points.rotate_3d_vectors(45, 0, v4, v5, v6, v7, degrees=True, trim=2)
        self.assertEqual(v4.values(), (1.3, 697.49, -709.65))
        self.assertEqual(v5.values(), (14.3, 714.54, -712.42))
        self.assertEqual(v6.values(), (108.3, 715.34, -697.81))
        self.assertEqual(v7.values(), (-8.7, 707.96, -705.98))

        points.rotate_3d_vectors(-10, 1, v4, v5, v6, v7, degrees=True, trim=2)
        self.assertEqual(v4.values(), (124.51, 697.49, -698.64))
        self.assertEqual(v5.values(), (137.79, 714.54, -699.11))
        self.assertEqual(v6.values(), (227.83, 715.34, -668.40))
        self.assertEqual(v7.values(), (114.02, 707.96, -696.77))

        points.rotate_3d_vectors(181, 2, v4, v5, v6, v7, degrees=True, trim=2)
        self.assertEqual(v4.values(), (-112.32, -699.56, -698.64))
        self.assertEqual(v5.values(), (-125.30, -716.84, -699.11))
        self.assertEqual(v6.values(), (-215.31, -719.21, -668.40))
        self.assertEqual(v7.values(), (-101.65, -709.84, -696.77))
