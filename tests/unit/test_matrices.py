from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock
from points.matrices import Matrix
from points.vectors import Vector

class MatrixTest(TestCase):

    def setUp(self):
        self.vector1 = Mock(Vector)
        self.vector2 = Mock(Vector)
        self.vector1.values.return_value = (3, 4)


class MatrixCreationTests(MatrixTest):

    def test_can_make_matrix(self):
        matrix = Matrix([1, 2], [3, 4])
        self.assertEqual(matrix._rows, [[1, 2], [3, 4]])


    def test_can_make_matrix_with_tuple(self):
        matrix = Matrix([1, 2], (3, 4))
        self.assertEqual(matrix._rows, [[1, 2], [3, 4]])


    def test_matrix_rows_must_be_iterable(self):
        with self.assertRaises(TypeError) as e:
            Matrix([1, 2], (3, 4), 789)
        self.assertIn("789 is not iterable", str(e.exception))


    def test_rows_must_be_equal_length(self):
        with self.assertRaises(ValueError):
            Matrix([1, 2], (3, 4), [3])
        with self.assertRaises(ValueError):
            Matrix([1, 2], (3, 4, 5))


    def test_can_make_matrix_with_columns(self):
        matrix = Matrix([1, 2], (0.1, 0.2), [3, 4], columns=True)
        self.assertEqual(matrix._rows, [[1, 0.1, 3], [2, 0.2, 4]])



class IdentityMatrixTests(TestCase):

    def test_can_get_identity_matrix(self):
        i = Matrix.identity(1)
        self.assertEqual(i._rows, [[1]])
        i = Matrix.identity(2)
        self.assertEqual(i._rows, [[1, 0], [0, 1]])
        i = Matrix.identity(3)
        self.assertEqual(i._rows, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])


    def test_dimensions_must_be_int(self):
        with self.assertRaises(TypeError):
            Matrix.identity(1.4)



class MatrixReprTests(TestCase):

    @patch("points.matrices.Matrix.size")
    def test_matrix_repr(self, mock_size):
        mock_size.return_value = (12, 43)
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertEqual(repr(matrix), "<12×43 Matrix>")



class MatrixStrTests(TestCase):

    def test_matrix_str_simple(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertEqual(str(matrix), "1 2\n3 4\n5 6")


    def test_matrix_str_different_widths(self):
        matrix = Matrix([1, 2, 3.5], [4.002, 5, 6])
        self.assertEqual(str(matrix), "    1     2   3.5\n4.002     5     6")



class MatrixContainerTests(TestCase):

    def test_items_in_matrix(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertIn(4, matrix)
        self.assertNotIn(8, matrix)



class MatrixEqualityTests(TestCase):

    def test_matrices_equal(self):
        self.assertEqual(
         Matrix([1, 2], [3, 4]), Matrix([1, 2], [3, 4])
        )


    def test_matrices_not_equal(self):
        self.assertNotEqual(
         Matrix([1, 2], [3, 4]), Matrix([1, 9], [3, 4])
        )
        self.assertNotEqual(
         Matrix([1, 2], [3, 4]), Matrix([1, 2, 9], [3, 4, 9])
        )
        self.assertNotEqual(
         Matrix([1, 2, 9], [3, 4, 9]), Matrix([1, 2], [3, 4])
        )
        self.assertNotEqual(
         Matrix([1, 2, 9], [3, 4, 9]), "other"
        )



class MatrixAdditionTests(TestCase):

    def setUp(self):
        self.matrix2 = Mock(Matrix)
        self.matrix2._rows = [[10, 20], [30, 40], [50, 60]]
        self.patch1 = patch("points.matrices.Matrix.size")
        self.mock_size = self.patch1.start()
        self.mock_size.return_value = self.matrix2.size.return_value = (3, 2)


    def tearDown(self):
        self.patch1.stop()


    def test_can_only_add_matrices(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        with self.assertRaises(TypeError):
            matrix + [1, 2, 3]


    def test_matrix_addition_needs_equal_size(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.matrix2.size.return_value = (4, 3)
        with self.assertRaises(ValueError):
            matrix + self.matrix2


    def test_can_add_matrices(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        matrix3 = matrix + self.matrix2
        self.assertEqual(matrix3._rows, [[11, 22], [33, 44], [55, 66]])



class MatrixSubtractionTests(TestCase):

    def setUp(self):
        self.matrix2 = Mock(Matrix)
        self.matrix2._rows = [[10, 20], [30, 40], [50, 60]]
        self.patch1 = patch("points.matrices.Matrix.size")
        self.mock_size = self.patch1.start()
        self.mock_size.return_value = self.matrix2.size.return_value = (3, 2)


    def tearDown(self):
        self.patch1.stop()


    def test_can_only_subtract_matrices(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        with self.assertRaises(TypeError):
            matrix - [1, 2, 3]


    def test_matrix_subtraction_needs_equal_size(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.matrix2.size.return_value = (4, 3)
        with self.assertRaises(ValueError):
            matrix - self.matrix2


    def test_can_subtract_matrices(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        matrix3 = matrix - self.matrix2
        self.assertEqual(matrix3._rows, [[-9, -18], [-27, -36], [-45, -54]])



class MatrixScalarMultiplicationTests(TestCase):

    def test_can_multiply_matrix_by_number(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        matrix2 = matrix * 2
        self.assertEqual(matrix2._rows, [[2, 4], [6, 8], [10, 12]])


    def test_can_multiply_number_by_matrix(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        matrix2 = 2 * matrix
        self.assertEqual(matrix2._rows, [[2, 4], [6, 8], [10, 12]])


    def test_matrix_multiplication_requires_numbers(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        with self.assertRaises(TypeError):
            matrix * [1, 2, 3]
        with self.assertRaises(TypeError):
            [1, 2, 3] * matrix



class MatrixWidthTests(TestCase):

    def test_matrix_width(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertEqual(matrix.width(), 2)



class MatrixHeightTests(TestCase):

    def test_matrix_height(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertEqual(matrix.height(), 3)



class MatrixSizeTests(TestCase):

    @patch("points.matrices.Matrix.width")
    @patch("points.matrices.Matrix.height")
    def test_matrix_size(self, mock_height, mock_width):
        mock_width.return_value = 50
        mock_height.return_value = 35
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertEqual(matrix.size(), (35, 50))
        mock_width.assert_called_with()
        mock_height.assert_called_with()



class MatrixSquareTests(TestCase):

    @patch("points.matrices.Matrix.width")
    @patch("points.matrices.Matrix.height")
    def test_square_matrices(self, mock_height, mock_width):
        mock_height.return_value = 4
        mock_width.return_value = 4
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertTrue(matrix.is_square())
        mock_width.return_value = 3
        self.assertFalse(matrix.is_square())




class MatrixMatMultiplicationTests(TestCase):

    def setUp(self):
        self.matrix2 = Mock(Matrix)
        self.matrix2._rows = [[10, 20, 30], [40, 50, 60]]
        self.patch1 = patch("points.matrices.Matrix.size")
        self.mock_size = self.patch1.start()
        self.mock_size.return_value = (3, 2)
        self.matrix2.size.return_value = (2, 3)
        self.matrix2.columns.return_value = ((10, 40), (20, 50), (30, 60))


    def tearDown(self):
        self.patch1.stop()

    def test_can_only_matmul_matrices(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        with self.assertRaises(TypeError):
            matrix @ 100


    def test_matrix_dimensions_must_match(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.matrix2.size.return_value = (3, 3)
        with self.assertRaises(ValueError):
            matrix3 = matrix @ self.matrix2


    def test_can_mat_mul_matrices(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        matrix3 = matrix @ self.matrix2
        self.assertEqual(
         matrix3._rows, [[90, 120, 150], [190, 260, 330], [290, 400, 510]]
        )


    def test_can_mat_mul_vectors(self):
        matrix = Matrix([1, 2], [3, 4])
        vector = Mock(Vector)
        vector.values.return_value = [5, 6]
        vector.__len__, vector.__len__.return_value = MagicMock(), 2
        output = matrix @ vector
        self.assertIsInstance(output, Vector)
        self.assertEqual(output._values, [17, 39])


    def test_vector_must_be_right_size_for_matmul(self):
        matrix = Matrix([1, 2], [3, 4])
        vector = Mock(Vector)
        vector.values.return_value = [5, 6]
        vector.__len__, vector.__len__.return_value = MagicMock(), 3
        with self.assertRaises(ValueError):
            output = matrix @ vector



class MatrixRowsTests(TestCase):

    def test_can_get_rows(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertEqual(matrix.rows(), ((1, 2), (3, 4), (5, 6)))



class MatrixColumnsTests(TestCase):

    def test_can_get_columns(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertEqual(matrix.columns(), ((1, 3, 5), (2, 4, 6)))



class MatrixTranspositionTests(TestCase):

    def test_can_transpose_matrix(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        matrix_t = matrix.transposed()
        self.assertEqual(matrix_t._rows, [[1, 3, 5], [2, 4, 6]])



class MatrixMinorTests(TestCase):

    def setUp(self):
        self.patch1 = patch("points.matrices.Matrix.is_square")
        self.patch2 = patch("points.matrices.Matrix.width")
        self.mock_square = self.patch1.start()
        self.mock_width = self.patch2.start()
        self.mock_square.return_value = True


    def tearDown(self):
        self.patch1.stop()
        self.patch2.stop()


    def test_matrix_must_be_square(self):
        matrix = Matrix([1, 2], [3, 4])
        self.mock_square.return_value = False
        with self.assertRaises(ValueError):
            matrix.minor(0, 0)


    def test_2d_matrix_minors(self):
        self.mock_width.return_value = 2
        matrix = Matrix([1, 2], [3, 4])
        self.assertEqual(matrix.minor(0, 0), 4)
        self.assertEqual(matrix.minor(0, 1), 3)
        self.assertEqual(matrix.minor(1, 0), 2)
        self.assertEqual(matrix.minor(1, 1), 1)


    def test_3d_matrix_minors(self):
        self.mock_width.return_value = 3
        matrix = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        matrix_patch = patch("points.matrices.Matrix")
        mock_matrix = matrix_patch.start()
        try:
            matrices2 = [Mock(), Mock(), Mock(), Mock(), Mock(), Mock()]
            mock_matrix.side_effect = matrices2
            for index, mat in enumerate(matrices2, start=1):
                mat.determinant.return_value = index * 100
            self.assertEqual(matrix.minor(0, 0), 100)
            self.assertEqual(matrix.minor(0, 1), 200)
            self.assertEqual(matrix.minor(1, 1), 300)
            self.assertEqual(matrix.minor(1, 2), 400)
            self.assertEqual(matrix.minor(2, 0), 500)
            self.assertEqual(matrix.minor(2, 2), 600)
            mock_matrix.assert_any_call([5, 6], [8, 9])
            mock_matrix.assert_any_call([4, 6], [7, 9])
            mock_matrix.assert_any_call([1, 3], [7, 9])
            mock_matrix.assert_any_call([1, 2], [7, 8])
            mock_matrix.assert_any_call([2, 3], [5, 6])
            mock_matrix.assert_any_call([1, 2], [4, 5])
            for mat in matrices2:
                mat.determinant.assert_called_with()
        finally:
            matrix_patch.stop()



class MatrixCofactorTests(TestCase):

    def setUp(self):
        self.patch1 = patch("points.matrices.Matrix.minor")
        self.mock_minor = self.patch1.start()
        self.mock_minor.return_value = 5


    def tearDown(self):
        self.patch1.stop()


    def test_can_return_unaltered_minors(self):
        matrix = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        self.assertEqual(matrix.cofactor(0, 0), 5)
        self.assertEqual(matrix.cofactor(0, 2), 5)
        self.assertEqual(matrix.cofactor(1, 1), 5)
        self.assertEqual(matrix.cofactor(2, 0), 5)
        self.assertEqual(matrix.cofactor(2, 0), 5)


    def test_can_return_negative_minors(self):
        matrix = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        self.assertEqual(matrix.cofactor(0, 1), -5)
        self.assertEqual(matrix.cofactor(1, 0), -5)
        self.assertEqual(matrix.cofactor(1, 2), -5)
        self.assertEqual(matrix.cofactor(2, 1), -5)



class MatrixMinorsTests(TestCase):

    @patch("points.matrices.Matrix.minor")
    def test_can_get_matrix_minors(self, mock_minor):
        mock_minor.side_effect = [4, 8, 15, 16, 23, 42, 19, 20, 21]
        matrix = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        minors = matrix.minors()
        self.assertEqual(minors._rows, [[4, 8, 15], [16, 23, 42], [19, 20, 21]])
        mock_minor.assert_any_call(0, 0)
        mock_minor.assert_any_call(0, 1)
        mock_minor.assert_any_call(0, 2)
        mock_minor.assert_any_call(1, 0)
        mock_minor.assert_any_call(1, 1)
        mock_minor.assert_any_call(1, 2)
        mock_minor.assert_any_call(2, 0)
        mock_minor.assert_any_call(2, 1)
        mock_minor.assert_any_call(2, 2)



class MatrixCofactorsTests(TestCase):

    @patch("points.matrices.Matrix.cofactor")
    def test_can_get_matrix_minors(self, mock_cof):
        mock_cof.side_effect = [4, 8, 15, 16, 23, 42, 19, 20, 21]
        matrix = Matrix([1, 2, 3], [4, 5, 6], [7, 8, 9])
        minors = matrix.cofactors()
        self.assertEqual(minors._rows, [[4, 8, 15], [16, 23, 42], [19, 20, 21]])
        mock_cof.assert_any_call(0, 0)
        mock_cof.assert_any_call(0, 1)
        mock_cof.assert_any_call(0, 2)
        mock_cof.assert_any_call(1, 0)
        mock_cof.assert_any_call(1, 1)
        mock_cof.assert_any_call(1, 2)
        mock_cof.assert_any_call(2, 0)
        mock_cof.assert_any_call(2, 1)
        mock_cof.assert_any_call(2, 2)



class MatrixDeterminantTests(TestCase):

    def setUp(self):
        self.patch1 = patch("points.matrices.Matrix.is_square")
        self.patch2 = patch("points.matrices.Matrix.width")
        self.mock_square = self.patch1.start()
        self.mock_width = self.patch2.start()
        self.mock_square.return_value = True


    def tearDown(self):
        self.patch1.stop()
        self.patch2.stop()


    def test_matrix_must_be_square(self):
        matrix = Matrix([1, 2], [3, 4])
        self.mock_square.return_value = False
        with self.assertRaises(ValueError):
            matrix.determinant()


    def test_2d_matrix(self):
        self.mock_width.return_value = 2
        matrix = Matrix([1, 2], [3, 4])
        self.assertEqual(matrix.determinant(), -2)


    @patch("points.matrices.Matrix.cofactor")
    def test_3d_matrix(self, mock_cof):
        self.mock_width.return_value = 3
        mock_cof.side_effect = [16, -23, 42]
        matrix = Matrix([4, -3, 1], [2, -1, 2], [1, 5, 7])
        self.assertEqual(matrix.determinant(), 175)
        mock_cof.assert_any_call(0, 0)
        mock_cof.assert_any_call(0, 1)
        mock_cof.assert_any_call(0, 2)



class MatrixAdjointTests(TestCase):

    @patch("points.matrices.Matrix.cofactors")
    def test_can_get_matrix_adjoint(self, mock_cof):
        cofactors = Mock()
        mock_cof.return_value = cofactors
        cofactors.transposed.return_value = "TRANSPOSED"
        matrix = Matrix([4, -3, 1], [2, -1, 2], [1, 5, 7])
        self.assertEqual(matrix.adjoint(), "TRANSPOSED")
        mock_cof.assert_called_with()
        cofactors.transposed.assert_called_with()



class MatrixInversionTests(TestCase):

    @patch("points.matrices.Matrix.adjoint")
    @patch("points.matrices.Matrix.determinant")
    def test_can_get_matrix_inverse(self, mock_det, mock_adjoint):
        adjoint = Mock()
        mock_adjoint.return_value = 3
        mock_det.return_value = 0.25
        matrix = Matrix([4, -3, 1], [2, -1, 2], [1, 5, 7])
        self.assertEqual(matrix.inverse(), 12)
        mock_adjoint.assert_called_with()
        mock_det.assert_called_with()


    @patch("points.matrices.Matrix.determinant")
    def test_no_inverse_if_zero_det(self, mock_det):
        mock_det.return_value = 0
        matrix = Matrix([4, -3, 1], [2, -1, 2], [1, 5, 7])
        with self.assertRaises(ValueError):
            matrix.inverse()



class MatrixColumnSpaceTests(TestCase):

    @patch("points.matrices.Matrix.columns")
    @patch("points.matrices.Vector")
    @patch("points.matrices.VectorSpan")
    def test_can_get_matrix_column_space(self, mock_span, mock_vec, mock_col):
        mock_col.return_value = ((3, 2), (5, 3), (9, 5))
        mock_vec.side_effect = ("v1", "v2", "v3")
        mock_span.return_value = "SPAN"
        m = Matrix([3, 5, 9], [2, 3, 5])
        space = m.column_space()
        mock_col.assert_called_with()
        mock_vec.assert_any_call((3, 2))
        mock_vec.assert_any_call((5, 3))
        mock_vec.assert_any_call((9, 5))
        mock_span.assert_called_with("v1", "v2", "v3")
        self.assertEqual(space, "SPAN")



class MatrixRankTests(TestCase):

    @patch("points.matrices.Matrix.column_space")
    def test_can_get_matrix_rank(self, mock_space):
        space = Mock()
        space.rank.return_value = 400
        mock_space.return_value = space
        m = Matrix([3, 5, 9], [2, 3, 5])
        self.assertEqual(m.rank(), 400)
        mock_space.assert_called_with()
        space.rank.assert_called_with()



class MatrixFullRankTests(TestCase):

    @patch("points.matrices.Matrix.rank")
    def test_can_get_matrix_rank(self, mock_rank):
        mock_rank.return_value = 400
        m = Matrix([3, 5, 9], [2, 3, 5])
        self.assertFalse(m.is_full_rank())
        mock_rank.assert_called_with()
        mock_rank.return_value = 2
        self.assertTrue(m.is_full_rank())


'''
class MatrixNullSpaceTests(TestCase):

    @patch("points.matrices.Matrix.is_full_rank")
    @patch("points.matrices.VectorSpan")
    @patch("points.matrices.Vector")
    def test_null_space_is_zero_when_full_rank(self, mock_vec, mock_span, mock_full):
        mock_full.return_value = True
        mock_vec.return_value = "VECTOR"
        mock_span.return_value = "SPAN"
        m = Matrix([1, 2], [3, 4])
        space = m.null_space()
        mock_full.assert_called_with()
        mock_vec.assert_called_with(0, 0)
        mock_span.assert_called_with("VECTOR")
        self.assertEqual(space, "SPAN")
        m = Matrix([1, 2, 12], [3, 4, 9], [1, 6, 4], [3, 5, 6], [0, 0, 1])
        m.null_space()
        mock_vec.assert_called_with(0, 0, 0, 0, 0)'''



class MatrixGaussianEliminationTests(TestCase):

    def test_can_gaussian_eliminate_square_matrices(self):
        m = Matrix([3, 5, 9], [2, 3, 5])
        m.gauss()
        self.assertEqual(m._rows, [[3, 5, 9], [0, -1 / 3, -1]])
        m = Matrix([2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3])
        m.gauss()
        self.assertEqual(m._rows, [
         [-3, -1, 2, -11], [0, 5 / 3, 2 / 3, 13 / 3], [0, 0, 1 / 5, -1 / 5]
        ])
        m = Matrix([1, -1, -1, 1], [3, 2, 12, 1], [2, -1, 1, 1])
        m.gauss()
        self.assertEqual(m._rows, [
         [3, 2, 12, 1], [0, -7 / 3, -7, 1 / 3], [0, 0, 0, 3 / 7]
        ])


    def test_can_gaussian_eliminate_vertical_matrices(self):
        m = Matrix([3, 5, 9], [2, 3, 5], [4, 6, 8], [3, 6, 7], [1, 2, 3])
        m.gauss()
        self.assertEqual(m._rows, [
         [4, 6, 8], [0, 3 / 2, 1], [0, 0, 8 / 3], [0, 0, 0], [0, 0, 0]
        ])


    def test_can_gaussian_eliminate_horizontal_matrices(self):
        m = Matrix([3, 5, 9, 2, 3, 5], [4, 6, 8, 3, 6, 7])
        m.gauss()
        self.assertEqual(m._rows, [
         [4, 6, 8, 3, 6, 7], [0, 0.5, 3, -0.25, -1.5, -0.25]
        ])



class MatrixRowEchelonFormCheckTests(TestCase):

    def test_not_in_row_echelon_if_zeroes_above_non_zeroes(self):
        self.assertFalse(Matrix([1, 0], [0, 0], [0, 1]).is_row_echelon())
        self.assertFalse(Matrix([0, 0], [1, 0], [0, 1]).is_row_echelon())


    def test_not_in_row_echelon_if_leading_coefficients_wrong(self):
        self.assertFalse(Matrix([1, 0], [2, 0]).is_row_echelon())
        self.assertFalse(Matrix([0, 1], [2, 0]).is_row_echelon())


    def test_row_echelon_returns_true(self):
        self.assertTrue(Matrix([1, 0], [0, 2]).is_row_echelon())
        self.assertTrue(Matrix([1, 0], [0, 2], [0, 0]).is_row_echelon())



class MatrixReducedRowEchelonFormCheckTests(TestCase):

    @patch("points.matrices.Matrix.is_row_echelon")
    def test_check_row_echelon_first(self, mock_check):
        mock_check.return_value = False
        self.assertFalse(
         Matrix([1, 0], [0, 1], [0, 0]).is_reduced_row_echelon()
        )
        mock_check.assert_called_with()


    @patch("points.matrices.Matrix.is_row_echelon")
    def test_reduced_row_echelon_checks(self, mock_check):
        mock_check.return_value = True
        self.assertTrue(Matrix([1, 0], [0, 1], [0, 0]).is_reduced_row_echelon())
        mock_check.assert_called_with()
        self.assertFalse(
         Matrix([1, 0], [0, 2], [0, 0]).is_reduced_row_echelon()
        )
        self.assertFalse(
         Matrix([1, 0, 0], [0, 1, 1], [0, 0, 1]).is_reduced_row_echelon()
        )
        self.assertTrue(
         Matrix([1, 0, 0], [0, 0, 1], [0, 0, 0]).is_reduced_row_echelon()
        )
