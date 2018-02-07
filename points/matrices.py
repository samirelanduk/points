"""Contains the Matrix class."""

from .vectors import Vector

class Matrix:
    """A Matrix is a rectangular array of numbers. They are created from
    iterables, which will be interpeted as rows. If you pass :py:class:`.Vector`
    objects though, they will be interpreted as columns.

    They can be added and subtracted from each other, and multiplied by a scalar
    using the `*` operator. To multiply a Matrix with another Matrix, use ``@``.

    :param iter args: The rows of the Matrix. Each row must be iterable.
    :raises ValueError: if you create an empty matrix.
    :raises TypeError: if you mix Vectors with other iterables.
    :raises TypeError: if you give non iterables.
    :raises ValueError: if you give rows of different lengths."""

    def __init__(self, *args):
        self._rows = []
        try: width = len(args[0])
        except:
            raise ValueError("Matrix cannot be empty")
        if any([isinstance(arg, Vector) for arg in args]):
            if not all([isinstance(arg, Vector) for arg in args]):
                raise TypeError(
                 "Either all Matrix args have to be Vectors, or none"
                )
            args = [[
             vector._values[n] for vector in args
            ] for n in range(len(args[0]))]
            width = len(args[0])
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
            raise ValueError("{} & {} are different sizes".format(self, other))
        rows = [[
         n1 + n2 for n1, n2 in zip(row1, row2)
        ] for row1, row2 in zip(self._rows, other._rows)]
        return Matrix(*rows)


    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError("{} is not a Matrix".format(other))
        if self.size() != other.size():
            raise ValueError("{} & {} are different sizes".format(self, other))
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
        if isinstance(other, Vector):
            other = Matrix(other)
        if not isinstance(other, Matrix):
            raise TypeError("{} is not a Matrix".format(other))
        if self.size()[1] != other.size()[0]:
            raise ValueError(
             "{} and {} dimensions incompatible".format(self, other)
            )
        new_rows = []
        other_columns = other.columns()
        for row in self._rows:
            new_row = []
            for c in range(len(other_columns)):
                new_row.append(sum([
                 row[j] * other._rows[j][c] for j in range(len(other._rows))
                ]))
            new_rows.append(new_row)
        if len(new_rows[0]) == 1:
            return Vector([r[0] for r in new_rows])
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

        return (self.height(), self.width())


    def rows(self):
        """Returns the rows of the Matrix.

        :rtype: ``tuple``"""

        return tuple([tuple(row) for row in self._rows])


    def columns(self):
        """Returns the rows of the Matrix.

        :rtype: ``tuple``"""

        return tuple([tuple([
         row[n] for row in self._rows
        ]) for n in range(len(self._rows[0]))])


    def transposed(self):
        """Returns a transposed version of the matrix. The matrix calling the
        method is unaffected.

        :rtype: ``Matrix``"""

        return Matrix(*map(list, zip(*self._rows)))


    def is_square(self):
        """Checks if the number of rows equals the number of columns.

        :rtype: ``bool``"""

        return self.width() == self.height()


    def minor(self, i, j):
        """Returns the first minor of the value at the position specified.

        :param int i: The row to use.
        :param int j: The column to use.
        :raises ValueError: if a non-square matrix is given.
        :rtype: ``float``"""

        if not self.is_square():
            raise ValueError("{} is not square".format(self))
        if self.width() == 2:
            return self._rows[1-i][1-j]


    def cofactor(self, i, j):
        """Returns the cofactor of the value at the position specified.

        :param int i: The row to use.
        :param int j: The column to use.
        :raises ValueError: if a non-square matrix is given.
        :rtype: ``float``"""

        return self.minor(i, j) * ((-1) ** (i + j))


    def minors(self):
        """Returns the Matrix of minors for this matrix.

        :raises ValueError: if a non-square matrix is given.
        :rtype: ``Matrix``"""

        return Matrix(*[[
         self.minor(i, j) for j in range(len(row))
        ] for i, row in enumerate(self._rows)])


    def cofactors(self):
        """Returns the Matrix of cofactors for this matrix.

        :raises ValueError: if a non-square matrix is given.
        :rtype: ``Matrix``"""

        return Matrix(*[[
         self.cofactor(i, j) for j in range(len(row))
        ] for i, row in enumerate(self._rows)])


    def determinant(self):
        """Returns the determinant of the matrix - the matrix must be square for
        this to happen.

        The Laplace expansion is used to calculate matrices of three dimensions
        and above.

        :raises ValueError: if a non-square matrix is given.
        :rtype: ``float``"""

        if not self.is_square():
            raise ValueError("{} is not square".format(self))
        if self.width() == 2:
            return ((self._rows[0][0] * self._rows[1][1])
             - (self._rows[0][1] * self._rows[1][0]))
        else:
            products = []
            for index, value in enumerate(self._rows[0]):
                matrix = Matrix(*[
                 [val for index2, val in enumerate(row) if index2 != index]
                  for row in self._rows[1:]
                ])
                products.append(value * matrix.determinant())
            det = 0
            for index, product in enumerate(products):
                det = det - product if index % 2 else det + product
            return det


    '''def inverse(self):
        if not self.determinant():
            raise ValueError("{} has no inverse: determinant is 0".format(self))
        for r_index, row in enumerate(self._rows):
            cofactor_row = []
            for c_index, cell in enumerate(row):
                new_rows = [[cell2 for c_index2, cell2 in enumerate(row) if c_index2 != c_index] for row2, r_index2 in enumerate(self._rows) if r_index2 != r_index]
                print(new_rows)'''