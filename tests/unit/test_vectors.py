from unittest import TestCase
from unittest.mock import Mock, patch
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


    @patch("points.vectors.are_numeric")
    def test_vector_values_must_be_numeric(self, mock_are):
        mock_are.return_value = False
        with self.assertRaises(TypeError):
            vector = Vector([2, 5, 1])



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


    @patch("points.vectors.is_numeric")
    @patch("points.vectors.are_numeric")
    def test_can_only_add_numbers(self, mock_are, mock_is):
        mock_is.return_value = False
        mock_are.return_value = True
        vector = Vector(2, 5, 1)
        with self.assertRaises(TypeError):
            vector.add(12)
        mock_is.assert_called_with(12)



class VectorValueInsertionTests(TestCase):

    def test_can_insert_value(self):
        vector = Vector(2, 5, 1)
        vector.insert(1, 12)
        self.assertEqual(vector._values, [2, 12, 5, 1])


    @patch("points.vectors.is_numeric")
    @patch("points.vectors.are_numeric")
    def test_can_only_insert_numbers(self, mock_are, mock_is):
        mock_is.return_value = False
        mock_are.return_value = True
        vector = Vector(2, 5, 1)
        with self.assertRaises(TypeError):
            vector.insert(1, 12)
        mock_is.assert_called_with(12)



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
        self.assertAlmostEqual(vector1.angle_with(vector2), 60, delta=0.0000005)


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
