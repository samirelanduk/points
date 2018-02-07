from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock
from points.matrices import Matrix
from points.vectors import Vector

class MatrixCreationTests(TestCase):

    def test_can_make_matrix(self):
        matrix = Matrix([1, 2], [3, 4])
        self.assertEqual(matrix._rows, [[1, 2], [3, 4]])


    def test_can_make_matrix_with_tuple(self):
        matrix = Matrix([1, 2], (3, 4))
        self.assertEqual(matrix._rows, [[1, 2], [3, 4]])


    def test_can_make_matrix_with_vectors(self):
        v1, v2 = Mock(Vector), Mock(Vector)
        v1._values = [1, 3, 5]
        v1.__len__ = MagicMock()
        v1.__len__.return_value = 3
        v2._values = [2, 4, 6]
        matrix = Matrix(v1, v2)
        self.assertEqual(matrix._rows, [[1, 2], [3, 4], [5, 6]])


    def test_all_need_to_be_vectors_if_they_are_to_be_used(self):
        v1 = Mock(Vector)
        v1._values = [1, 3]
        v1.__len__ = MagicMock()
        v1.__len__.return_value = 2
        with self.assertRaises(TypeError):
            Matrix(v1, [2, 4])


    def test_cannot_make_matrix_from_none_iterables(self):
        with self.assertRaises(TypeError) as e:
            Matrix([1, 2], (3, 4), 789)
        self.assertIn("789 is not iterable", str(e.exception))


    def test_matrix_elements_must_be_numeric(self):
        with self.assertRaises(TypeError) as e:
            Matrix([1, 2], (3, "4"))
        Matrix([1, 2], (3, 4.5))


    def test_rows_must_be_equal_length(self):
        with self.assertRaises(ValueError):
            Matrix([1, 2], (3, 4), [3])
        with self.assertRaises(ValueError):
            Matrix([1, 2], (3, 4, 5))


    def test_matrix_cannot_be_empty(self):
        with self.assertRaises(ValueError):
            Matrix()



class MatrixReprTests(TestCase):

    @patch("points.matrices.Matrix.size")
    def test_matrix_repr(self, mock_size):
        mock_size.return_value = (12, 43)
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertEqual(str(matrix), "<12×43 Matrix>")



class MatrixContainerTests(TestCase):

    def test_items_in_matrix(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertIn(4, matrix)


    def test_items_not_in_matrix(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertNotIn(8, matrix)



class MatrixAdditionTests(TestCase):

    @patch("points.matrices.Matrix.size")
    def test_can_add_matrices(self, mock_size):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        mock_size.return_value = (3, 2)
        matrix2 = Mock(Matrix)
        matrix2._rows = [[10, 20], [30, 40], [50, 60]]
        matrix2.size.return_value = (3, 2)
        matrix3 = matrix + matrix2
        self.assertEqual(matrix3._rows, [[11, 22], [33, 44], [55, 66]])


    def test_can_only_add_matrices(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        with self.assertRaises(TypeError):
            matrix + [1, 2, 3]


    @patch("points.matrices.Matrix.size")
    def test_matrix_addition_needs_equal_size(self, mock_size):
        mock_size.return_value = (3, 4)
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        matrix2 = Mock(Matrix)
        matrix2.size.return_value = (4, 3)
        with self.assertRaises(ValueError):
            matrix + matrix2



class MatrixSubtractionTests(TestCase):

    @patch("points.matrices.Matrix.size")
    def test_can_subtract_matrices(self, mock_size):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        mock_size.return_value = (3, 2)
        matrix2 = Mock(Matrix)
        matrix2._rows = [[10, 20], [30, 40], [50, 60]]
        matrix2.size.return_value = (3, 2)
        matrix3 = matrix - matrix2
        self.assertEqual(matrix3._rows, [[-9, -18], [-27, -36], [-45, -54]])


    def test_can_only_subtract_matrices(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        with self.assertRaises(TypeError):
            matrix - [1, 2, 3]


    @patch("points.matrices.Matrix.size")
    def test_matrix_subtraction_needs_equal_size(self, mock_size):
        mock_size.return_value = (3, 4)
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        matrix2 = Mock(Matrix)
        matrix2.size.return_value = (4, 3)
        with self.assertRaises(ValueError):
            matrix - matrix2


class MatrixMultiplicationTests(TestCase):

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



class MatrixMatMultiplicationTests(TestCase):

    @patch("points.matrices.Matrix.size")
    def test_can_mat_mul_matrices(self, mock_size):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        mock_size.return_value = (3, 2)
        matrix2 = Mock(Matrix)
        matrix2._rows = [[10, 20, 30], [40, 50, 60]]
        matrix2.columns.return_value = ((10, 40), (20, 50), (30, 60))
        matrix2.size.return_value = (2, 3)
        matrix3 = matrix @ matrix2
        self.assertEqual(matrix3._rows, [[90, 120, 150], [190, 260, 330], [290, 400, 510]])


    def test_can_only_matmul_matrices(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        with self.assertRaises(TypeError):
            matrix @ 100


    @patch("points.matrices.Matrix.size")
    def test_matrix_dimensions_must_match(self, mock_size):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        mock_size.return_value = (3, 2)
        matrix2 = Mock(Matrix)
        matrix2._rows = [[10, 20, 30], [40, 50, 60]]
        matrix2.columns.return_value = ((10, 40), (20, 50), (30, 60))
        matrix2.size.return_value = (3, 3)
        with self.assertRaises(ValueError):
            matrix3 = matrix @ matrix2


    def test_matrix_vector_multiplication(self):
        matrix = Matrix([1, 2], [3, 4])
        vector = Mock(Vector)
        vector._values = [5, 6]
        vector.__len__ = MagicMock()
        vector.__len__.return_value = 2
        output = matrix @ vector
        self.assertIsInstance(output, Vector)
        self.assertEqual(output._values, [17, 39])



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



class MatrixSquareTests(TestCase):

    @patch("points.matrices.Matrix.width")
    @patch("points.matrices.Matrix.height")
    def test_square_matrices(self, mock_height, mock_width):
        mock_height.return_value = 4
        mock_width.return_value = 4
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertTrue(matrix.is_square())


    @patch("points.matrices.Matrix.width")
    @patch("points.matrices.Matrix.height")
    def test_square_matrices(self, mock_height, mock_width):
        mock_height.return_value = 4
        mock_width.return_value = 3
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertFalse(matrix.is_square())



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



'''class MatrixInversionTests(TestCase):

    def setUp(self):
        self.patch1 = patch("points.matrices.Matrix.determinant")
        self.mock_det = self.patch1.start()
        self.mock_det.return_value = 5


    def tearDown(self):
        self.patch1.stop()


    def test_determinant_must_be_non_zero(self):
        matrix = Matrix([1, 2], [3, 4])
        self.mock_det.return_value = 0
        with self.assertRaises(ValueError):
            matrix.inverse()'''
