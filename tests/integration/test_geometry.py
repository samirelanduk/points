import math
from unittest import TestCase
import points

class GeometryTests(TestCase):

    def test_2d_transformations(self):
        # Translation
        v1 = points.Vector(5, -1)
        v2 = points.Vector(19, 1)
        v3 = points.Vector(-112, 0.4)
        points.translate_vectors((12, -0.4), v1, v2, v3)
        self.assertEqual(v1.values(), (17, -1.4))
        self.assertEqual(v2.values(), (31, 0.6))
        self.assertEqual(v3.values(), (-100, 0))

        # Rotation
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

        # Rotation about arbitrary point
        v4 = points.Vector(3.9, 6)
        v5 = points.Vector(4.1, 6)
        points.rotate_2d_vectors(
         90, v4, v5, degrees=True, point=points.Vector(4, 5), trim=6
        )
        self.assertEqual(v4.values(), (3, 4.9))
        self.assertEqual(v5.values(), (3, 5.1))


    def test_3d_transformations(self):
        # Translation
        v1 = points.Vector(1, -9, 5)
        v2 = points.Vector(14, 1.1, -9.01)
        v3 = points.Vector(108, 12, 0.75)
        v4 = points.Vector(-9, 1, 0.2)
        points.translate_vectors((0.3, 0.4, -1000), v1, v2, v3, v4)
        self.assertEqual(v1.values(), (1.3, -8.6, -995))
        self.assertEqual(v2.values(), (14.3, 1.5, -1009.01))
        self.assertEqual(v3.values(), (108.3, 12.4, -999.25))
        self.assertEqual(v4.values(), (-8.7, 1.4, -999.8))

        # Rotate
        points.rotate_3d_vectors(45, 0, v1, v2, v3, v4, degrees=True, trim=2)
        self.assertEqual(v1.values(), (1.3, 697.49, -709.65))
        self.assertEqual(v2.values(), (14.3, 714.54, -712.42))
        self.assertEqual(v3.values(), (108.3, 715.34, -697.81))
        self.assertEqual(v4.values(), (-8.7, 707.96, -705.98))

        points.rotate_3d_vectors(-10, 1, v1, v2, v3, v4, degrees=True, trim=2)
        self.assertEqual(v1.values(), (124.51, 697.49, -698.64))
        self.assertEqual(v2.values(), (137.79, 714.54, -699.11))
        self.assertEqual(v3.values(), (227.83, 715.34, -668.40))
        self.assertEqual(v4.values(), (114.02, 707.96, -696.77))

        points.rotate_3d_vectors(181, 2, v1, v2, v3, v4, degrees=True, trim=2)
        self.assertEqual(v1.values(), (-112.32, -699.56, -698.64))
        self.assertEqual(v2.values(), (-125.30, -716.84, -699.11))
        self.assertEqual(v3.values(), (-215.31, -719.21, -668.40))
        self.assertEqual(v4.values(), (-101.65, -709.84, -696.77))

        # Rotation around arbitrary point
        v5 = points.Vector(2, 2, 2)
        v6 = points.Vector(-1, -1, -1)
        points.rotate_3d_vectors(
         90, 0, v5, v6, degrees=True, trim=6, point=[1, 1, 1]
        )
        self.assertEqual(v5.values(), (2, 0, 2))
        self.assertEqual(v6.values(), (-1, 3, -1))

        # Aligning to planes
        v5 = points.Vector(0, 0, 1)
        v6 = points.Vector(0, 1, 1)
        v7 = points.Vector(0, -1, 1)
        v8 = points.Vector(1, 0, 1)
        v9 = points.Vector(-1, 0, 1)
        # Rotate around x-axis to xy plane
        points.align_vectors_to_plane(0, 1, v5, v6, v7, v8, v9, trim=2)
        self.assertEqual(v5.values(), (0, -1, 0))
        self.assertEqual(v6.values(), (0, -1, 1))
        self.assertEqual(v7.values(), (0, -1, -1))
        self.assertEqual(v8.values(), (1, -1, 0))
        self.assertEqual(v9.values(), (-1, -1, 0))
        # Rotate around z-axis to xz plane
        points.align_vectors_to_plane(2, 0, v5, v6, v7, v8, v9, trim=2)
        self.assertEqual(v5.values(), (1, 0, 0))
        self.assertEqual(v6.values(), (1, 0, 1))
        self.assertEqual(v7.values(), (1, 0, -1))
        self.assertEqual(v8.values(), (1, 1, 0))
        self.assertEqual(v9.values(), (1, -1, 0))
