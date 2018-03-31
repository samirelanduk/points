from unittest import TestCase
import points

class VectorTests(TestCase):

    def test_single_vectors(self):
        # Vector values
        vector = points.Vector(15, 23, 17)
        self.assertEqual(vector.values(), (15, 23, 17))
        for value in vector:
            self.assertIn(value, vector)
        self.assertEqual(vector[1], 23)
        vector[1] = 8
        self.assertEqual(vector.values(), (15, 8, 17))
        vector.append(9)
        self.assertEqual(vector.values(), (15, 8, 17, 9))
        vector.insert(2, 7)
        self.assertEqual(vector.values(), (15, 8, 7, 17, 9))
        self.assertEqual(vector.pop(2), 7)
        self.assertEqual(vector.values(), (15, 8, 17, 9))
        vector.remove(9)
        self.assertEqual(vector.values(), (15, 8, 17))

        # Vector properties
        self.assertEqual(vector.length(), 3)
        self.assertAlmostEqual(vector.magnitude(), 24.041, delta=0.005)
        components = vector.components()
        self.assertEqual(len(components), 3)
        self.assertEqual(components[0].values(), (15, 0, 0))
        self.assertEqual(components[1].values(), (0, 8, 0))
        self.assertEqual(components[2].values(), (0, 0, 17))

        # Vector span - one dimensional
        d1 = points.Vector(15)
        span = d1.span()
        self.assertIn(d1, span)
        self.assertIn(points.Vector(4), span)
        self.assertIn(points.Vector(-3.5), span)
        self.assertIn(points.Vector(0), span)
        self.assertNotIn(points.Vector(15, 0), span)
        self.assertNotIn(points.Vector(4), points.Vector(0).span())
        self.assertIn(points.Vector(0), points.Vector(0).span())

        # Vector span - two dimensional
        d2 = points.Vector(15, 8)
        span = d2.span()
        self.assertIn(d2, span)
        self.assertIn(points.Vector(7.5, 4), span)
        self.assertIn(points.Vector(30, 16), span)
        self.assertIn(points.Vector(0, 0), span)
        self.assertNotIn(points.Vector(30, 16.000001), span)
        self.assertNotIn(points.Vector(30), span)
        self.assertNotIn(points.Vector(30, 16, 0), span)
        self.assertNotIn(points.Vector(4, 5), points.Vector(0, 0).span())

        # Vector span - three dimensional
        d3 = points.Vector(15, 8, 17)
        span = d3.span()
        self.assertIn(d3, span)
        self.assertIn(points.Vector(30, 16, 34), span)
        self.assertIn(points.Vector(7.5, 4, 8.5), span)
        self.assertIn(points.Vector(-7.5, -4, -8.5), span)
        self.assertNotIn(points.Vector(30, 16), span)
        self.assertNotIn(points.Vector(30, 16, 34.01), span)


    def test_vector_interactions(self):
        v1 = points.Vector(5, 23, 17)
        v2 = points.Vector([14, -4, 9])

        # Vector arithmetic
        v = v1 + v2
        self.assertEqual(v.values(), (19, 19, 26))
        v = v1 - v2
        self.assertEqual(v.values(), (-9, 27, 8))
        v = v1 * 10
        self.assertEqual(v.values(), (50, 230, 170))
        v = v1.dot(v2)
        self.assertEqual(v, 131)
        v = v1.cross(v2)
        self.assertEqual(v.values(), (275, 193, -342))

        # Vector geometry
        v1, v2 = points.Vector(2, 5, -1), points.Vector(1, -3, -4)
        self.assertTrue(v1.distance_to(v2), 74)
        self.assertAlmostEqual(v1.angle_with(v2), 1.898, delta=0.005)

        # Vector span - one dimension
        v1, v2 = points.Vector(4), points.Vector(-3)
        self.assertFalse(v1.linearly_independent_of(v2))
        span = v1.span_with(v2)
        self.assertEqual(span.dimension(), 1)
        self.assertIn(v1, span)
        self.assertIn(v2, span)
        self.assertIn(points.Vector(0), span)

        # Vector span - two dimensions
        v1, v2 = points.Vector(5, 23), points.Vector(14, -4)
        self.assertTrue(v1.linearly_independent_of(v2))
        span = v1.span_with(v2)
        self.assertIn(v1, span)
        self.assertIn(v2, span)
        self.assertIn(points.Vector(1, 2), span)
        v3 = points.Vector(10, 46)
        self.assertFalse(v3.linearly_independent_of(v1))
        span = v3.span_with(v1)
        self.assertNotIn(v2, span)
        span = v1.span_with(v2, v3)
        self.assertIn(points.Vector(-23, -69), span)

        # Vector span - three dimensions
        v1, v2 = points.Vector(5, 23, 17), points.Vector(14, -4, 9)
        span = v1.span_with(v2)
        self.assertIn(v1, span)
        self.assertIn(v2, span)
        self.assertNotIn(points.Vector(5, 23, 17.1), span)
        self.assertIn(points.Vector(10 - 42, 46 + 12, 34 - 27), span)
        self.assertNotIn(points.Vector(1, 2, 3), span)
        self.assertNotIn(points.Vector(14, -4), span)
        self.assertNotIn(points.Vector(14, -4, 0), span)
