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



class VectorReprTests(TestCase):

    def test_vector_repr(self):
        vector = Vector(2, 5, 1)
        self.assertEqual(repr(vector), "<Vector [2, 5, 1]>")



class VectorStrTests(TestCase):

    @patch("points.vectors.Vector.__repr__")
    def test_vector_str(self, mock_repr):
        mock_repr.return_value = "xxxxx"
        vector = Vector(2, 5, 1)
        self.assertEqual(str(vector), "xxxxx")
        self.assertTrue(mock_repr.called)


    @patch("points.vectors.Vector.__repr__")
    def test_long_vector_str(self, mock_repr):
        vector = Vector(range(1, 11))
        self.assertEqual(
         str(vector), "<Vector [1, 2, (...6 items omitted...), 9, 10]>"
        )
        self.assertFalse(mock_repr.called)



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



class VectorIndexingSettingTests(TestCase):

    def test_can_set_vector_index(self):
        vector = Vector(2, 5, 1)
        vector[0] = 4
        vector[1] = 6
        vector[2] = 8
        self.assertEqual(vector._values, [4, 6, 8])


    def test_cannot_set_vector_out_of_index(self):
        vector = Vector(2, 5, 1)
        with self.assertRaises(IndexError):
            vector[3] = 9



class VectorLenTests(TestCase):

    def test_can_get_vector_len(self):
        vector = Vector(2, 5, 1)
        self.assertEqual(len(vector), 3)



class VectorIterationTests(TestCase):

    def test_vector_is_iterable(self):
        vector = Vector(2, 5, 1)
        self.assertEqual(list(iter(vector)), vector._values)



class VectorAdditionTests(TestCase):

    def setUp(self):
        self.vector2 = Mock(Vector)
        self.patch1 = patch("points.vectors.Vector.__len__")
        self.mock_length = self.patch1.start()
        self.mock_length.return_value = 9
        self.vector2.__len__, self.vector2.__len__.return_value = MagicMock(), 9
        self.vector2._values = [10, 20, 30]


    def tearDown(self):
        self.patch1.stop()


    def test_can_only_add_vectors(self):
        vector = Vector(2, 5, 1)
        with self.assertRaises(TypeError):
            vector + "vector"


    def test_cannot_add_vectors_of_different_length(self):
        self.vector2.__len__.return_value = 8
        vector = Vector(2, 5, 1)
        self.mock_length.return_value = 3
        with self.assertRaises(ValueError):
            vector + self.vector2


    def test_can_add_vectors(self):
        vector = Vector(2, 5, 1)
        new = vector + self.vector2
        self.assertEqual(new._values, [12, 25, 31])



class VectorSubtractionTests(TestCase):

    def setUp(self):
        self.vector2 = Mock(Vector)
        self.patch1 = patch("points.vectors.Vector.__len__")
        self.mock_length = self.patch1.start()
        self.mock_length.return_value = 9
        self.vector2.__len__, self.vector2.__len__.return_value = MagicMock(), 9
        self.vector2._values = [1, 2, 3]


    def tearDown(self):
        self.patch1.stop()


    def test_can_only_subtract_vectors(self):
        vector = Vector(2, 5, 1)
        with self.assertRaises(TypeError):
            vector - "vector"


    def test_cannot_subtract_vectors_of_different_length(self):
        self.vector2.__len__.return_value = 8
        vector = Vector(2, 5, 1)
        self.mock_length.return_value = 3
        with self.assertRaises(ValueError):
            vector - self.vector2


    def test_can_subtract_vectors(self):
        vector = Vector(2, 5, 1)
        new = vector - self.vector2
        self.assertEqual(new._values, [1, 3, -2])



class VectorScalarMultiplicationTests(TestCase):

    def test_can_multiply_vector_by_scalar(self):
        vector = Vector(2, 5, 1)
        new = vector * 3
        self.assertEqual(new._values, [6, 15, 3])


    def test_can_multiply_scalar_by_vector(self):
        vector = Vector(2, 5, 1)
        new = 3 * vector
        self.assertEqual(new._values, [6, 15, 3])


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



class VectorMagnitudeTests(TestCase):

    def test_can_get_vector_magnitude(self):
        vector = Vector(3, 4)
        self.assertEqual(vector.magnitude(), 5)



class VectorValueAppendingTests(TestCase):

    def test_can_add_value(self):
        vector = Vector(2, 5, 1)
        vector.append(12)
        self.assertEqual(vector._values, [2, 5, 1, 12])



class VectorValueInsertionTests(TestCase):

    def test_can_insert_value(self):
        vector = Vector(2, 5, 1)
        vector.insert(1, 12)
        self.assertEqual(vector._values, [2, 12, 5, 1])



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



class VectorComponentTests(TestCase):

    def test_can_get_vector_components(self):
        vector = Vector(3, 4)
        components = vector.components()
        self.assertEqual(len(components), 2)
        self.assertEqual(components[0]._values, [3, 0])
        self.assertEqual(components[1]._values, [0, 4])



class VectorLinearDependenceTests(TestCase):

    @patch("points.vectors.VectorSpan")
    def test_can_check_linear_dependence(self, mock_span):
        vector = Vector(3, 4)
        v2, v3 = Mock(Vector), Mock(Vector)
        mock_span.return_value = [vector]
        self.assertTrue(vector.linearly_dependent_on(v2, v3))
        mock_span.assert_called_with(v2, v3)
        mock_span.return_value = []
        self.assertFalse(vector.linearly_dependent_on(v2, v3))



class VectorLinearIndependenceTests(TestCase):

    @patch("points.vectors.Vector.linearly_dependent_on")
    def test_can_check_linear_independence(self, mock_dep):
        mock_dep.return_value = True
        vector = Vector(3, 4)
        v2, v3 = Mock(Vector), Mock(Vector)
        self.assertFalse(vector.linearly_independent_of(v2, v3))
        mock_dep.assert_called_with(v2, v3)
        mock_dep.return_value = False
        self.assertTrue(vector.linearly_independent_of(v2, v3))
        mock_dep.assert_called_with(v2, v3)



class VectorSpanTests(TestCase):

    @patch("points.vectors.VectorSpan")
    def test_can_get_span(self, mock_span):
        mock_span.return_value = "SPAN"
        vector = Vector(3, 4)
        self.assertEqual(vector.span(), "SPAN")
        mock_span.assert_called_with(vector)



class VectorSpanWithTests(TestCase):

    @patch("points.vectors.VectorSpan")
    def test_can_get_span(self, mock_span):
        mock_span.return_value = "SPAN"
        vector = Vector(3, 4)
        v2, v3 = Mock(Vector), Mock(Vector)
        self.assertEqual(vector.span_with(v2, v3), "SPAN")
        mock_span.assert_called_with(vector, v2, v3)



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
        vector1 = Vector(3, -3, 1)
        vector2._values = [4, 9]
        with self.assertRaises(ValueError):
            vector1.cross(vector2)



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


    def test_angle_requires_vector(self):
        vector1 = Vector(-6, -8)
        with self.assertRaises(TypeError):
            vector1.angle_with("vector")


    def test_angle_requires_equal_length(self):
        vector1 = Vector(-6, 8)
        vector2 = Mock(Vector)
        vector2.length.return_value = 3
        with self.assertRaises(ValueError):
            vector1.angle_with(vector2)





'''





class VectorRotation(TestCase):

    def setUp(self):
        self.vector = Mock()
        self.matrix = Mock()
        self.matrix.__matmul__ = MagicMock()
        self.matrix.__matmul__.return_value = self.vector


    @patch("points.matrices.Matrix")
    def test_can_do_2d_rotation(self, mock_matrix):
        self.vector._values = [-4, 3]
        mock_matrix.return_value = self.matrix
        v = Vector(3, 4)
        v.rotate(pi / 2)
        matrix_args = mock_matrix.call_args_list[0][0]
        self.assertAlmostEqual(matrix_args[0][0], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[0][1], -1, delta=0.005)
        self.assertAlmostEqual(matrix_args[1][0], 1, delta=0.005)
        self.assertAlmostEqual(matrix_args[1][1], 0, delta=0.005)
        self.matrix.__matmul__.assert_called_with(v)
        self.assertEqual(v._values, [-4, 3])


    @patch("points.matrices.Matrix")
    def test_can_do_3d_rotation_x(self, mock_matrix):
        self.vector._values = [-4, 3, 5]
        mock_matrix.return_value = self.matrix
        v = Vector(3, 4, 5)
        v.rotate(pi / 2, "x")
        matrix_args = mock_matrix.call_args_list[0][0]
        self.assertAlmostEqual(matrix_args[0][0], 1, delta=0.005)
        self.assertAlmostEqual(matrix_args[0][1], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[0][2], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[1][0], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[1][1], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[1][2], -1, delta=0.005)
        self.assertAlmostEqual(matrix_args[2][0], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[2][1], 1, delta=0.005)
        self.assertAlmostEqual(matrix_args[2][2], 0, delta=0.005)
        self.matrix.__matmul__.assert_called_with(v)
        self.assertEqual(v._values, [-4, 3, 5])


    @patch("points.matrices.Matrix")
    def test_can_do_3d_rotation_y(self, mock_matrix):
        self.vector._values = [-4, 3, 5]
        mock_matrix.return_value = self.matrix
        v = Vector(3, 4, 5)
        v.rotate(pi / 2, "y")
        matrix_args = mock_matrix.call_args_list[0][0]
        self.assertAlmostEqual(matrix_args[0][0], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[0][1], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[0][2], 1, delta=0.005)
        self.assertAlmostEqual(matrix_args[1][0], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[1][1], 1, delta=0.005)
        self.assertAlmostEqual(matrix_args[1][2], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[2][0], -1, delta=0.005)
        self.assertAlmostEqual(matrix_args[2][1], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[2][2], 0, delta=0.005)
        self.matrix.__matmul__.assert_called_with(v)
        self.assertEqual(v._values, [-4, 3, 5])


    @patch("points.matrices.Matrix")
    def test_can_do_3d_rotation_z(self, mock_matrix):
        self.vector._values = [-4, 3, 5]
        mock_matrix.return_value = self.matrix
        v = Vector(3, 4, 5)
        v.rotate(pi / 2, "z")
        matrix_args = mock_matrix.call_args_list[0][0]
        self.assertAlmostEqual(matrix_args[0][0], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[0][1], -1, delta=0.005)
        self.assertAlmostEqual(matrix_args[0][2], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[1][0], 1, delta=0.005)
        self.assertAlmostEqual(matrix_args[1][1], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[1][2], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[2][0], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[2][1], 0, delta=0.005)
        self.assertAlmostEqual(matrix_args[2][2], 1, delta=0.005)
        self.matrix.__matmul__.assert_called_with(v)
        self.assertEqual(v._values, [-4, 3, 5])


    def test_only_2_and_3_d_vectors_can_rotate(self):
        vector = Vector(1)
        with self.assertRaises(ValueError):
            vector.rotate(pi)
        vector = Vector(1, 2, 3, 4)
        with self.assertRaises(ValueError):
            vector.rotate(pi)


    def test_axis_must_be_valid(self):
        vector = Vector(1, 2, 3)
        with self.assertRaises(ValueError):
            vector.rotate(pi, "n")
















'''
