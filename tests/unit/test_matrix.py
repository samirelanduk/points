from unittest import TestCase
from unittest.mock import patch
from points.matrices import Matrix
from points.exceptions import MatrixError

class MatrixCreationTests(TestCase):

    def test_can_make_matrix(self):
        matrix = Matrix((1, 2, 3), (4, 5, 6))
        self.assertEqual(matrix._rows, ((1, 2, 3), (4, 5, 6)))


    def test_all_sequences_converted_to_tuple(self):
        matrix = Matrix([1, 2, 3], (4, 5, 6))
        self.assertEqual(matrix._rows, ((1, 2, 3), (4, 5, 6)))


    def test_matrix_needs_sequences(self):
        with self.assertRaises(TypeError):
            Matrix([1, 2, 3], "456")


    def test_matrix_cannot_be_empty(self):
        with self.assertRaises(TypeError):
            Matrix()
        with self.assertRaises(TypeError):
            Matrix([], [])


    def test_sequences_must_be_equal_in_length(self):
        with self.assertRaises(ValueError):
            Matrix([1, 2, 3], [4, 5])


    def test_matrix_repr(self):
        matrix = Matrix((1, 2, 3), (4, 5, 6))
        self.assertEqual(str(matrix), "<Matrix (2×3)>")



class MatrixRowsAndColumnsTests(TestCase):

    def test_can_get_rows(self):
        matrix = Matrix((1, 2, 3), (4, 5, 6))
        self.assertEqual(matrix.rows(), ((1, 2, 3), (4, 5, 6)))


    def test_can_get_columns(self):
        matrix = Matrix((1, 2, 3), (4, 5, 6))
        self.assertEqual(matrix.columns(), ((1, 4), (2, 5), (3, 6)))


    def test_can_get_size(self):
        matrix = Matrix((1, 2, 3), (4, 5, 6))
        self.assertEqual(matrix.size(), (2, 3))



class MatrixEquality(TestCase):

    def test_equal_points_are_equal(self):
        matrix1 = Matrix((1, 2, 3), (4, 5, 6))
        matrix2 = Matrix((1, 2, 3), (4, 5, 6))
        self.assertEqual(matrix1, matrix2)


    def test_unequal_points_are_not_equal(self):
        matrix1 = Matrix((1, 2, 3), (4, 5, 6))
        matrix2 = Matrix((1, 2, 3), (4, 5.1, 6))
        self.assertNotEqual(matrix1, matrix2)
        self.assertNotEqual(matrix1, "matrix2")



class MatrixAdditionTests(TestCase):

    def test_can_add_points(self):
        matrix1 = Matrix((1, 2, 3), (4, 5, 6))
        matrix2 = Matrix((1, 2, 3), (4, 5, 6))
        matrix3 = matrix1 + matrix2
        self.assertEqual(matrix3.rows(), ((2, 4, 6), (8, 10, 12)))


    @patch("points.matrices.can_add")
    def test_cannot_add_if_function_says_no(self, mock_check):
        mock_check.return_value = False
        matrix1 = Matrix((1, 2, 3), (4, 5, 6))
        matrix2 = Matrix((1, 2, 3), (4, 5, 6))
        with self.assertRaises(MatrixError):
            matrix1 + matrix2


    def test_can_subtract_points(self):
        matrix1 = Matrix((-1, 2, 0), (0, 3, 6))
        matrix2 = Matrix((0, -4, 3), (9, -4, -3))
        matrix3 = matrix1 - matrix2
        self.assertEqual(matrix3.rows(), ((-1, 6, -3), (-9, 7, 9)))


    @patch("points.matrices.can_add")
    def test_cannot_add_if_function_says_no(self, mock_check):
        mock_check.return_value = False
        matrix1 = Matrix((-1, 2, 0), (0, 3, 6))
        matrix2 = Matrix((0, -4, 3), (9, -4, -3))
        with self.assertRaises(MatrixError):
            matrix1 - matrix2



class MatrixMultiplicationTests(TestCase):

    def test_can_multiply_points(self):
        matrix1 = Matrix((1, 2, 3), (4, 5, 6))
        matrix2 = Matrix((7, 8), (9, 10), (11, 12))
        matrix3 = matrix1 * matrix2
        self.assertEqual(matrix3.rows(), ((58, 64), (139, 154)))


    @patch("points.matrices.can_multiply")
    def test_cannot_multiply_if_function_says_no(self, mock_check):
        mock_check.return_value = False
        matrix1 = Matrix((1, 2, 3), (4, 5, 6))
        matrix2 = Matrix((7, 8), (9, 10), (11, 12))
        with self.assertRaises(MatrixError):
            matrix1 * matrix2


    def test_matrix_multiplication_is_not_commutative(self):
        matrix1 = Matrix((1, 2), (4, 5))
        matrix2 = Matrix((100, -2), (4.4, 50))
        self.assertNotEqual(matrix1 * matrix2, matrix2 * matrix1)


    def test_can_multiply_points_by_scalar(self):
        matrix = Matrix((1, 2, 3), (4, 5, 6))
        self.assertEqual(
         matrix * 3,
         Matrix((3, 6, 9), (12, 15, 18))
        )
        self.assertEqual(
         3 * matrix,
         Matrix((3, 6, 9), (12, 15, 18))
        )
