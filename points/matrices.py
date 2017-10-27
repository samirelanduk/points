"""Contains the Matrix class."""

class Matrix:
    """A Matrix is a rectangular array of numbers.

    They can be added and subtracted from each other, and multiplied by a scalar
    using the `*` operator. To multiply a Matrix with another Matrix, use `@`.

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


    def __repr__(self):
        return "<{}×{} Matrix>".format(*self.size())


    def __contains__(self, item):
        return any([item in row for row in self._rows])


    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("{} is not a Matrix".format(other))
        if self.size() != other.size():
            raise ValueError("{} and {} are different sizes".format(self, other))
        rows = [[
         n1 + n2 for n1, n2 in zip(row1, row2)
        ] for row1, row2 in zip(self._rows, other._rows)]
        return Matrix(*rows)


    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("{} is not a Matrix".format(other))
        if self.size() != other.size():
            raise ValueError("{} and {} are different sizes".format(self, other))
        rows = [[
         n1 - n2 for n1, n2 in zip(row1, row2)
        ] for row1, row2 in zip(self._rows, other._rows)]
        return Matrix(*rows)


    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError(
             "{} isn't numeric - Matrix * operator needs scalars".format(other)
            )
        rows = [[n * other for n in row] for row in self._rows]
        return Matrix(*rows)


    def __rmul__(self, other):
        return self * other


    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("{} is not a Matrix".format(other))
        if self.size()[1] != other.size()[0]:
            raise ValueError(
             "{} and {} dimensions incompatible".format(self, other)
            )
        new_rows = []
        other_columns = [[
         row[n] for row in other._rows
        ] for n in range(len(other._rows[0]))]
        for row in self._rows:
            new_row = []
            for c in range(len(other_columns)):
                new_row.append(sum([
                 row[j] * other._rows[j][c] for j in range(len(other._rows))
                ]))
            new_rows.append(new_row)
        return Matrix(*new_rows)



    def width(self):
        """Returns the Matrix width - how many columns it has.

        :rtype: ``int``"""

        return len(self._rows[0])


    def height(self):
        """Returns the Matrix height - how many rows it has.

        :rtype: ``int``"""

        return len(self._rows)


    def size(self):
        """Returns the dimensions of the Matrix.

        :rtype: ``tuple``"""

        return (self.width(), self.height())


    def rows(self):
        """Returns the rows of the Matrix.

        :rtype: ``tuple``"""

        return tuple([tuple(row) for row in self._rows])
