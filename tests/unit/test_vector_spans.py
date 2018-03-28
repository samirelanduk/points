from unittest import TestCase
from unittest.mock import Mock, patch, MagicMock
from points.vectors import Vector, VectorSpan

class VectorSpanTest(TestCase):

    def setUp(self):
        self.v1, self.v2, self.v3, self.v4 = [Mock(Vector) for _ in range(4)]
        for v in self.v1, self.v2, self.v3, self.v4:
            v.__len__, v.__len__.return_value = MagicMock(), 3
            v.values.return_value = (2, 5, -9)
            v.__iter__, v.__iter__.return_value = MagicMock(), iter([2, 5, -9])
            v.linearly_independent_of.return_value = True


class VectorSpanCreationTests(VectorSpanTest):

    def test_can_make_vector_span(self):
        span = VectorSpan(self.v1)
        self.assertEqual(span._vectors, {self.v1})
        self.assertEqual(span._dimension, 3)


    def test_can_make_vector_spans_from_multiple_vectors(self):
        span = VectorSpan(self.v1, self.v2, self.v3, self.v4)
        self.assertEqual(span._vectors, {self.v1, self.v2, self.v3, self.v4})
        self.assertEqual(span._dimension, 3)
        self.v2.linearly_independent_of.assert_called_with(self.v1)
        self.assertEqual(
         set(self.v3.linearly_independent_of.call_args[0]), {self.v1, self.v2}
        )
        self.assertEqual(
         set(self.v4.linearly_independent_of.call_args[0]),
         {self.v1, self.v2, self.v3}
        )


    def test_vectors_in_space_must_be_same_dimension(self):
        self.v3.__len__.return_value = 2
        with self.assertRaises(ValueError):
            VectorSpan(self.v1, self.v2, self.v3, self.v4)


    def test_only_independent_vectors_kept(self):
        self.v4.linearly_independent_of.return_value = False
        span = VectorSpan(self.v1, self.v2, self.v3, self.v4)
        self.assertEqual(span._vectors, {self.v1, self.v2, self.v3})
        self.assertEqual(span._dimension, 3)
        self.v2.linearly_independent_of.assert_called_with(self.v1)
        self.assertEqual(
         set(self.v3.linearly_independent_of.call_args[0]), {self.v1, self.v2}
        )
        self.assertEqual(
         set(self.v4.linearly_independent_of.call_args[0]),
         {self.v1, self.v2, self.v3}
        )



class VectorSpanReprTests(VectorSpanTest):

    def test_vector_span_repr_one_vector(self):
        self.v1.values.return_value = (1, 4, 9)
        span = VectorSpan(self.v1)
        self.assertEqual(repr(span), "<VectorSpan of [1, 4, 9] - 3 dimensions>")


    def test_vector_span_repr_multiple_vectors(self):
        span = VectorSpan(self.v1, self.v2, self.v3)
        self.assertEqual(repr(span), "<VectorSpan - 3 dimensions>")



class VectorSpanContainerTests(VectorSpanTest):

    def test_non_dimension_vector_never_present(self):
        span = VectorSpan(self.v1, self.v2, self.v3)
        self.v4.__len__.return_value = 4
        self.assertNotIn(self.v4, span)


    def test_origin_always_in_span(self):
        span = VectorSpan(self.v1, self.v2, self.v3)
        self.v4.values.return_value = [0, 0, 0]
        self.assertIn(self.v4, span)


    def test_vector_in_1v_span(self):
        span = VectorSpan(self.v1)
        self.assertIn(self.v2, span)
        self.v1.__iter__.return_value = iter([2, 5, -9])
        self.v2.__iter__.return_value = iter([1, 2.5, -4.5])
        self.assertIn(self.v2, span)
        self.v2.__iter__.return_value = iter([1, 2.5, -4.6])
        self.assertNotIn(self.v2, span)


    def test_no_vectors_in_span_of_zero_vector(self):
        self.v1.values.return_value = (0, 0, 0)
        span = VectorSpan(self.v1)
        self.assertNotIn(self.v2, span)


    def test_rejection_of_vectors_with_zero_components(self):
        span = VectorSpan(self.v1)
        self.v2.values.return_value = (1, 0, -4.5)
        self.assertNotIn(self.v2, span)
        self.v1.values.return_value = (2, 0, -9)
        self.assertIn(self.v2, span)


    @patch("points.matrices.Matrix")
    def test_vector_in_2v_span(self, mock_matrix):
        mock_augment = Mock()
        mock_matrix.return_value = mock_augment
        mock_augment.rows.return_value = ((4, 6, 8), (0, 2, 4), (0, 0, 0))
        span = VectorSpan(self.v1, self.v2)
        self.assertIn(self.v3, span)
        self.assertEqual(
         set(mock_matrix.call_args[0]), {self.v1, self.v2, self.v3}
        )
        self.assertEqual(mock_matrix.call_args[0][-1], self.v3)
        self.assertEqual(mock_matrix.call_args[1], {"columns": True})
        mock_augment.gauss.assert_called_with()


    @patch("points.matrices.Matrix")
    def test_vector_not_in_2v_span(self, mock_matrix):
        mock_augment = Mock()
        mock_matrix.return_value = mock_augment
        mock_augment.rows.return_value = ((4, 6, 8), (0, 2, 4), (0, 0, 9))
        span = VectorSpan(self.v1, self.v2)
        self.assertNotIn(self.v3, span)
        self.assertEqual(
         set(mock_matrix.call_args[0]), {self.v1, self.v2, self.v3}
        )
        self.assertEqual(mock_matrix.call_args[0][-1], self.v3)
        self.assertEqual(mock_matrix.call_args[1], {"columns": True})
        mock_augment.gauss.assert_called_with()



class VectorSpanDimensionTests(VectorSpanTest):

    def test_can_get_span_dimension(self):
        span = VectorSpan(self.v1)
        self.assertEqual(span.dimension(), span._dimension)



class VectorSpanRankTests(VectorSpanTest):

    def test_can_get_span_rank(self):
        span = VectorSpan(self.v1)
        self.assertEqual(span.rank(), 1)
        span._vectors = range(10)
        self.assertEqual(span.rank(), 10)
