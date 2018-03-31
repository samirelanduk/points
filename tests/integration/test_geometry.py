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




        v1 = points.Vector(1, -9, 5)
        v2 = points.Vector(14, 1.1, -9.01)
        v3 = points.Vector(108, 12, 0.75)
