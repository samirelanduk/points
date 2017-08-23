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



class VectorReprTests(TestCase):

    def test_vector_repr(self):
        vector = Vector(2, 5, 1)
        self.assertEqual(str(vector), "<Vector [2, 5, 1]>")



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
