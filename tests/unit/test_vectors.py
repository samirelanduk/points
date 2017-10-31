from math import pi
from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock
from points.vectors import Vector

class VectorCreationTests(TestCase):

    def test_can_make_vector(self):
        vector = Vector(2, 5, 1)
        self.assertEqual(vector._values, [2, 5, 1])


    def test_can_make_vector_from_sequence(self):
        vector = Vector([2, 5, 1])
        self.assertEqual(vector._values, [2, 5, 1])
        vector = Vector((2, 5, 1))
        self.assertEqual(vector._values, [2, 5, 1])


    def test_can_make_vector_from_one_number(self):
        vector = Vector(2)
        self.assertEqual(vector._values, [2])


    def test_vector_values_must_be_numeric(self):
        with self.assertRaises(TypeError):
            vector = Vector([2, "5", 1])



class VectorReprTests(TestCase):

    def test_vector_repr(self):
        vector = Vector(2, 5, 1)
        self.assertEqual(str(vector), "<Vector [2, 5, 1]>")



class VectorContainerTests(TestCase):

    def test_vector_is_container(self):
        vector = Vector(2, 5, 1)
        self.assertIn(5, vector)
        self.assertNotIn(7, vector)



class VectorIndexingGettingTests(TestCase):

    def test_can_get_vector_index(self):
        vector = Vector(2, 5, 1)
        self.assertEqual(vector[0], 2)
        self.assertEqual(vector[1], 5)
        self.assertEqual(vector[2], 1)



class VectorLenTests(TestCase):

    def test_can_get_vector_len(self):
        vector = Vector(2, 5, 1)
        self.assertEqual(len(vector), 3)



class VectorAdditionTests(TestCase):

    @patch("points.vectors.Vector.length")
    def test_can_add_vectors(self, mock_length):
        vector = Vector(2, 5, 1)
        vector2 = Mock(Vector)
        mock_length.return_value = 3
        vector2.length.return_value = 3
        vector2._values = [1, 2, 3]
        vector3 = vector + vector2
        self.assertIsInstance(vector3, Vector)
        self.assertEqual(vector3._values, [3, 7, 4])


    @patch("points.vectors.Vector.length")
    def test_cant_add_vectors_of_different_length(self, mock_length):
        vector = Vector(2, 5, 1)
        vector2 = Mock(Vector)
        mock_length.return_value = 3
        vector2.length.return_value = 2
        vector2._values = [1, 2, 3]
        with self.assertRaises(ValueError):
            vector + vector2


    def test_can_only_add_vectors(self):
        vector = Vector(2, 5, 1)
        with self.assertRaises(TypeError):
            vector + "vector"



class VectorSubtractionTests(TestCase):

    @patch("points.vectors.Vector.length")
    def test_can_subtract_vectors(self, mock_length):
        vector = Vector(2, 5, 1)
        vector2 = Mock(Vector)
        mock_length.return_value = 3
        vector2.length.return_value = 3
        vector2._values = [1, 2, 3]
        vector3 = vector - vector2
        self.assertIsInstance(vector3, Vector)
        self.assertEqual(vector3._values, [1, 3, -2])


    @patch("points.vectors.Vector.length")
    def test_cant_subtract_vectors_of_different_length(self, mock_length):
        vector = Vector(2, 5, 1)
        vector2 = Mock(Vector)
        mock_length.return_value = 3
        vector2.length.return_value = 2
        vector2._values = [1, 2, 3]
        with self.assertRaises(ValueError):
            vector - vector2


    def test_can_only_subtract_vectors(self):
        vector = Vector(2, 5, 1)
        with self.assertRaises(TypeError):
            vector - "vector"



class VectorScalarMultiplicationTests(TestCase):

    def test_can_multiply_vector_by_scalar(self):
        vector = Vector(2, 5, 1)
        vector2 = vector * 3
        self.assertIsInstance(vector2, Vector)
        self.assertEqual(vector2._values, [6, 15, 3])


    def test_can_multiply_scalar_by_vector(self):
        vector = Vector(2, 5, 1)
        vector2 = 3 * vector
        self.assertIsInstance(vector2, Vector)
        self.assertEqual(vector2._values, [6, 15, 3])


    def test_only_scalar_multiplication_allowed(self):
        vector = Vector(2, 5, 1)
        with self.assertRaises(TypeError):
            vector * Mock(Vector)



class VectorLengthTests(TestCase):

    @patch("points.vectors.Vector.__len__")
    def test_can_get_vector_len(self, mock_len):
        vector = Vector(2, 5, 1)
        mock_len.return_value = 100
        self.assertEqual(vector.length(), 100)



class VectorValuesTests(TestCase):

    def test_can_get_values(self):
        vector = Vector(2, 5, 1)
        self.assertEqual(vector.values(), (2, 5, 1))



class VectorValueAdditionTests(TestCase):

    def test_can_add_value(self):
        vector = Vector(2, 5, 1)
        vector.add(12)
        self.assertEqual(vector._values, [2, 5, 1, 12])


    def test_can_only_add_numbers(self):
        vector = Vector(2, 5, 1)
        with self.assertRaises(TypeError):
            vector.add("12")



class VectorValueInsertionTests(TestCase):

    def test_can_insert_value(self):
        vector = Vector(2, 5, 1)
        vector.insert(1, 12)
        self.assertEqual(vector._values, [2, 12, 5, 1])


    def test_can_only_insert_numbers(self):
        vector = Vector(2, 5, 1)
        with self.assertRaises(TypeError):
            vector.insert(1, "12")



class VectorValueRemovalTests(TestCase):

    def test_can_remove_value(self):
        vector = Vector(2, 5, 1)
        vector.remove(5)
        self.assertEqual(vector._values, [2, 1])



class ValuePoppingTests(TestCase):

    def test_can_pop_value(self):
        vector = Vector(2, 5, 1)
        val = vector.pop()
        self.assertEqual(val, 1)
        self.assertEqual(vector._values, [2, 5])


    def test_can_pop_any_position(self):
        vector = Vector(2, 5, 1)
        val = vector.pop(1)
        self.assertEqual(val, 5)
        self.assertEqual(vector._values, [2, 1])



class VectorMagnitudeTests(TestCase):

    def test_can_get_vector_magnitude(self):
        vector = Vector(3, 4)
        self.assertEqual(vector.magnitude(), 5)



class VectorComponentTests(TestCase):

    def test_can_get_vector_components(self):
        vector = Vector(3, 4)
        components = vector.components()
        self.assertEqual(len(components), 2)
        self.assertIsInstance(components[0], Vector)
        self.assertIsInstance(components[1], Vector)
        self.assertEqual(components[0]._values, [3, 0])
        self.assertEqual(components[1]._values, [0, 4])



class VectorRotation(TestCase):

    @patch("points.matrices.Matrix")
    def test_can_do_2d_rotation(self, mock_matrix):
        matrix = Mock(name="matrix")
        vector = Mock(name="vector")
        vector._values = [-4, 3]
        matrix.__matmul__ = MagicMock()
        matrix.__matmul__.return_value = vector
        mock_matrix.return_value = matrix
        v = Vector(3, 4)
        v.rotate(pi / 2)
        matrix_args = mock_matrix.call_args_list[0][0]
        self.assertAlmostEqual(matrix_args[0][0], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[0][1], -1, delta=0.005)
        self.assertAlmostEqual(matrix_args[1][0], 1, delta=0.005)
        self.assertAlmostEqual(matrix_args[1][1], 0, delta=0.005)
        matrix.__matmul__.assert_called_with(v)
        self.assertEqual(v._values, [-4, 3])



class VectorDistanceTests(TestCase):

    @patch("points.vectors.Vector.__sub__")
    def test_can_get_distance_between_vectors(self, mock_sub):
        vector1 = Vector(3, 4)
        vector2 = Mock(Vector)
        resultant_vector = Mock(Vector)
        mock_sub.return_value = resultant_vector
        resultant_vector.magnitude.return_value = 100
        distance = vector1.distance_to(vector2)
        mock_sub.assert_called_with(vector2)
        self.assertEqual(distance, 100)



class VectorDotProductTests(TestCase):

    def test_can_get_dot_product(self):
        vector1 = Vector(-6, 8)
        vector2 = Mock(Vector)
        vector2._values = [5, 12]
        vector2.length.return_value = 2
        self.assertEqual(vector1.dot(vector2), 66)


    def test_dot_product_requires_vector(self):
        vector1 = Vector(-6, -8)
        with self.assertRaises(TypeError):
            vector1.dot("vector")


    def test_dot_product_requires_equal_length(self):
        vector1 = Vector(-6, 8)
        vector2 = Mock(Vector)
        vector2.length.return_value = 3
        with self.assertRaises(ValueError):
            vector1.dot(vector2)



class VectorCrossProductTests(TestCase):

    def test_can_get_cross_product(self):
        vector1 = Vector(3, -3, 1)
        vector2 = Mock(Vector)
        vector2._values = [4, 9, 2]
        self.assertEqual(vector1.cross(vector2)._values, [-15, -2, 39])


    def test_cross_product_requires_vector(self):
        vector1 = Vector(-6, -8)
        with self.assertRaises(TypeError):
            vector1.cross("vector")


    def test_cross_product_requires_length_3(self):
        vector1 = Vector(-6, 8)
        vector2 = Mock(Vector)
        vector2._values = [4, 9, 2]
        with self.assertRaises(ValueError):
            vector1.cross(vector2)



class VectorAngleWithTests(TestCase):

    @patch("points.vectors.Vector.magnitude")
    @patch("points.vectors.Vector.dot")
    def test_can_get_angle_between_vectors(self, mock_dot, mock_mag):
        mock_dot.return_value = 1
        mock_mag.return_value = 4
        vector1 = Vector(7, 1)
        vector2 = Mock(Vector)
        vector2.magnitude.return_value = 0.5
        vector2.length.return_value = 2
        self.assertAlmostEqual(vector1.angle_with(vector2), 1.0471, delta=0.0005)


    def test_dot_product_requires_vector(self):
        vector1 = Vector(-6, -8)
        with self.assertRaises(TypeError):
            vector1.angle_with("vector")


    def test_dot_product_requires_equal_length(self):
        vector1 = Vector(-6, 8)
        vector2 = Mock(Vector)
        vector2.length.return_value = 3
        with self.assertRaises(ValueError):
            vector1.angle_with(vector2)
