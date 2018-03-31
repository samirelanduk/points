import math
from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock
from points.geometry import *
from points.vectors import Vector

class GeometryTest(TestCase):

    def setUp(self):
        self.v1, self.v2, self.v3 = Mock(Vector), Mock(Vector), Mock(Vector)
        self.v1._values, self.v2._values, self.v3._values = [1, 2, 3], [4, 5, 6], [7, 8, 9]



class VectorRoundingDecoratorTests(GeometryTest):

    def setUp(self):
        GeometryTest.setUp(self)
        self.func = lambda a, b, c: None


    def test_can_ignore_vector_values(self):
        self.v1._values = [0.123, 0.456]
        self.v2._values = [0.456, 0.789]
        func = round_vectors(self.func)
        func("a", self.v1, self.v2)
        self.assertEqual(self.v1._values, [0.123, 0.456])
        self.assertEqual(self.v2._values, [0.456, 0.789])


    def test_can_round_vector_values(self):
        self.v1._values = [0.123, 0.456]
        self.v2._values = [0.456, 0.789]
        func = round_vectors(self.func)
        func("a", self.v1, self.v2, trim=2)
        self.assertEqual(self.v1._values, [0.12, 0.46])
        self.assertEqual(self.v2._values, [0.46, 0.79])



class VectorRoundingDecoratorTests(GeometryTest):

    def setUp(self):
        GeometryTest.setUp(self)
        self.func = lambda a, b, c: a


    def test_can_just_use_radians(self):
        func = allow_degrees(self.func)
        self.assertEqual(func(math.pi, 2, 3), math.pi)


    def test_can_convert_to_degrees(self):
        func = allow_degrees(self.func)
        self.assertEqual(func(180, 2, 3, degrees=True), math.pi)



class TranslationTests(GeometryTest):

    def test_can_translate(self):
        translate_vectors((10, -20, 5), self.v1, self.v2)
        self.assertEqual(self.v1._values, [11, -18, 8])
        self.assertEqual(self.v2._values, [14, -15, 11])


    def test_translation_needs_vectors(self):
        with self.assertRaises(TypeError):
            translate_vectors((10, -20, 5), self.v1, self.v2, "vector")


    def test_translation_needs_correct_dimension(self):
        with self.assertRaises(ValueError):
            translate_vectors((10, -20), self.v1, self.v2)
        self.v3._values = [7, 8]
        with self.assertRaises(ValueError):
            translate_vectors((10, -20, 5), self.v1, self.v2, self.v3)



class Rotation2dTests(GeometryTest):

    def setUp(self):
        GeometryTest.setUp(self)
        self.patch1 = patch("points.geometry.Matrix")
        self.patch2 = patch("points.geometry.translate_vectors")
        self.mock_matrix = self.patch1.start()
        self.mock_trans = self.patch2.start()
        self.v1._values.pop(), self.v2._values.pop()


    def tearDown(self):
        self.patch1.stop()
        self.patch2.stop()


    def test_can_rotate_2d(self):
        matrix = Mock()
        self.mock_matrix.return_value = matrix
        matrix.__matmul__ = MagicMock()
        matrix.__matmul__.side_effect = [self.v2, self.v3, self.v1]
        rotate_2d_vectors(0.5, self.v1, self.v2)
        self.mock_matrix.assert_called_with(
         [cos(0.5), -sin(0.5)], [sin(0.5), cos(0.5)]
        )
        matrix.__matmul__.assert_any_call(self.v1)
        matrix.__matmul__.assert_any_call(self.v2)
        self.assertEqual(self.v1._values, [4, 5])
        self.assertEqual(self.v2._values, [7, 8, 9])
        self.assertFalse(self.mock_trans.called)


    def test_can_rotate_2d_about_point(self):
        matrix = Mock()
        self.mock_matrix.return_value = matrix
        matrix.__matmul__ = MagicMock()
        matrix.__matmul__.side_effect = [self.v2, self.v3, self.v1]
        rotate_2d_vectors(0.5, self.v1, self.v2, point=[1, 2])
        self.mock_trans.assert_any_call((-1, -2), self.v1, self.v2)
        self.mock_matrix.assert_called_with(
         [cos(0.5), -sin(0.5)], [sin(0.5), cos(0.5)]
        )
        matrix.__matmul__.assert_any_call(self.v1)
        matrix.__matmul__.assert_any_call(self.v2)
        self.assertEqual(self.v1._values, [4, 5])
        self.assertEqual(self.v2._values, [7, 8, 9])
        self.mock_trans.assert_any_call((1, 2), self.v1, self.v2)


    def test_rotation_needs_vectors(self):
        with self.assertRaises(TypeError):
            rotate_2d_vectors(0.5, self.v1, self.v2, "vector")


    def test_translation_needs_2d_vectors(self):
        with self.assertRaises(ValueError):
            rotate_2d_vectors(0.5, self.v1, self.v2, self.v3)


    def test_point_must_be_correct_dimension(self):
        with self.assertRaises(ValueError):
            rotate_2d_vectors(0.5, self.v1, self.v2, point=[1, 2, 3])



class Rotation3dTests(GeometryTest):

    def setUp(self):
        GeometryTest.setUp(self)
        self.patch1 = patch("points.geometry.Matrix")
        self.patch2 = patch("points.geometry.translate_vectors")
        self.mock_trans = self.patch2.start()
        self.mock_matrix = self.patch1.start()
        self.v3._values.pop()


    def tearDown(self):
        self.patch1.stop()
        self.patch2.stop()


    def test_can_rotate_3d_x(self):
        matrix = Mock()
        self.mock_matrix.return_value = matrix
        matrix.__matmul__ = MagicMock()
        matrix.__matmul__.side_effect = [self.v2, self.v3, self.v1]
        rotate_3d_vectors(0.5, 0, self.v1, self.v2)
        self.mock_matrix.assert_called_with(
         [1, 0, 0], [0, cos(0.5), -sin(0.5)], [0, sin(0.5), cos(0.5)]
        )
        matrix.__matmul__.assert_any_call(self.v1)
        matrix.__matmul__.assert_any_call(self.v2)
        self.assertEqual(self.v1._values, [4, 5, 6])
        self.assertEqual(self.v2._values, [7, 8])
        self.assertFalse(self.mock_trans.called)


    def test_can_rotate_3d_y(self):
        matrix = Mock()
        self.mock_matrix.return_value = matrix
        matrix.__matmul__ = MagicMock()
        matrix.__matmul__.side_effect = [self.v2, self.v3, self.v1]
        rotate_3d_vectors(0.5, 1, self.v1, self.v2)
        self.mock_matrix.assert_called_with(
         [cos(0.5), 0, sin(0.5)], [0, 1, 0], [-sin(0.5), 0, cos(0.5)]
        )
        matrix.__matmul__.assert_any_call(self.v1)
        matrix.__matmul__.assert_any_call(self.v2)
        self.assertEqual(self.v1._values, [4, 5, 6])
        self.assertEqual(self.v2._values, [7, 8])
        self.assertFalse(self.mock_trans.called)


    def test_can_rotate_3d_z(self):
        matrix = Mock()
        self.mock_matrix.return_value = matrix
        matrix.__matmul__ = MagicMock()
        matrix.__matmul__.side_effect = [self.v2, self.v3, self.v1]
        rotate_3d_vectors(0.5, 2, self.v1, self.v2)
        self.mock_matrix.assert_called_with(
         [cos(0.5), -sin(0.5), 0], [sin(0.5), cos(0.5), 0], [0, 0, 1]
        )
        matrix.__matmul__.assert_any_call(self.v1)
        matrix.__matmul__.assert_any_call(self.v2)
        self.assertEqual(self.v1._values, [4, 5, 6])
        self.assertEqual(self.v2._values, [7, 8])
        self.assertFalse(self.mock_trans.called)


    def test_can_rotate_3d_about_point(self):
        matrix = Mock()
        self.mock_matrix.return_value = matrix
        matrix.__matmul__ = MagicMock()
        matrix.__matmul__.side_effect = [self.v2, self.v3, self.v1]
        rotate_3d_vectors(0.5, 0, self.v1, self.v2, point=[1, 2, 3])
        self.mock_trans.assert_any_call((-1, -2, -3), self.v1, self.v2)
        self.mock_matrix.assert_called_with(
         [1, 0, 0], [0, cos(0.5), -sin(0.5)], [0, sin(0.5), cos(0.5)]
        )
        matrix.__matmul__.assert_any_call(self.v1)
        matrix.__matmul__.assert_any_call(self.v2)
        self.assertEqual(self.v1._values, [4, 5, 6])
        self.assertEqual(self.v2._values, [7, 8])
        self.mock_trans.assert_any_call((1, 2, 3), self.v1, self.v2)


    def test_rotation_needs_vectors(self):
        with self.assertRaises(TypeError):
            rotate_3d_vectors(0.5, 0, self.v1, self.v2, "vector")


    def test_translation_needs_3d_vectors(self):
        with self.assertRaises(ValueError):
            rotate_3d_vectors(0.5, 0, self.v1, self.v2, self.v3)


    def test_dimension_must_be_valid(self):
        with self.assertRaises(ValueError):
            rotate_3d_vectors(0.5, 3, self.v1, self.v2)


    def test_point_must_be_correct_dimension(self):
        with self.assertRaises(ValueError):
            rotate_3d_vectors(0.5, 1, self.v1, self.v2, point=[1, 2])



class VectorAlignmentTests(GeometryTest):

    @patch("points.geometry.Vector")
    @patch("points.geometry.rotate_3d_vectors")
    def test_can_align_vectors(self, mock_rotate, mock_vector):
        vector1, vector2 = Mock(Vector), Mock(Vector)
        mock_vector.side_effect = vector1, vector2
        vector1.angle_with.return_value = 25
        align_vectors_to_plane(1, 2, self.v1, self.v2, self.v3)
        mock_vector.assert_any_call(0, 0, 1)
        mock_vector.assert_any_call(1, 0, 3)
        vector1.angle_with.assert_called_with(vector2)
        mock_rotate.assert_called_with(25, 1, self.v1, self.v2, self.v3)


    def test_alignment_axes_must_be_valid(self):
        with self.assertRaises(ValueError):
            align_vectors_to_plane(3, 2, self.v1, self.v2, self.v3)
        with self.assertRaises(ValueError):
            align_vectors_to_plane(2, 3, self.v1, self.v2, self.v3)
        with self.assertRaises(ValueError):
            align_vectors_to_plane(2, 2, self.v1, self.v2, self.v3)
