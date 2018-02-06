from unittest import TestCase
from math import pi
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

        components = v1.components()
        self.assertEqual(len(components), 3)
        self.assertEqual(components[0].values(), (5, 0, 0))
        self.assertEqual(components[1].values(), (0, 23, 0))
        self.assertEqual(components[2].values(), (0, 0, 17))

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

        v2d = points.Vector(2, 2)
        v2d.rotate(pi)
        self.assertAlmostEqual(v2d.values()[0], -2, delta=0.005)
        self.assertAlmostEqual(v2d.values()[1], -2, delta=0.005)

        v3d = points.Vector(2, 3, 4)
        v3d.rotate(pi, "x")
        self.assertAlmostEqual(v3d.values()[0], 2, delta=0.005)
        self.assertAlmostEqual(v3d.values()[1], -3, delta=0.005)
        self.assertAlmostEqual(v3d.values()[2], -4, delta=0.005)



class MatrixTests(TestCase):

    def test_matrices(self):
        matrix = points.Matrix([1, 2, 3], (4, 5, 6), [7, 8, 9])
        self.assertEqual(matrix.size(), (3, 3))
        self.assertEqual(matrix.rows()[0], (1, 2, 3))
        self.assertEqual(matrix.rows()[1], (4, 5, 6))
        self.assertEqual(matrix.rows()[2], (7, 8, 9))
        self.assertEqual(matrix.columns()[0], (1, 4, 7))
        self.assertEqual(matrix.columns()[1], (2, 5, 8))
        self.assertEqual(matrix.columns()[2], (3, 6, 9))

        self.assertIn(7, matrix)
        self.assertNotIn(10, matrix)

        matrix2 = points.Matrix([11, 12, 31], (41, 15, 61), [17, 81, 19])
        self.assertEqual(
         (matrix + matrix2).rows(), ((12, 14, 34), (45, 20, 67), (24, 89, 28))
        )
        self.assertEqual(
         (matrix2 - matrix).rows(), ((10, 10, 28), (37, 10, 55), (10, 73, 10))
        )
        self.assertEqual(
         (matrix * 10).rows(), ((10, 20, 30), (40, 50, 60), (70, 80, 90))
        )
        self.assertEqual(
         (10 * matrix).rows(), ((10, 20, 30), (40, 50, 60), (70, 80, 90))
        )
        self.assertEqual(
         (matrix @ matrix2).rows(), ((144, 285, 210), (351, 609, 543), (558, 933, 876))
        )
        self.assertEqual(
         (matrix2 @ matrix).rows(), ((276, 330, 384), (528, 645, 762), (474, 591, 708))
        )

        self.assertEqual(
         matrix.transposed().rows(), ((1, 4, 7), (2, 5, 8), (3, 6, 9))
        )


    def test_matrices_with_vectors(self):

        v1 = points.Vector(1, 2, 3)
        v2 = points.Vector(4, 5, 6)
        v3 = points.Vector(7, 8, 9)
        matrix = points.Matrix(v1, v2, v3)
        self.assertEqual(matrix.rows()[0], (1, 4, 7))
        self.assertEqual(matrix.rows()[1], (2, 5, 8))
        self.assertEqual(matrix.rows()[2], (3, 6, 9))

        v4 = matrix @ v1
        self.assertEqual(v4.values(), (30, 36, 42))


    def test_matrices_complicated_properties(self):
        matrix2d = points.Matrix([1, 9], [2, 4])
        self.assertEqual(matrix2d.determinant(), -14)
        matrix3d = points.Matrix([9, 2, 3], [4, 15, 6], [0, 4, 11])
        self.assertEqual(matrix3d.determinant(), 1229)
        matrix4d = points.Matrix(
         [1, 3, 5, 9], [1, 3, 1, 7], [4, 3, 9, 7], [5, 2, 0, 9]
        )
        self.assertEqual(matrix4d.determinant(), -376)


    '''def test_matrix_inversion(self):
        matrix2d = points.Matrix([4, 7], [2, 6])
        inversion = matrix2d.inverse()
        self.assertEqual(inversion.rows(), ((0.6, -0.7), (-0.2, 0.4)))
        matrix3d = points.Matrix([7, 2, 1], [0, 3, -1], [-3, 4, -2])
        inversion = matrix3d.inverse()
        self.assertEqual(inversion.rows(), ((-2, 8, -1), (3, -11, 7), (9, -34, 21)))'''

