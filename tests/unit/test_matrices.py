from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock
from points.matrices import Matrix

class MatrixCreationTests(TestCase):

    def test_can_make_matrix(self):
        matrix = Matrix([1, 2], [3, 4])
        self.assertEqual(matrix._rows, [[1, 2], [3, 4]])


    def test_can_make_matrix_with_tuple(self):
        matrix = Matrix([1, 2], (3, 4))
        self.assertEqual(matrix._rows, [[1, 2], [3, 4]])


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
        self.assertEqual(matrix.size(), (50, 35))
        mock_width.assert_called_with()
        mock_height.assert_called_with()



class MatrixRowsTests(TestCase):

    def test_can_get_rows(self):
        matrix = Matrix([1, 2], [3, 4], [5, 6])
        self.assertEqual(matrix.rows(), ((1, 2), (3, 4), (5, 6)))
