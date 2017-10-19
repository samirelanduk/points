from unittest import TestCase
from unittest.mock import Mock, patch
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
