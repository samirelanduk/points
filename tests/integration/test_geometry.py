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
