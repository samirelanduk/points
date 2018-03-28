from unittest import TestCase
import points

class MatrixTests(TestCase):

    def test_single_matrices(self):
        # Basic creation
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
        self.assertTrue(matrix.is_square())
        self.assertEqual(
         matrix.transposed().rows(), ((1, 4, 7), (2, 5, 8), (3, 6, 9))
        )

        # Creation with columns
        matrix = points.Matrix([1, 2, 3], (4, 5, 6), [7, 8, 9], columns=True)
        self.assertEqual(matrix.rows()[0], (1, 4, 7))
        self.assertEqual(matrix.rows()[1], (2, 5, 8))
        self.assertEqual(matrix.rows()[2], (3, 6, 9))

        # Creating rectangular matrices
        matrix = points.Matrix([1, 2, 3, 4], [5, 6, 7, 8])
        self.assertEqual(matrix.width(), 4)
        self.assertEqual(matrix.height(), 2)
        self.assertEqual(matrix.size(), (2, 4))
        self.assertFalse(matrix.is_square())

        # 2D Matrix minors, cofactors, and determinant
        matrix2d = points.Matrix([1, 9], [2, 4])
        self.assertEqual(matrix2d.minor(0, 0), 4)
        self.assertEqual(matrix2d.minor(0, 1), 2)
        self.assertEqual(matrix2d.minor(1, 0), 9)
        self.assertEqual(matrix2d.minor(1, 1), 1)
        self.assertEqual(matrix2d.cofactor(0, 0), 4)
        self.assertEqual(matrix2d.cofactor(0, 1), -2)
        self.assertEqual(matrix2d.cofactor(1, 0), -9)
        self.assertEqual(matrix2d.cofactor(1, 1), 1)
        self.assertEqual(matrix2d.minors().rows(), ((4, 2), (9, 1)))
        self.assertEqual(matrix2d.cofactors().rows(), ((4, -2), (-9, 1)))
        self.assertEqual(matrix2d.determinant(), -14)

        # 3D Matrix minors, cofactors, and determinant and inversion
        matrix3d = points.Matrix([9, 2, 3], [4, 15, 6], [0, 4, 11])
        self.assertEqual(matrix3d.minor(0, 0), 141)
        self.assertEqual(matrix3d.minor(0, 1), 44)
        self.assertEqual(matrix3d.minor(0, 2), 16)
        self.assertEqual(matrix3d.minor(1, 0), 10)
        self.assertEqual(matrix3d.minor(1, 1), 99)
        self.assertEqual(matrix3d.minor(1, 2), 36)
        self.assertEqual(matrix3d.minor(2, 0), -33)
        self.assertEqual(matrix3d.minor(2, 1), 42)
        self.assertEqual(matrix3d.minor(2, 2), 127)
        self.assertEqual(matrix3d.cofactor(0, 0), 141)
        self.assertEqual(matrix3d.cofactor(0, 1), -44)
        self.assertEqual(matrix3d.cofactor(0, 2), 16)
        self.assertEqual(matrix3d.cofactor(1, 0), -10)
        self.assertEqual(matrix3d.cofactor(1, 1), 99)
        self.assertEqual(matrix3d.cofactor(1, 2), -36)
        self.assertEqual(matrix3d.cofactor(2, 0), -33)
        self.assertEqual(matrix3d.cofactor(2, 1), -42)
        self.assertEqual(matrix3d.cofactor(2, 2), 127)
        self.assertEqual(
         matrix3d.minors().rows(),
         ((141, 44, 16), (10, 99, 36), (-33, 42, 127))
        )
        self.assertEqual(
         matrix3d.cofactors().rows(),
         ((141, -44, 16), (-10, 99, -36), (-33, -42, 127))
        )
        self.assertEqual(matrix3d.determinant(), 1229)
        self.assertEqual(
         matrix3d.adjoint().rows(),
         ((141, -10, -33), (-44, 99, -42), (16, -36, 127))
        )
        matrix3d = points.Matrix([7, 2, 1], [0, 3, -1], [-3, 4, -2])
        self.assertEqual(
         matrix3d.inverse().rows(),
         ((-2, 8, -5), (3, -11, 7), (9, -34, 21))
        )
        self.assertEqual(
         matrix3d.inverse() @ matrix3d, points.Matrix.identity(3)
        )

        # 4D Matrix determinant
        matrix4d = points.Matrix(
         [1, 3, 5, 9], [1, 3, 1, 7], [4, 3, 9, 7], [5, 2, 0, 9]
        )
        self.assertEqual(matrix4d.determinant(), -376)


    def test_multiple_matrices(self):
        # Matrix equality
        self.assertEqual(
         points.Matrix([1, 2], [3, 4]), points.Matrix([1, 2], [3, 4])
        )
        self.assertNotEqual(
         points.Matrix([1, 2], [3, 4]), points.Matrix([1, 2], [3, 1])
        )

        # Matrix arithmetic
        matrix = points.Matrix([1, 2, 3], (4, 5, 6), [7, 8, 9])
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



class MatrixVectorTests(TestCase):

    def test_matrix_and_vectors(self):
        # Matrix from vector
        vector = points.Vector(1, 2, 3)
        matrix = points.Matrix(vector, (4, 5, 6), (7, 8, 9))
        self.assertEqual(matrix.rows()[0], (1, 2, 3))
        self.assertEqual(matrix.rows()[1], (4, 5, 6))
        self.assertEqual(matrix.rows()[2], (7, 8, 9))

        # Matrix-vector multiplication
        v2 = matrix.transposed() @ vector
        self.assertEqual(v2.values(), (30, 36, 42))

        # Matrix column space
        matrix = points.Matrix([1, 8, 2], [0, 1, 1], [1, 9, 2])
        space = matrix.column_space()
        self.assertEqual(space.dimension(), 3)
        self.assertIn(points.Vector(1, 2, 3), space)
        self.assertIn(points.Vector(19, -2.05, 309), space)

        space = points.Matrix([1, 0, 2], [0, 1, 1], [0, 0, 0]).column_space()
        self.assertEqual(space.dimension(), 3)
        self.assertIn(points.Vector(1, 2, 0), space)
        self.assertNotIn(points.Vector(1, 2, 3), space)
