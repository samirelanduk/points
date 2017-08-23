from unittest import TestCase
from unittest.mock import Mock, patch
from points.checks import is_numeric, are_numeric

class IsNumericTests(TestCase):

    def test_integers_classed_as_numeric(self):
        self.assertTrue(is_numeric(-5))
        self.assertTrue(is_numeric(0))
        self.assertTrue(is_numeric(5))


    def test_floats_classed_as_numeric(self):
        self.assertTrue(is_numeric(-5.34))
        self.assertTrue(is_numeric(0.0))
        self.assertTrue(is_numeric(5.9))


    def test_everything_else_not_classed_as_numeric(self):
        self.assertFalse(is_numeric("string"))
        self.assertFalse(is_numeric(None))
        self.assertFalse(is_numeric(False))
        self.assertFalse(is_numeric(True))



class AreNumericTests(TestCase):

    @patch("points.checks.is_numeric")
    def test_returns_true_when_all_numeric(self, mock_is):
        mock_is.return_value = True
        self.assertTrue(are_numeric(-1, -0.5, 0, 0.5, 1))


    @patch("points.checks.is_numeric")
    def test_returns_false_when_one_item_is_non_numeric(self, mock_is):
        mock_is.side_effect = [True, True, True, True, False]
        self.assertFalse(are_numeric(-1, -0.5, 0, 0.5, 1))
