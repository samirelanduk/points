from unittest import TestCase
import points

class VectorTests(TestCase):

    def test_vectors(self):
        v1 = points.Vector(5, 23, 17)
        v2 = points.Vector([14, -4, 9])

        self.assertIn(23, v1)
        self.assertNotIn(23, v2)
        self.assertEqual(v1[1], 23)

        self.assertEqual(v1.values(), (5, 23, 17))
        v1.add(9)
        self.assertEqual(v1.values(), (5, 23, 17, 9))
        v1.remove(9)
        self.assertEqual(v1.values(), (5, 23, 17))

        self.assertAlmostEqual(v1.magnitude(), 29.034, delta=0.005)
        self.assertAlmostEqual(v1.angle_with(v2), 1.304, delta=0.005)

        v = v1 + v2
        self.assertEqual(v.values(), (19, 19, 26))
        v = v1 - v2
        self.assertEqual(v.values(), (-9, 27, 8))
        self.assertAlmostEqual(v1.distance_to(v2), 29.563, delta=0.005)
        self.assertAlmostEqual(v2.distance_to(v1), 29.563, delta=0.005)
        v = v1 * 10
        self.assertEqual(v.values(), (50, 230, 170))
        v = v1.dot(v2)
        self.assertEqual(v, 131)
        v = v1.cross(v2)
        self.assertEqual(v.values(), (275, 193, -342))
