"""Contains the Matrix class."""

class Matrix:
    """A Matrix is a raectangular array of numbers:

    :param iter args: The rows of the Matrix. Each row must be iterable.
    :raises ValueError: if you create an empty matrix.
    :raises TypeError: if you give non iterables.
    :raises ValueError: if you give rows of different lengths."""

    def __init__(self, *args):
        self._rows = []
        try: width = len(args[0])
        except:
            raise ValueError("Matrix cannot be empty")
        for arg in args:
            try: iter(arg)
            except:
                raise TypeError("Matrix row {} is not iterable".format(arg))
            if len(arg) != width:
                raise ValueError(
                 "Matrix row {} is not length {}".format(arg, width)
                )
            if any(not isinstance(element, (int, float)) for element in arg):
                raise TypeError("row {} has non-numeric values".format(arg))
            self._rows.append(list(arg))
